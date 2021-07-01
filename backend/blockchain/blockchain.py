#Refer to block.py file in backend/blockchain path

from backend.blockchain.block import Block

class Blockchain:
    
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    
    # Serialize blockchain into a list of blocks
    def to_json(self): 
        serialized_chain = []
        
        for block in self.chain:
            serialized_chain.append(block.to_json())
        
        return serialized_chain

    # Deserialize a list of blocks into a blockchain instance
    # The result is a chain list of block instances
    @staticmethod
    def from_json(chain_json):
        blockchain = Blockchain()
        
        blockchain.chain = list (
            map(lambda block_json: Block.from_json(block_json), chain_json)
        )

        return blockchain

    # Validate incoming chain
    # Rules as follows: the chain must start with the genesis block, formatted correctly
    @staticmethod
    def is_valid_chain(chain):
        
        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be valid!')
        
        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)
    
    # Replace local chain with incoming one only when its longer than the local one and is formatted properly
    def replace_chain(self, chain):
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. The chain must be longer!')

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The chain must be longer!: {e} ')
        
        self.chain = chain



def main():

    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)
    print(f'blockchain.py ___name__: {__name__}')

if __name__ == '__main__':
    main()