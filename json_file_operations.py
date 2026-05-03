import json
import urllib.request

# We'll use a free public API (no key needed)
# JSONPlaceholder gives fake data for practice
API_URL = "https://jsonplaceholder.typicode.com/users"

def fetch_and_save(url: str, filename: str):
    """Call an API and save the JSON response to a file."""

    # 1. Call the API
    with urllib.request.urlopen(url) as response:
        raw_data = response.read()              # bytes
        data = json.loads(raw_data)             # Python list/dict

    # 2. Write to a .json file
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)            # indent=2 makes it readable

    print(f"Saved {len(data)} records to '{filename}'")
    return data


def load_from_file(filename: str):
    """Read a JSON file back into Python."""
    with open(filename, "r") as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    # --- Step 1: Fetch from API and save ---
    users = fetch_and_save(API_URL, "users.json")

    # --- Step 2: Load the file back and use the data ---
    loaded_users = load_from_file("users.json")

    print("\nFirst user from file:")
    first = loaded_users[0]
    print(f"  Name  : {first['name']}")
    print(f"  Email : {first['email']}")
    print(f"  City  : {first['address']['city']}")
