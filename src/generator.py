# fake csv generator
import argparse
import csv
from pathlib import Path
from typing import Sequence

from faker import Faker

HEADERS: Sequence[str] = ("first_name", "last_name", "address", "date_of_birth")
fake = Faker()


def generate_csv(path: Path, rows: int = 1000) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)

        for _ in range(rows):
            dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
            writer.writerow(
                [
                    fake.first_name(),
                    fake.last_name(),
                    fake.address().replace("\n", ", "),
                    dob.isoformat(),
                ]
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fake customer CSV generator")
    parser.add_argument("--out", default="customers.csv", help="output CSV path")
    parser.add_argument("--rows", type=int, default=1000, help="number of rows")
    parser.add_argument(
        "--seed", type=int, help="set Faker random seed for reproducibility"
    )
    args = parser.parse_args()

    if args.seed is not None:
        Faker.seed(args.seed)

    generate_csv(Path(args.out), args.rows)

