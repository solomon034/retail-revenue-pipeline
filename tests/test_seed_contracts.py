"""Fast source-contract checks that require only the Python standard library."""

from __future__ import annotations

import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_seed(name: str) -> list[dict[str, str]]:
    with (ROOT / "seeds" / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class SeedContractTests(unittest.TestCase):
    def test_primary_keys_are_unique(self) -> None:
        for name, key in (
            ("raw_customers.csv", "customer_id"),
            ("raw_orders.csv", "order_id"),
            ("raw_payments.csv", "payment_id"),
        ):
            values = [row[key] for row in read_seed(name)]
            self.assertTrue(all(values), f"{name} contains a blank {key}")
            self.assertEqual(len(values), len(set(values)), f"{name} has duplicate {key}")

    def test_order_foreign_keys_and_statuses(self) -> None:
        customer_ids = {row["customer_id"] for row in read_seed("raw_customers.csv")}
        orders = read_seed("raw_orders.csv")
        self.assertTrue({row["customer_id"] for row in orders} <= customer_ids)
        self.assertTrue({row["status"] for row in orders} <= {"completed", "pending", "returned"})

    def test_payment_orders_exist(self) -> None:
        order_ids = {row["order_id"] for row in read_seed("raw_orders.csv")}
        payment_order_ids = {row["order_id"] for row in read_seed("raw_payments.csv")}
        self.assertTrue(payment_order_ids <= order_ids)


if __name__ == "__main__":
    unittest.main()

