# Latitude Anonymizer Challenge

Generate realistic customer data, then anonymize the sensitive columns.

## Contents

1. [Architecture diagram](#architecture-diagram)  
2. [Features](#features)
3. [Design details](#design-details)  
4. [Repository layout](#repository-layout)  
5. [Local setup](#local-setup)  
6. [CLI usage](#cli-usage)
7. [Run from Docker Hub image](#run-from-docker-hub-image)  


---

## Architecture diagram

<img width="764" height="258" alt="image" src="https://github.com/user-attachments/assets/2baf82bb-fa47-4d6e-9576-c478a04cad0c" />



*Developer pushes → CI runs pytest → main branch push triggers CD → Docker image is built and pushed with the current date tag.*

---

## Features

| Area            | Details                                                                                 |
|-----------------|-----------------------------------------------------------------------------------------|
| **Data generation** | `generator.py` uses the [Faker](https://faker.readthedocs.io/) library to create realistic `first_name`, `last_name`, `address`, and `date_of_birth` fields.|
| **Anonymization**  | `anonymizer.py` hashes `first_name`, `last_name`, and `address` with SHA-256 and a salt, leaving `date_of_birth` intact.|
| **Tests**          | Pytest covers both the anonymizer and generator scripts.                           |
| **Docker**         | Self-contained image lets you run either command (`generate` or `anonymize`).         |
| **CI**             | Pull requests and pushes run pytest on Ubuntu-latest with Python 3.9.                 |
| **CD**             | Every push to `main` builds the Docker image and tags it as `YYYYMMDD` in Docker Hub. |

---
## Design-details

<img width="761" height="324" alt="image" src="https://github.com/user-attachments/assets/bb0049bf-2bd6-4303-a8d5-08bbef0d1983" />

### `generator.py` (overview)

`generator.py` produces a CSV file filled with realistic, synthetic customer data.  It accepts two main flags:

* **`--out`** – path for the output CSV (default: `customers.csv`)  
* **`--rows`** – number of fake records to create (default: 100)  

Internally it uses the **Faker** library to create a first name, last name, street-style address, and an ISO-formatted date of birth for each row, then writes everything to  `csv`.

---

### `anonymizer.py` (overview)

`anonymizer.py` is the companion script that takes an existing CSV and pseudonymises the sensitive columns.  It expects:

* **`--in`** – input CSV path  
* **`--out`** – output CSV path  
* **`--salt`** – (optional) salt string; if omitted it falls back to the `ANON_SALT` environment variable  

The script  hashes the `first_name`, `last_name`, and `address` fields using SHA-256 plus the provided salt, and writes the result, leaving non-PII fields such as `date_of_birth` untouched.  

---
## Repository layout
.
```text
.
├── src
│   ├── anonymizer.py        # Hashes PII columns
│   └── generator.py         # Writes fake CSV data
├── tests                    # Pytest suite
│   ├── test_anonymizer.py
│   └── test_generator.py
├── Dockerfile
├── requirements.txt
└── .github
    └── workflows
        ├── ci.yml           # Test pipeline
        └── cd.yml           # Docker build & push
```
---
## Local setup

```bash
python -m venv .venv
source .venv/bin/activate         # for Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
---
## CLI usage

### Generate a CSV
```bash
python -m src.generator --out customers.csv --rows 100
```

### Anonymize a CSV
```bash
export ANON_SALT="mysupersecret" #can be any key
python -m src.anonymizer --in customers.csv --out anonymized.csv
```

### Test 
```bash
python -m pytest -v
```
---
## Run from remote Docker Hub Image
replace <DOCKERHUB_USERNAME> with actual Docker Hub username.

### Pull docker 
```bash
docker pull <DOCKERHUB_USERNAME>/divya-anonymizer:20250714
```
### Generate customer data 
```bash
docker run --rm -v "$(pwd -W)":/data <DOCKERHUB_USERNAME>/divya-anonymizer:20250714 generate --out /data/customer.csv --rows 100 
```
### Anonymize customer data 
```bash
 docker run --rm -e ANON_SALT=mysupersecret -v "$(pwd -W)":/data <DOCKERHUB_USERNAME>/divya-anonymizer:20250714 anonymize --in /data/customer.csv --out /data/anon_data.csv
```





---
