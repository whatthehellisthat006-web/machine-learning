import csv
from collections import Counter
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tickets.csv"


def main():
    if not DATA_FILE.is_file():
        raise SystemExit(
            f"Dataset not found: {DATA_FILE}\n"
            "Get tickets.csv from the course materials and put it in atelier2/data."
        )

    with DATA_FILE.open(encoding="utf-8-sig", newline="") as csv_file:
        tickets = list(csv.DictReader(csv_file))

    if not tickets:
        raise SystemExit(f"Dataset is empty: {DATA_FILE}")

    counts = Counter(ticket["categorie"] for ticket in tickets)
    total = len(tickets)

    print(f"Tickets: {total}")
    for category, count in counts.most_common():
        percentage = 100 * count / total
        print(f"{category:<13}{count:>3}  {percentage:>5.1f} %  {'#' * count}")


if __name__ == "__main__":
    main()
