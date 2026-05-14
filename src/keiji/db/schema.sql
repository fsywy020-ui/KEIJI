PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS source_offers (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  brand TEXT,
  model TEXT,
  jan TEXT,
  asin TEXT,
  condition TEXT NOT NULL,
  purchase_price_yen INTEGER NOT NULL,
  domestic_shipping_yen INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS market_listings (
  id TEXT PRIMARY KEY,
  marketplace TEXT NOT NULL,
  title TEXT NOT NULL,
  brand TEXT,
  model TEXT,
  jan TEXT,
  asin TEXT,
  condition TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS p4_identity_runs (
  id TEXT PRIMARY KEY,
  rules_version TEXT NOT NULL,
  source_offer_id TEXT NOT NULL,
  market_listing_id TEXT NOT NULL,
  status TEXT NOT NULL,
  started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  finished_at TEXT,
  error_message TEXT,
  FOREIGN KEY (source_offer_id) REFERENCES source_offers(id),
  FOREIGN KEY (market_listing_id) REFERENCES market_listings(id)
);

CREATE TABLE IF NOT EXISTS product_identity_decisions (
  id TEXT PRIMARY KEY,
  p4_run_id TEXT NOT NULL,
  source_offer_id TEXT NOT NULL,
  market_listing_id TEXT NOT NULL,
  decision TEXT NOT NULL,
  confidence_score REAL NOT NULL,
  match_score REAL NOT NULL,
  identifier_score REAL NOT NULL,
  title_score REAL NOT NULL,
  brand_score REAL NOT NULL,
  variant_score REAL NOT NULL,
  condition_score REAL NOT NULL,
  block_reason TEXT,
  explanation_json TEXT NOT NULL,
  requires_human_review INTEGER NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (p4_run_id) REFERENCES p4_identity_runs(id),
  FOREIGN KEY (source_offer_id) REFERENCES source_offers(id),
  FOREIGN KEY (market_listing_id) REFERENCES market_listings(id)
);

CREATE TABLE IF NOT EXISTS p3_profit_runs (
  id TEXT PRIMARY KEY,
  rules_version TEXT NOT NULL,
  identity_decision_id TEXT NOT NULL,
  status TEXT NOT NULL,
  skip_reason TEXT,
  started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  finished_at TEXT,
  FOREIGN KEY (identity_decision_id) REFERENCES product_identity_decisions(id)
);

CREATE TABLE IF NOT EXISTS profit_estimates (
  id TEXT PRIMARY KEY,
  p3_run_id TEXT NOT NULL,
  identity_decision_id TEXT NOT NULL,
  expected_sale_price_yen INTEGER,
  purchase_price_yen INTEGER NOT NULL,
  inbound_shipping_yen INTEGER NOT NULL,
  platform_fee_yen INTEGER NOT NULL,
  fulfillment_fee_yen INTEGER NOT NULL,
  storage_fee_yen INTEGER NOT NULL,
  other_cost_yen INTEGER NOT NULL,
  net_profit_yen INTEGER NOT NULL,
  roi_percent REAL NOT NULL,
  profit_margin_percent REAL NOT NULL,
  break_even_price_yen INTEGER NOT NULL,
  risk_adjusted_profit_yen INTEGER NOT NULL,
  decision TEXT NOT NULL,
  decision_reason TEXT NOT NULL,
  requires_human_approval INTEGER NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (p3_run_id) REFERENCES p3_profit_runs(id),
  FOREIGN KEY (identity_decision_id) REFERENCES product_identity_decisions(id)
);

CREATE TABLE IF NOT EXISTS purchase_candidates (
  id TEXT PRIMARY KEY,
  profit_estimate_id TEXT NOT NULL,
  status TEXT NOT NULL,
  requested_quantity INTEGER NOT NULL,
  total_purchase_amount_yen INTEGER NOT NULL,
  requires_human_approval INTEGER NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (profit_estimate_id) REFERENCES profit_estimates(id)
);

CREATE TABLE IF NOT EXISTS human_approvals (
  id TEXT PRIMARY KEY,
  target_type TEXT NOT NULL,
  target_id TEXT NOT NULL,
  decision TEXT NOT NULL,
  reviewer_name TEXT NOT NULL,
  comment TEXT,
  approved_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_logs (
  id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,
  actor TEXT NOT NULL,
  target_type TEXT NOT NULL,
  target_id TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
