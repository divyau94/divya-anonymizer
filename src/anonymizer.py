# csv anonymizer
import argparse
import csv
import hashlib
import logging
import os
import sys
from typing import Sequence

# read salt from environment; override default in production
SALT = os.getenv('ANON_SALT', 'default_salt')
COLUMNS_TO_HASH: Sequence[str] = ("first_name", "last_name", "address")


def hash_pseudonym(value: str, salt: bytes) -> str:
    h = hashlib.sha256()
    h.update(salt)
    h.update(value.encode('utf-8'))
    return h.hexdigest()

def anonymize_csv(in_path: str, out_path: str, salt: bytes) -> None:
  
    with open(in_path, newline='', encoding='utf-8') as f_in, open(out_path, 'w', newline='', encoding='utf-8') as f_out:

        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            for col in COLUMNS_TO_HASH:
                row[col] = hash_pseudonym(row[col], salt)
            writer.writerow(row)

if __name__ == '__main__':
   
    parser = argparse.ArgumentParser(description="CSV anonymiser")
    parser.add_argument("--in", dest="in_path", required=True, help="input CSV")
    parser.add_argument("--out", dest="out_path", required=True, help="output CSV")
    args = parser.parse_args()


    if SALT == "default_salt":
        logging.warning(
            "Using default salt. Set ANON_SALT in the environment for production."
        )
    anonymize_csv(args.in_path, args.out_path,  SALT.encode("utf-8"))
