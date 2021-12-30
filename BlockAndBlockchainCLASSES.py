from datetime import datetime
from hashlib import sha256
# print current date and time
#BLATT ALLE
print(datetime.now())
class Block:
    
 def __init__(self, transactions, previous_hash, nonce = 0):
     self.timestamp = datetime.now()
     self.transactions = transactions
     self.previous_hash = previous_hash
     self.nonce = nonce
     self.hash = self.generate_hash()

 def print_block(self):
     print("timestamp:", self.timestamp)
     print("transactions:", self.transactions)
     print("current hash:", self.generate_hash())

 def generate_hash(self):
     block_contents = str(self.timestamp) + str(self.transactions) + str(self.nonce) + str(self.previous_hash)
     block_hash = sha256(block_contents.encode())
     return block_hash.hexdigest()
     
class Blockchain:
    def __init__(self):
        self.chain = []
        self.all_transactions = []
        self.genesis_block()
         
    def genesis_block(self):
        transactions = {}
        genesis_block = Block(transactions, "0")
        self.chain.append(genesis_block)
        return self.chain

    def print_blocks(self):
        for i in range(len(self.chain)):
            current_block = self.chain[i]
            print("Block {} {}".format(i, current_block))
            current_block.print_block()
    
    def add_block(self, transactions):
         previous_block_hash = self.chain[len(self.chain)-1].hash
         new_block = Block(transactions, previous_block_hash)
         # modify this method
         proof = self.proof_of_work(new_block)
         self.chain.append(new_block)
         return proof, new_block 
         
    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.generate_hash():
                return False
            if current.previous_hash != previous.generate_hash():
                return False
            return True
            
    def proof_of_work(self,block, difficulty=2):
        proof = block.generate_hash()
        while proof[:difficulty] != '0' * difficulty:
            block.nonce += 1
            proof = block.generate_hash()
        block.nonce = 0
        return proof
     
if __name__=="__main__":
    newBlock=Block([1,2,3,4,5],"dkansdpvcß23r")
    newBlock.print_block()
    new_transactions = [{'amount': '30', 'sender':'alice', 'receiver':'bob'},{'amount': '55', 'sender':'bob', 'receiver':'alice'}]
    my_blockchain = Blockchain()
    my_blockchain.add_block(new_transactions)
    my_blockchain.print_blocks()
    my_blockchain.chain[1].transactions = "fake_transactions"
    print(my_blockchain.validate_chain())