"""P3 persistence repository."""

from __future__ import annotations

import sqlite3
from uuid import uuid4

from keiji.p3_profit.input_models import ProfitEstimate, ProfitInput


class P3Repository:
    """Persist P3 runs and profit estimates."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def create_run(self, *, rules_version: str, identity_decision_id: str, status: str, skip_reason: str | None = None) -> str:
        run_id = str(uuid4())
        self.connection.execute(
            """
            INSERT INTO p3_profit_runs (id, rules_version, identity_decision_id, status, skip_reason)
            VALUES (?, ?, ?, ?, ?)
            """,
            (run_id, rules_version, identity_decision_id, status, skip_reason),
        )
        self.connection.commit()
        return run_id

    def save_estimate(
        self,
        *,
        p3_run_id: str,
        identity_decision_id: str,
        profit_input: ProfitInput,
        estimate: ProfitEstimate,
    ) -> str:
        estimate_id = str(uuid4())
        self.connection.execute(
            """
            INSERT INTO profit_estimates
            (id, p3_run_id, identity_decision_id, expected_sale_price_yen, purchase_price_yen,
             inbound_shipping_yen, platform_fee_yen, fulfillment_fee_yen, storage_fee_yen, other_cost_yen,
             net_profit_yen, roi_percent, profit_margin_percent, break_even_price_yen,
             risk_adjusted_profit_yen, decision, decision_reason, requires_human_approval)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                estimate_id,
                p3_run_id,
                identity_decision_id,
                profit_input.expected_sale_price_yen,
                profit_input.purchase_price_yen,
                profit_input.inbound_shipping_yen,
                estimate.fees.platform_fee_yen,
                estimate.fees.fulfillment_fee_yen,
                estimate.fees.storage_fee_yen,
                estimate.fees.other_cost_yen,
                estimate.net_profit_yen,
                estimate.roi_percent,
                estimate.profit_margin_percent,
                estimate.break_even_price_yen,
                estimate.risk_adjusted_profit_yen,
                estimate.decision,
                ";".join(estimate.reasons),
                int(estimate.requires_human_approval),
            ),
        )
        self.connection.commit()
        return estimate_id

    def get_estimate(self, estimate_id: str) -> sqlite3.Row:
        row = self.connection.execute("SELECT * FROM profit_estimates WHERE id = ?", (estimate_id,)).fetchone()
        if row is None:
            raise KeyError(estimate_id)
        return row
