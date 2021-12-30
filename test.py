import requests
import re
from flask import Flask, jsonify, request


from urllib.parse import urlencode
from urllib.request import Request, urlopen

url = "http://127.0.0.1:5000/api/fetch_transaction"  # Set destination URL here
post_fields = {"foo": "bar"}  # Set POST fields here

request = Request(url, urlencode(post_fields).encode())
json = urlopen(request).read().decode()
print(json)
print("opfer")
