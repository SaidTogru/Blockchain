import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse
from flask_cors import CORS
import base64
from Crypto import Random
from Crypto.PublicKey import RSA
import os
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import sys
from base64 import b64decode
import ast

# First Argument Username Second Port

if len(sys.argv) < 2:
    print("Please read the docs")
    sys.exit(1)


class Blockchain:
    activeNodes = []
    transactions = []

    def __init__(self, username):
        self.chain = []
        self.mempool = []
        self.unconfirmed_transactions = []
        self.create_block(proof=0, previous_hash="0")  # GENESIS BLOCK
        self.create_account()  # CREATE PUBLIC AND PRIVATE KEY
        self.username = username
        self.connect()  # CONNECTING TO NETWORK
        self.startbalance = 100.00

    def create_account(self):
        if os.path.isfile("private.key"):
            with open("private.key", "rb") as content_file:
                self.privatekey = content_file.read()
                self.privatekey = RSA.importKey(self.privatekey)
            self.publickey = self.privatekey.publickey()
        else:
            self.privatekey = RSA.generate(2048)
            with open("private.key", "wb") as content_file:
                content_file.write(self.privatekey.exportKey("PEM"))
            self.publickey = self.privatekey.publickey()

    def connect(self):  # Peer Discovery
        ip = requests.get("https://api.ipify.org").content.decode("utf8")
        with open("DNS_Feed.json") as json_file:
            data = json.load(json_file)
            for name, address in data.items():
                if (
                    address[0][address[0].find("http://") + 7 : address[0].find(":50")]
                    == ip
                ):
                    if address[1].split(":")[-1] != sys.argv[1]:
                        self.activeNodes.append(address[1])
                else:
                    self.activeNodes.append(address[0])

    def broadcast_transaction(self, transaction):
        sendTo = []
        validators = []
        valid = False
        for node in self.activeNodes:
            try:
                re = requests.post(
                    f"{node}/api/fetch_transaction",
                    json=transaction,
                    headers={"content-type": "application/json"},
                )
                response = json.loads(re.text)
                valid = response["valid"]  # 0 or 1
                validators.append(response["username"])
                sendTo.append(node)
            except Exception as e:
                print(
                    f"Post request to {node} raised a Error. Probably the site is down!"
                )
                pass
        return str(sendTo), valid, validators

    def fetch_transaction(self, transaction):
        sender = transaction["sender"]
        receiver = transaction["receiver"]
        amount = transaction["amount"]
        newdata = {"sender": sender, "receiver": receiver, "amount": amount}
        if self.validate_transaction(
            newdata, transaction["publickey"], transaction["signature"], amount
        ):
            self.add_transaction(sender, receiver, amount)
            return True
        else:
            return False

    def validate_transaction(self, data, publickey, signature, amount):
        if (
            self.validate_signature(data, publickey, signature)
            and self.get_balance() >= amount
        ):
            return True
        else:
            return False

    def remove_double_backslashes(self, b):
        return ast.literal_eval(str(b).replace("\\\\", "\\"))

    def validate_signature(self, data, publickey, signature):
        message = json.dumps(data, indent=2).encode("utf-8")
        h = SHA256.new(message)
        # signature = self.remove_double_backslashes(signature[2:-1]).encode("utf-8")
        try:
            key64 = (
                publickey.replace("\\n", "")
                .replace("-----BEGIN PUBLIC KEY-----", "")
                .replace("-----END PUBLIC KEY-----", "")
                .strip()
            )[2:-1]
            keyDER = b64decode(key64)
            publickey = RSA.importKey(keyDER)
            pkcs1_15.new(publickey).verify(h, signature)
            return False
        except Exception as e:
            print(e)
            return True

    def get_balance(self):
        balance = self.startbalance
        blockchain = self.chain

        for block in blockchain:
            for transaction in block["transactions"]:
                if transaction:
                    if transaction["receiver"] == self.username:
                        balance += float(transaction["amount"])
                        self.startbalance += float(transaction["amount"])
                    elif transaction["sender"] == self.username:
                        balance -= float(transaction["amount"])
                        self.startbalance -= float(transaction["amount"])
        return balance

    def generate_signature(self, data):
        # PKCS#1 v1.5 (RSA): private RSA key (loaded from a file) used to compute the signature of a message:
        message = json.dumps(data, indent=2).encode("utf-8")
        h = SHA256.new(message)
        signature = pkcs1_15.new(self.privatekey).sign(h)
        print("GENERATE")
        print(signature)
        return str(signature)

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append(
            {"sender": sender, "receiver": receiver, "amount": amount}
        )
        previous_block = self.get_previous_block()
        return previous_block["index"] + 1

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
            "transactions": self.mempool,
        }
        self.mempool = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()
            ).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def valid_chain(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(
                str(proof ** 2 - previous_proof ** 2).encode()
            ).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True

    def replace_chain(self):
        longest_chain = None
        max_length = len(self.chain)
        for node in self.activeNodes:
            response = requests.get(f"{node}/api/get_chain")
            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


blockchain = None
joined = False
excep = f"Before you can operate anything you must join the network"


@app.route("/api/join", methods=["POST", "GET"])
def join():
    global blockchain, joined
    json_data = request.get_json()
    username = json_data["username"] if json_data is not None else "Default"
    blockchain = Blockchain(username)
    joined = True
    response = {
        "message": f"{blockchain.username}, thank you for joining the HSRM Network. You successfully created an Account and can participate!"
    }
    return jsonify(response), 200


@app.route("/api/connected", methods=["GET"])  # CHECK IF CONNECTED
def connected():
    if not joined:
        return jsonify(), 400
    else:
        return jsonify(), 200


@app.route("/api/get_keys", methods=["GET"])  # CHECK IF CONNECTED
def get_keys():
    if not joined:
        return jsonify(excep), 400
    else:
        return (
            jsonify(
                {
                    "publickey": str(blockchain.publickey.export_key()),
                    "privatekey": str(blockchain.privatekey.export_key()),
                }
            ),
            200,
        )


@app.route("/api/show_network", methods=["GET"])
def show_network():
    if not joined:
        return jsonify(excep), 400
    if len(blockchain.activeNodes) == 0:
        return jsonify("There are no peers in the network"), 200
    else:
        return jsonify(f"Currently on the network: {blockchain.activeNodes}"), 200


@app.route("/api/send_transaction", methods=["POST"])
def send_transaction():
    if not joined:
        return jsonify(excep), 400
    json_data = request.get_json()
    transaction_keys = ["sender", "receiver", "amount"]
    if not all(key in json_data for key in transaction_keys):
        return "Some elements of the transaction are missing", 400
    json_data["signature"] = blockchain.generate_signature(json_data)
    json_data["publickey"] = str(blockchain.publickey.export_key())
    # sender,receiver,amount,signature,publickey
    receivers, valid, validators = blockchain.broadcast_transaction(json_data)
    valid = bool(valid)
    if len(receivers) < 3:
        response = {
            "message": "Unfortunately, there are no active nodes to send the transaction to"
        }
        return jsonify(response), 200
    else:
        response = {"valid": valid, "validators": validators}
        return jsonify(response), 200


@app.route("/api/fetch_transaction", methods=["POST"])
def fetch_transaction():
    if not joined:
        return jsonify(excep), 400
    json_data = request.get_json(force=True)
    transaction_keys = ["sender", "receiver", "amount", "signature", "publickey"]
    if not all(key in json_data for key in transaction_keys):
        return "Some elements of the transaction are missing", 400
    valid = blockchain.fetch_transaction(json_data)
    response = (
        {"valid": 1, "username": blockchain.username}
        if valid
        else {"valid": 0, "username": blockchain.username}
    )
    return jsonify(response), 200


@app.route("/api/mine_block", methods=["GET"])
def mine_block():
    if not joined:
        return jsonify(excep), 400
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    # blockchain.add_transaction(sender=blockchain.username, receiver=, amount=1)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        "message": "Congrats, you just mined a block!",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
        "transactions": block["transactions"],
    }
    return jsonify(response), 200


