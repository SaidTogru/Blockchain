import requests
from flask import Flask, jsonify, request

url = "http://localhost:5000/api/fetch_transaction"
payload = {"sender": "", "receiver": "", "amount": 10, "signature": 1, "publickey": 2}

x = requests.post(url, json=payload, headers={"Content-Type": "text/plain"})

print(x.text)
