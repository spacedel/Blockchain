import os
import random

import requests

from flask import Flask, jsonify

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
pubsub = PubSub(blockchain)

# Flask end points
@app.route('/')
def route_default():
    return 'The BLOCKCHAIN'

@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = 'mock_transaction_data'
    
    blockchain.add_block(transaction_data)
    
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)

    return jsonify(block.to_json())

# Set Port
ROOT_PORT = 5000
PORT = ROOT_PORT

# Peer instance listening on any PORT between 5001 and 6000
if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)

    result = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    print(f'result.json(): {result.json()}')

    result_blockchain = Blockchain.from_json(result.json())
    
    try:
        blockchain.replace_chain(result_blockchain.chain)
        print('\n -- Successfully synchronized the local chain')
    except Exception as e:
        print(f'\n -- Error synchronizing: {e}')
app.run(port = PORT)
