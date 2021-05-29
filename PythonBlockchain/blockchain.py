class Block:
    def __init__(self, data):
        self.data = data
    
    def __repr__(self):
        return f'Block - data: {self.data}'
        


class Blockchain:
    
    def __init__(self):
        self.chain = []

    def add_block(self, data):
        self.chain.append(Block(data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'
        

blockchain= Blockchain()
blockchain.add_block('one')
blockchain.add_block('two')

print(blockchain)