import requests

# This is a test case for the data input API


address = "http://127.0.0.1:5000/api"

TEST_DATA = [
    {"search_term": "btc", "group": "reddit"},
    {"search_term": "btc", "subgroup": "reddit"},
    {"search_term": "btc"},
    {"search": "btc"},
    {"search_term": "bTC"},
    {"search_term": "Bitcoin"},
]

for data in TEST_DATA:
    req = requests.post(address+"/search", data=data)
    print("Status: {}\nBody:\n{}\n".format(req.status_code, req.content))