@app.route("/api/valid_chain", methods=["GET"])
def valid_chain():
    if not joined:
        return jsonify(excep), 400
    is_valid = blockchain.valid_chain(blockchain.chain)
    if is_valid:
        response = {"message": "All good. The Blockchain is valid."}
    else:
        response = {"message": "The Blockchain is not valid!"}

    return jsonify(response), 200


@app.route("/api/get_chain", methods=["GET"])
def get_chain():
    if not joined:
        return jsonify(excep), 400
    response = {"chain": blockchain.chain, "length": len(blockchain.chain)}
    return jsonify(response), 200


@app.route("/api/replace_chain", methods=["GET"])
def replace_chain():
    if not joined:
        return jsonify(excep), 400
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {
            "message": "The nodes had different chains so the chain was replaced by the longest one",
            "new_chain": blockchain.chain,
        }
    else:
        response = {
            "message": "All good. The chain is the largest one.",
            "actual_chain": blockchain.chain,
        }
    return jsonify(response), 200


@app.route("/api/get_balance", methods=["POST"])
def get_balance():
    if not joined:
        return jsonify(excep), 400
    json = request.get_json()
    username = json.get("username")
    balance = blockchain.get_balance(username)
    response = {"message": f"Your balance is {balance} HSRM Coins"}
    return jsonify(response), 200


app.run(host="0.0.0.0", port=sys.argv[1])
