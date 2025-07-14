import csv
from src.anonymizer import hash_pseudonym, anonymize_csv

def test_hash_pseudonym():
    salt = b'test'
    assert hash_pseudonym('A', salt) == hash_pseudonym('A', salt)
    assert hash_pseudonym('A', salt) != hash_pseudonym('B', salt)

def test_anonymize_csv(tmp_path):
    salt = b'test_salt'
    inp = tmp_path / 'in.csv'
    out = tmp_path / 'out.csv'
    inp.write_text(
        'first_name,last_name,address,date_of_birth\n'
        'Alice,Smith,123 St,1990-01-01\n'
    )

    anonymize_csv(str(inp), str(out), salt)

    row = next(csv.DictReader(out.read_text().splitlines()))
    assert row['first_name'] != 'Alice'
    assert row['last_name']  != 'Smith'
    assert row['address']    != '123 St'
    assert row['date_of_birth'] == '1990-01-01'
