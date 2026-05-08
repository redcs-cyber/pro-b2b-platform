CREATE TABLE customer_accounts (
  customer_id TEXT PRIMARY KEY,
  parent_customer_id TEXT REFERENCES customer_accounts(customer_id),
  name TEXT NOT NULL,
  tier TEXT NOT NULL,
  tax_office TEXT NOT NULL,
  tax_number TEXT NOT NULL,
  gl_code TEXT NOT NULL,
  payment_term_days INTEGER NOT NULL,
  credit_limit NUMERIC(18,2) NOT NULL,
  balance NUMERIC(18,2) NOT NULL,
  kvkk_consent BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE b2b_products (
  sku TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  brand TEXT NOT NULL,
  category TEXT NOT NULL,
  list_price NUMERIC(18,2) NOT NULL,
  currency CHAR(3) NOT NULL DEFAULT 'TRY',
  vat_rate NUMERIC(5,4) NOT NULL DEFAULT 0.20,
  attributes JSONB NOT NULL DEFAULT '{}'
);

CREATE TABLE price_rules (
  rule_id TEXT PRIMARY KEY,
  priority INTEGER NOT NULL,
  rule_type TEXT NOT NULL,
  sku TEXT REFERENCES b2b_products(sku),
  customer_id TEXT REFERENCES customer_accounts(customer_id),
  tier TEXT,
  min_quantity INTEGER NOT NULL DEFAULT 1,
  discount_rate NUMERIC(6,5) NOT NULL DEFAULT 0,
  net_price NUMERIC(18,2),
  valid_range TSTZRANGE NOT NULL
);

CREATE TABLE stock_reservations (
  reservation_id TEXT PRIMARY KEY,
  order_id TEXT NOT NULL,
  sku TEXT NOT NULL REFERENCES b2b_products(sku),
  quantity INTEGER NOT NULL,
  warehouse_id TEXT NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE system_audit (
  audit_id BIGSERIAL PRIMARY KEY,
  actor_id TEXT NOT NULL,
  action TEXT NOT NULL,
  entity TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  ip_address INET NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
