# Python JSON File Operations — Complete Guide

---

## Table of Contents

1. [Prerequisites & Setup](#1-prerequisites--setup)
2. [Core Concepts](#2-core-concepts)
3. [Call an API & Save to JSON File](#3-call-an-api--save-to-json-file)
4. [Update / Replace Specific Values](#4-update--replace-specific-values)
5. [Delete Objects from JSON](#5-delete-objects-from-json)
6. [Practice Exercises](#6-practice-exercises)

---

## 1. Prerequisites & Setup

### Python Version
Make sure you have Python 3.8+ installed.
```bash
python --version      # or python3 --version
```

### Built-in Libraries (no install needed)
These come with Python — just import them:

| Library | Purpose |
|---------|---------|
| `json` | Read/write JSON data |
| `urllib.request` | Make HTTP requests (basic) |

### Third-party Libraries (install these)
These make working with APIs much easier:

```bash
# Install using pip
pip install requests        # easier HTTP requests than urllib
pip install httpx           # modern async-friendly alternative to requests
```

Verify installation:
```bash
pip show requests
pip show httpx
```

> **Tip:** Use a virtual environment to keep dependencies isolated.
> ```bash
> python -m venv venv
> source venv/bin/activate        # Mac/Linux
> venv\Scripts\activate           # Windows
> pip install requests
> ```

---

## 2. Core Concepts

### What is JSON?
JSON (JavaScript Object Notation) is a text format for storing structured data.

```json
{
  "id": 1,
  "name": "Alice",
  "age": 30,
  "skills": ["python", "sql"],
  "address": {
    "city": "New York",
    "zip": "10001"
  }
}
```

### JSON ↔ Python mapping

| JSON | Python |
|------|--------|
| object `{}` | `dict` |
| array `[]` | `list` |
| string `""` | `str` |
| number | `int` / `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

### The 4 key functions in the `json` module

```python
import json

# 1. json.dumps()  — Python object  →  JSON string
data = {"name": "Alice", "age": 30}
json_string = json.dumps(data, indent=2)
print(json_string)
# {
#   "name": "Alice",
#   "age": 30
# }

# 2. json.loads()  — JSON string  →  Python object
parsed = json.loads('{"name": "Alice", "age": 30}')
print(parsed["name"])   # Alice

# 3. json.dump()   — Python object  →  write to FILE
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# 4. json.load()   — read from FILE  →  Python object
with open("data.json", "r") as f:
    loaded = json.load(f)
```

**Memory trick:** `dump/load` work with **files**. `dumps/loads` work with **strings** (the extra `s` = string).

---

## 3. Call an API & Save to JSON File

We'll use `https://jsonplaceholder.typicode.com` — a free public API, no key needed.

### Step-by-step breakdown

#### Step 1 — Make the API call
```python
import requests

url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)

# Always check the status code before using the data
print(response.status_code)   # 200 means success

data = response.json()        # automatically parses JSON → Python list
print(type(data))             # <class 'list'>
print(len(data))              # 10 users
```

#### Step 2 — Save to a file
```python
import json

with open("users.json", "w") as f:
    json.dump(data, f, indent=2)

print("File saved!")
```

#### Step 3 — Read it back
```python
with open("users.json", "r") as f:
    users = json.load(f)

print(users[0]["name"])        # Leanne Graham
print(users[0]["email"])       # Sincere@april.biz
```

### Complete working example
```python
import requests
import json

def fetch_and_save(url: str, filename: str):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    data = response.json()

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(data)} records to {filename}")
    return data


def load_json(filename: str):
    with open(filename, "r") as f:
        return json.load(f)


# --- Run it ---
users = fetch_and_save("https://jsonplaceholder.typicode.com/users", "users.json")
loaded = load_json("users.json")
print(loaded[0])
```

### What each part does

```
requests.get(url)        → sends HTTP GET request, returns a Response object
response.status_code     → HTTP status (200=OK, 404=Not Found, 500=Server Error)
response.json()          → parses the response body as JSON → Python object
json.dump(data, f)       → writes Python object into the open file f
indent=2                 → makes the file human-readable (pretty-printed)
json.load(f)             → reads the file and parses JSON → Python object
```

---

## 4. Update / Replace Specific Values

Once the data is in Python (a `dict` or `list`), you use standard Python operations to modify it, then write it back.

### Concept: Read → Modify → Write

```
users.json  →  json.load()  →  Python list  →  modify  →  json.dump()  →  users.json
```

### Example: Change a user's email by their ID

```python
import json

def update_user_email(filename: str, user_id: int, new_email: str):
    # 1. Read the file
    with open(filename, "r") as f:
        users = json.load(f)              # list of dicts

    # 2. Find and update
    for user in users:
        if user["id"] == user_id:
            print(f"Old email: {user['email']}")
            user["email"] = new_email     # direct dict assignment
            print(f"New email: {user['email']}")
            break
    else:
        print(f"User {user_id} not found")
        return

    # 3. Write back
    with open(filename, "w") as f:
        json.dump(users, f, indent=2)

    print("File updated!")


# Usage — pass user_id and new email as arguments
update_user_email("users.json", user_id=3, new_email="newemail@example.com")
```

### Example: Accept input from the command line

```python
import json
import sys

def update_field(filename: str, user_id: int, field: str, new_value: str):
    with open(filename, "r") as f:
        users = json.load(f)

    for user in users:
        if user["id"] == user_id:
            if field not in user:
                print(f"Field '{field}' does not exist on this user")
                return
            user[field] = new_value
            break

    with open(filename, "w") as f:
        json.dump(users, f, indent=2)
    print("Done.")


# Run from terminal:
# python update.py users.json 3 email alice@example.com
if __name__ == "__main__":
    filename  = sys.argv[1]         # users.json
    user_id   = int(sys.argv[2])    # 3
    field     = sys.argv[3]         # email
    new_value = sys.argv[4]         # alice@example.com
    update_field(filename, user_id, field, new_value)
```

Run it:
```bash
python update.py users.json 3 email alice@example.com
```

### Nested values
If you need to update a nested field (e.g., `address.city`):
```python
user["address"]["city"] = "Los Angeles"
```

---

## 5. Delete Objects from JSON

Deleting an object means filtering it out of the list, then writing the smaller list back.

### Concept
```python
# Original list
users = [{"id": 1, ...}, {"id": 2, ...}, {"id": 3, ...}]

# Keep everyone EXCEPT id=2
users = [u for u in users if u["id"] != 2]

# Now users has 2 items
```

### Example: Delete a user by ID

```python
import json

def delete_user(filename: str, user_id: int):
    with open(filename, "r") as f:
        users = json.load(f)

    original_count = len(users)

    # List comprehension — keep all users whose id is NOT the target
    users = [u for u in users if u["id"] != user_id]

    if len(users) == original_count:
        print(f"User {user_id} not found — nothing deleted")
        return

    with open(filename, "w") as f:
        json.dump(users, f, indent=2)

    print(f"Deleted user {user_id}. Remaining: {len(users)}")


delete_user("users.json", user_id=5)
```

### Example: Delete based on a field value (not just id)

```python
def delete_by_field(filename: str, field: str, value: str):
    with open(filename, "r") as f:
        users = json.load(f)

    before = len(users)
    users = [u for u in users if str(u.get(field)) != str(value)]
    after = len(users)

    with open(filename, "w") as f:
        json.dump(users, f, indent=2)

    print(f"Removed {before - after} record(s)")


# Delete all users from city "Gwenborough"
delete_by_field("users.json", field="address.city", value="Gwenborough")
```

### Delete a specific key from every object

```python
def remove_key_from_all(filename: str, key: str):
    with open(filename, "r") as f:
        users = json.load(f)

    for user in users:
        user.pop(key, None)    # pop removes the key; None avoids KeyError if missing

    with open(filename, "w") as f:
        json.dump(users, f, indent=2)

    print(f"Removed key '{key}' from all records")


remove_key_from_all("users.json", "phone")
```

---

## 6. Practice Exercises

Try these yourself using `https://jsonplaceholder.typicode.com/posts` (100 blog posts).

| # | Task |
|---|------|
| 1 | Fetch all posts and save to `posts.json` |
| 2 | Load the file and print the title of post with `id=7` |
| 3 | Change the title of post `id=7` to `"My Updated Title"` and save |
| 4 | Delete all posts where `userId == 3` and save |
| 5 | Remove the `body` key from every post and save |
| 6 | Accept `post_id` and `new_title` from the command line and update the file |

---

## Quick Reference Cheat Sheet

```python
import json, requests

# Fetch API → save file
data = requests.get(url).json()
with open("file.json", "w") as f:  json.dump(data, f, indent=2)

# Load file
with open("file.json", "r") as f:  data = json.load(f)

# Update a value
for item in data:
    if item["id"] == target_id:
        item["field"] = new_value

# Delete an object
data = [x for x in data if x["id"] != delete_id]

# Save back
with open("file.json", "w") as f:  json.dump(data, f, indent=2)
```

---

*Happy coding! Work through the exercises in order — each one builds on the last.*
