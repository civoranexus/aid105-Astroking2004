import os
import psycopg2
from pathlib import Path


def run_sql_file(conn, path: Path):
    sql = path.read_text()
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()


def main():
    db_url = os.environ.get("DATABASE_URL", "postgresql://civora:civora@db:5432/schemeassist")
    # psycopg2.connect accepts a DSN or connection string
    try:
        conn = psycopg2.connect(db_url)
    except Exception as e:
        print(f"Could not connect to DB for migrations: {e}")
        return 1

    schema_file = Path(__file__).resolve().parents[2] / "schemas" / "db_schema.sql"
    if not schema_file.exists():
        print(f"Schema file not found at {schema_file}")
        return 1

    print(f"Applying schema from {schema_file}")
    try:
        run_sql_file(conn, schema_file)
        print("Migrations applied")
    except Exception as e:
        print(f"Error applying migrations: {e}")
    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
