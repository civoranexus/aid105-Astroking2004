import os
import socket
import time
from urllib.parse import urlparse


def parse_db_url(url: str):
    # Expect format: dialect://user:pass@host:port/db
    parsed = urlparse(url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 5432
    return host, port


def wait_for(host: str, port: int, timeout: int = 120):
    start = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=2):
                return True
        except Exception:
            if time.time() - start > timeout:
                return False
            time.sleep(1)


def main():
    db_url = os.environ.get("DATABASE_URL") or "postgresql://civora:civora@db:5432/schemeassist"
    host, port = parse_db_url(db_url)
    ok = wait_for(host, port, timeout=120)
    if not ok:
        print(f"WARNING: DB at {host}:{port} not ready after timeout")
    else:
        print(f"DB reachable at {host}:{port}")


if __name__ == "__main__":
    main()
