import csv
from pathlib import Path
from src.generator import generate_csv

def test_generate_csv(tmp_path):
    out = tmp_path / "gen.csv"
    generate_csv(out, rows=3)

    with open(out, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 4       
    assert rows[0] == ["first_name","last_name","address","date_of_birth"]
    for data_row in rows[1:]:
        assert len(data_row) == 4
