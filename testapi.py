import requests

BASE_URL = "http://127.0.0.1:8000"


def print_response(response):
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(response.json())
    print("-" * 50)


# Home
print("GET /")
response = requests.get(f"{BASE_URL}/")
print_response(response)


# All items
print("GET /items")
response = requests.get(f"{BASE_URL}/items")
print_response(response)


# Limit
print("GET /items?limit=2")
response = requests.get(
    f"{BASE_URL}/items",
    params={"limit": 2}
)
print_response(response)


# Category filter
print("GET /items?category=Safety")
response = requests.get(
    f"{BASE_URL}/items",
    params={"category": "Safety"}
)
print_response(response)


# Category + Limit
print("GET /items?category=Safety&limit=1")
response = requests.get(
    f"{BASE_URL}/items",
    params={
        "category": "Safety",
        "limit": 1
    }
)
print_response(response)


# Item by id
print("GET /items/1")
response = requests.get(f"{BASE_URL}/items/1")
print_response(response)


# Not found
print("GET /items/999")
response = requests.get(f"{BASE_URL}/items/999")
print_response(response)