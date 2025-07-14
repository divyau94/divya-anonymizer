import csv
import os
import pytest
from src.anonymizer import hash_pseudonym, anonymize_csv

def test_hash_pseudonym_consistency():
    salt = b'test_salt'
    v1 = hash_pseudonym('Alice', salt)
    v2 = hash_pseudonym('Alice', salt)
    assert v1 == v2

def test_hash_pseudonym_variation():
    salt = b'test_salt'
    v1 = hash_pseudonym('Alice', salt)
    v2 = hash_pseudonym('Bob', salt)
    assert v1 != v2

def test_anonymize_csv(tmp_path, monkeypatch):
    # set a known salt
    monkeypatch.setenv('ANON_SALT', 'test_salt')
    input_file = tmp_path / 'in.csv'
    output_file = tmp_path / 'out.csv'
    input_file.write_text('first_name,last_name,address,date_of_birth\nAlice,Smith,123 St,1990-01-01\n')

    anonymize_csv(str(input_file), str(output_file))
    with open(output_file) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert rows and rows[0]['first_name'] != 'Alice'
        assert rows[0]['last_name'] != 'Smith'
