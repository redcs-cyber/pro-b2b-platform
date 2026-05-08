import argparse
import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from api.b2b_ecosystem import B2BEcosystemStore, B2BOrderCreate
from api.quick_order import parse_quick_order_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="ProB2B enterprise toolbox")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("blueprint", help="Platform blueprint JSON çıktısı üretir")

    quote = sub.add_parser("quote-csv", help="CSV hızlı siparişi teklif JSON çıktısına dönüştürür")
    quote.add_argument("csv_path", type=Path)
    quote.add_argument("--customer-id", default="CARI-99")
    quote.add_argument("--branch-id", default="ANKARA-SUBE")

    sub.add_parser("export-fixtures", help="Seed müşteri/ürün/fiyat verisini JSON olarak üretir")
    args = parser.parse_args()

    store = B2BEcosystemStore()
    if args.command == "blueprint":
        print(json.dumps(store.platform_blueprint(), ensure_ascii=False, indent=2))
    elif args.command == "quote-csv":
        parsed = parse_quick_order_csv(args.csv_path.read_text(encoding="utf-8"))
        quote_result = store.calculate_quote(B2BOrderCreate(args.customer_id, args.branch_id, parsed.lines)) if parsed.lines else None
        print(json.dumps({"quote": quote_result, "errors": parsed.errors}, ensure_ascii=False, indent=2))
    elif args.command == "export-fixtures":
        print(json.dumps(_fixtures(store), ensure_ascii=False, indent=2))


def _fixtures(store: B2BEcosystemStore) -> dict[str, Any]:
    return {
        "customers": [_dump(item) for item in store.customers.values()],
        "products": [_dump(item) for item in store.products.values()],
        "price_rules": [_dump(item) for item in store.price_rules],
    }


def _dump(value: Any) -> Any:
    return asdict(value) if is_dataclass(value) else value


if __name__ == "__main__":
    main()
