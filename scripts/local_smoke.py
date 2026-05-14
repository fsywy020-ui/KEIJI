#!/usr/bin/env python3
"""Run an end-to-end local offline smoke workflow.

The smoke workflow validates sample input, runs P4/P3 offline, exports review
CSV/HTML/Markdown, exports status reports, and exports audit logs. It does not
perform network calls or external actions.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from keiji.db.connection import connect, initialize_schema
from keiji.io.audit_export import export_audit_json, export_audit_markdown
from keiji.io.candidate_validation import validate_candidate_file
from keiji.io.local_candidates import load_candidates_csv, load_candidates_json
from keiji.io.review_export import export_pending_review_csv
from keiji.io.review_report import export_pending_review_html, export_pending_review_markdown
from keiji.io.status_report import export_status_json, export_status_markdown
from keiji.pipeline.offline_runner import OfflinePipelineRunner
from keiji.candidate_scoring import CandidateScoreInput, CandidateScoringEngine
from keiji.manus_handoff import (
    build_manus_handoff_packet,
    evaluate_manus_action,
    export_manus_handoff_packets_json,
    export_manus_handoff_packets_markdown,
)
from keiji.market_monitoring import load_market_observations, matching_market_observations
from keiji.p3_profit import ProfitInput
from keiji.review import build_candidate_review_packet, export_review_packets_csv, export_review_packets_json, export_review_packets_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Run local KEIJI smoke workflow")
    parser.add_argument("--input", default="data/samples/offline_candidates.example.csv")
    parser.add_argument("--out-dir", default="storage/smoke")
    parser.add_argument("--product-rules", default="config/product_identity_rules.v1.yaml")
    parser.add_argument("--profit-rules", default="config/profit_rules.v1.yaml")
    parser.add_argument("--market-input", default="data/samples/market_observations.example.csv")
    args = parser.parse_args()

    input_path = Path(args.input)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    validation = validate_candidate_file(input_path)
    if not validation.ok:
        print(validation.format_text())
        return 1

    db_path = out_dir / "keiji-smoke.sqlite3"
    if db_path.exists():
        db_path.unlink()
    p8_blocked_actions_audit_path = out_dir / "p8_blocked_actions_audit.jsonl"
    if p8_blocked_actions_audit_path.exists():
        p8_blocked_actions_audit_path.unlink()
    connection = connect(db_path)
    try:
        initialize_schema(connection)
        candidates = load_candidates_json(input_path) if input_path.suffix.lower() == ".json" else load_candidates_csv(input_path)
        runner = OfflinePipelineRunner(
            connection=connection,
            product_identity_rules_path=args.product_rules,
            profit_rules_path=args.profit_rules,
        )
        p7_packets = []
        market_observations = tuple(load_market_observations(args.market_input))
        p6_engine = CandidateScoringEngine()
        for index, candidate in enumerate(candidates, start=1):
            runner.run_one(candidate)
            identity = runner.p4_engine.evaluate(candidate.source_offer, candidate.market_listing)
            profit = runner.p3_engine.evaluate(
                ProfitInput(
                    id=f"smoke-profit:{index}",
                    p4_decision=identity.decision.value,
                    p4_confidence_score=identity.confidence_score,
                    p4_requires_human_review=identity.requires_human_review,
                    expected_sale_price_yen=candidate.expected_sale_price_yen,
                    purchase_price_yen=candidate.source_offer.purchase_price_yen,
                    inbound_shipping_yen=candidate.source_offer.domestic_shipping_yen,
                    category=candidate.category,
                    allocated_budget_yen=candidate.allocated_budget_yen,
                )
            )
            matching_market = matching_market_observations(
                market_observations,
                jan=candidate.market_listing.jan,
                asin=candidate.market_listing.asin,
                model_number=candidate.market_listing.model,
            )
            score = p6_engine.score(
                CandidateScoreInput(
                    candidate_id=f"smoke-candidate:{index}",
                    source_offer=candidate.source_offer,
                    market_listing=candidate.market_listing,
                    identity_decision=identity,
                    profit_estimate=profit,
                    market_observations=matching_market,
                    allocated_budget_yen=candidate.allocated_budget_yen,
                )
            )
            p7_packets.append(
                build_candidate_review_packet(
                    candidate_id=f"smoke-candidate:{index}",
                    source_offer=candidate.source_offer,
                    market_listing=candidate.market_listing,
                    identity_decision=identity,
                    profit_estimate=profit,
                    market_observations=matching_market,
                    candidate_score=score,
                    allocated_budget_yen=candidate.allocated_budget_yen,
                )
            )
        export_pending_review_csv(connection, out_dir / "pending_review.csv")
        export_pending_review_html(connection, out_dir / "pending_review.html")
        export_pending_review_markdown(connection, out_dir / "pending_review.md")
        export_status_json(connection, out_dir / "status.json")
        export_status_markdown(connection, out_dir / "status.md")
        export_audit_json(connection, out_dir / "audit_log.json")
        export_audit_markdown(connection, out_dir / "audit_log.md")
        export_review_packets_json(p7_packets, out_dir / "p7_review_packets.json")
        export_review_packets_csv(p7_packets, out_dir / "p7_review_packets.csv")
        export_review_packets_markdown(p7_packets, out_dir / "p7_review_packets.md")
        p8_packets = [build_manus_handoff_packet(packet) for packet in p7_packets]
        export_manus_handoff_packets_json(p8_packets, out_dir / "p8_manus_handoff_packets.json")
        export_manus_handoff_packets_markdown(p8_packets, out_dir / "p8_manus_handoff_packets.md")
        for packet in p8_packets:
            evaluate_manus_action(
                requested_action="checkout",
                target_id=packet.candidate_id,
                audit_path=p8_blocked_actions_audit_path,
            )
    finally:
        connection.close()
    print(f"smoke_ok=true out_dir={out_dir} processed={len(candidates)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
