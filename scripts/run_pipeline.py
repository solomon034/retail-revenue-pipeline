"""Run the complete local dbt workflow and print a small mart preview."""

from __future__ import annotations

import os
import shutil
import sqlite3
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE = ROOT / "warehouse"
DATABASE = WAREHOUSE / "analytics.db"


def run(*args: str) -> None:
    print(f"\n$ {' '.join(args)}")
    subprocess.run(args, cwd=ROOT, check=True, env=os.environ.copy())


def main() -> int:
    WAREHOUSE.mkdir(exist_ok=True)
    dbt = shutil.which("dbt")
    if dbt is None:
        raise SystemExit("dbt is not installed; run: pip install -r requirements.txt")
    for command in ("seed", "run", "test"):
        run(dbt, command, "--profiles-dir", ".")

    with sqlite3.connect(DATABASE) as connection:
        rows = connection.execute(
            """
            select order_status, count(*) as orders,
                   round(sum(recognized_revenue), 2) as revenue
            from fct_orders
            group by order_status
            order by order_status
            """
        ).fetchall()

    print("\nValidated mart preview")
    for status, orders, revenue in rows:
        print(f"  {status:10} orders={orders} revenue={revenue:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

