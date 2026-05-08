import csv
from dataclasses import dataclass
from io import StringIO
from typing import Any

from api.b2b_ecosystem import B2BOrderLine


@dataclass
class QuickOrderParseResult:
    lines: list[B2BOrderLine]
    errors: list[dict[str, Any]]


def parse_quick_order_csv(content: str) -> QuickOrderParseResult:
    reader = csv.DictReader(StringIO(content.strip()))
    lines: list[B2BOrderLine] = []
    errors: list[dict[str, Any]] = []
    required = {"sku", "quantity"}
    if not reader.fieldnames or not required.issubset({name.strip() for name in reader.fieldnames}):
        return QuickOrderParseResult([], [{"row": 0, "error": "CSV başlıkları sku,quantity içermelidir"}])
    for row_number, row in enumerate(reader, start=2):
        sku = (row.get("sku") or "").strip()
        raw_quantity = (row.get("quantity") or "").strip()
        try:
            quantity = int(raw_quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            errors.append({"row": row_number, "sku": sku, "error": "quantity pozitif tam sayı olmalıdır"})
            continue
        if not sku:
            errors.append({"row": row_number, "error": "sku boş olamaz"})
            continue
        lines.append(B2BOrderLine(sku=sku, quantity=quantity))
    return QuickOrderParseResult(lines, errors)
