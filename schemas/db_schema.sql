-- DB schema for SchemeAssist AI (Postgres)

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  external_id VARCHAR(128),
  name VARCHAR(256),
  email VARCHAR(256),
  age INT,
  income NUMERIC,
  state VARCHAR(128),
  district VARCHAR(128),
  needs JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS schemes (
  id SERIAL PRIMARY KEY,
  scheme_id VARCHAR(64) UNIQUE,
  title TEXT,
  description TEXT,
  metadata JSONB,
  tags TEXT[],
  benefits JSONB,
  documents JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
