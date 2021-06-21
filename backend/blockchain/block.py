# Import time module
import time

# Refer to cyptohash.py in the Util folder
from backend.util.cryptohash import cryptohash

from backend.util.hex_to_binary import hex_to_binary

# Refer to the config.py for global values
from backend.config import MINE_RATE

# Global variable that shows all the values being used in the genesis method
GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}

class Block:
    # Components of a block
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce
    
    # Display
    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )

    @staticmethod
    # Mine a block based on last block and its data, until a block hash is found that meets the leading 0 POW requirement
    def mine_block(last_block, data):
        
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = cryptohash(timestamp, last_hash, data, difficulty, nonce)
        
        # While loop

        # While subtring 0 up to difficulty of hash string does not equal to string generated from the character 0 multiplied by difficulty
        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = cryptohash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)



    @staticmethod
    # Return the block class
    def genesis():
        
        return Block(**GENESIS_DATA)

    @staticmethod
    # Calculate adjusted difficulty according to mine rate
    # Access last blocks difficulty and timestamp
    def adjust_difficulty(last_block, new_timestamp):

        # Increase the difficulty for quickly mined blocks
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        # Decrease the difficulty for slowly mined blocks
        if (last_block.difficulty -1 ) > 0:
            return last_block.difficulty - 1
        
        # Limits decreasing to 1
        return 1
    
    @staticmethod
    # Validate block based on last hash, POW requirement, adjust difficulty by 1, block hash is valid combination of block fields
    def is_valid_block(last_block, block):
        if block.last_hash != last_block.hash:
            # Creates user error
            raise Exception('The last hash of the block must be correct!')
            
        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty: 
            raise Exception('Proof of work requirement is not met!')

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('The block difficulty must be adjusted by 1')

        reconstructed_hash = cryptohash (
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce,
        )

        if block.hash != reconstructed_hash:
            raise Exception('The block hash must be correct!')


def main():
    
    genesis_block = Block.genesis()
    invalid_block = Block.mine_block(Block.genesis(), 'Ultimate')
    invalid_block.last_hash = 'Invalid data'
    
    # Pass in the genesis block as the last block and the invalid block to validate
    
    try:
        Block.is_valid_block(genesis_block, invalid_block)
    except Exception as e:
        print(f'is_valid_block: {e}')
    
    
if __name__ == '__main__':
    main()