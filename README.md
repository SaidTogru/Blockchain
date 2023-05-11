# Blockchain Network Project

## Project Overview
The main goal of this project was to transform a local blockchain class in Python into a network-capable model. This allows various devices to communicate (whether via external IP, internal IP or localhost) and fulfill the main functions of a blockchain when exchanging data. Additionally, we've focused on the creation of nodes (the participants of the network) and their initialization, methods, and functions to enable bidirectional communication.

We started by researching the P2P model, collecting and evaluating various approaches. The architecture of decentralized cryptocurrencies like Bitcoin and Ethereum became the basis of our design. We began with low-level communication through the Python modules Socket and Threading and wrote several script classes that could independently be server and client. This was facilitated by the use of two virtual machines running Ubuntu.

![Screenshot 2023-05-11 113220](https://github.com/SaidTogru/Blockchain/assets/65668541/7eb80c8a-8f4b-4e54-9e20-40b663533726)

Our model is shown in figure 1. The main issue was that we were trying to independently develop a concept where nodes could act as both a server and a client. We solved this with dynamic port distribution, but we still had to make a deep construction to ensure stable communication between all participants. We then focused more on implementing the main features of a decentralized blockchain network.

## Model
We decided to use the backend module Flask and the frontend framework Angular to manage information exchange via HTTP requests. We first created a DNS feed where all active nodes are available in JSON format. Each node has its own IP/port address and knows which nodes exist when it enters the network.

The exchange of the blockchain takes place via GET and POST request, with the site hosters communicating via the backend. When a transaction is created, for example, the transaction is created and distributed to all active nodes. Once the transaction has been validated, it is appended to a candidate block and is available to all nodes after it has been mined.

### Frontend
We used Angular for the front end. Angular is an open-source framework developed by Google based on JavaScript. Angular provides a basic framework for creating web applications and does not require additional libraries.

### Backend
The backend components are built to handle joining, transaction sending and fetching, block mining, chain validation and replacement, and balance retrieval.

### Conclusion
Programming a decentralized blockchain where multiple nodes act as participants was a significant challenge. We learned a lot about setting up a web server with Flask and the functionality of HTTP communication. We also gained experience in programming APIs. With this project, we were able to understand the basics and architecture of the blockchain.

## Getting Started

### Prerequisites
Ensure you have Python 3.x installed on your machine, installed all dependecies and Angular CLI.

### Setting Up the Backend
Open a terminal and navigate to the project's root directory.
Run the Flask backend server:

python hsrmcoin.py <port_number>

Replace <port_number> with the desired port number for the backend server.
The backend server will be accessible at http://localhost:<port_number>.

### Setting Up the Frontend
Open a new terminal and navigate to the app directory within the project's root directory.
Install the required Angular dependencies:

npm install

Start the Angular development server:
ng serve

Open a web browser and navigate to http://localhost:4200. The Angular app will be running.

### Joining the Network
Open a web browser and go to http://localhost:4200.
Click on the "Join Network" button to create an account and join the network.
Provide a username for your account.

### Interacting with the Blockchain
Once you have joined the network, you can perform the following actions:
* Sending a Transaction: Click on the "Send Transaction" button and fill in the required details (sender, receiver, amount) in the form. Click "Submit" to send the transaction.
* Mining a Block: Click on the "Mine Block" button to mine a new block and add it to the blockchain.
* Viewing the Blockchain: Click on the "View Blockchain" button to see the current state of the blockchain.
* Viewing Account Balance: Click on the "View Balance" button to see your account balance.

## Additional Information
* Cryptographic operations are performed using the Crypto module.
* Network communication and HTTP requests are handled using the Request module.
* The project utilizes Oracle VM VirtualBox to run Ubuntu virtual machines for development.
* The DNS_Feed.json file contains information about active nodes in the network.
* The private.key file stores the private key (**here for testing purposes only, NEVER RELEASE YOUR PRIVATE KEY!**) for cryptographic operations.
* The transaction.json file represents all the transactions in JSON format (basically the local blockchain that used to be synchronised with other peers in the network).

Please refer to the individual directories within the project for detailed instructions on setting up and running the different components.

License
This project is licensed under the MIT License. 
