"""
Week 1 Assessment - Task 2: Files, APIs and Environment

1. Read data/employees.csv with csv.DictReader
2. Write data/employees.json and data/high_earners.csv (salary above 50000)
3. Load API_KEY from .env with python-dotenv
4. GET /users safely (timeout=5, handle Timeout and ConnectionError)
5. GET /users/9999 and handle the expected 404
6. Read nested JSON fields with .get() and save data/users.json
"""

import csv
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent       # the week1-assessment folder
DATA_DIR = ROOT / "data"
BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 5                               # seconds to wait before giving up


# ---------------------------------------------------------------------------
# 1-2. FILE I/O: CSV -> JSON and CSV
# ---------------------------------------------------------------------------
def read_employees(path):
    """Read the CSV into a list of dicts; convert id and salary from text to int."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["id"] = int(row["id"])
        row["salary"] = int(row["salary"])
    return rows


def write_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)       # indent=2 makes the file readable


def write_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# 4-5. SAFE API CALL
# ---------------------------------------------------------------------------
def get_json(endpoint):
    """
    GET BASE_URL + endpoint.
    Returns the parsed JSON, or None if anything went wrong.
    Each kind of failure is handled separately so the message is clear.
    """
    url = BASE_URL + endpoint
    try:
        response = requests.get(url, timeout=TIMEOUT)
        if response.status_code == 404:
            print(f"{endpoint} -> 404 Not found")
            return None
        response.raise_for_status()        # raises HTTPError for other 4xx/5xx codes
        return response.json()
    except requests.exceptions.Timeout:
        print(f"{endpoint} -> Timeout: no reply within {TIMEOUT} seconds")
    except requests.exceptions.ConnectionError:
        print(f"{endpoint} -> ConnectionError: check your internet connection")
    except requests.exceptions.HTTPError as error:
        print(f"{endpoint} -> HTTP error: {error}")
    return None


# ---------------------------------------------------------------------------
# 6. NESTED JSON WITH .get()
# ---------------------------------------------------------------------------
def simplify_user(user):
    """
    'address' and 'company' are nested dictionaries inside each user.
    .get(key, {}) returns an empty dict if the key is missing,
    so the second .get() never crashes.
    """
    return {
        "id": user.get("id"),
        "name": user.get("name"),
        "email": user.get("email"),
        "city": user.get("address", {}).get("city"),
        "company": user.get("company", {}).get("name"),
    }


def main():
    # --- Files ---
    employees = read_employees(DATA_DIR / "employees.csv")
    high_earners = [e for e in employees if e["salary"] > 50000]
    write_json(employees, DATA_DIR / "employees.json")
    write_csv(high_earners, DATA_DIR / "high_earners.csv")
    print(f"Rows read: {len(employees)} | High earners: {len(high_earners)}")

    # --- Environment variable ---
    load_dotenv(ROOT / ".env")             # copies values from .env into os.environ
    api_key = os.getenv("API_KEY")
    # Never print the secret itself, only whether it was found.
    print("API_KEY loaded:", "yes" if api_key else "no (copy .env.example to .env)")

    # --- API ---
    users = get_json("/users")
    if users:
        for user in users[:3]:
            print(f"{user['id']} - {user['name']} - {user['email']}")

        simplified = [simplify_user(u) for u in users]
        write_json(simplified, DATA_DIR / "users.json")
        print(f"Saved {len(simplified)} users to data/users.json "
              f"(e.g. {simplified[0]['name']} lives in {simplified[0]['city']})")

    get_json("/users/9999")                # this user does not exist -> 404


if __name__ == "__main__":
    main()
