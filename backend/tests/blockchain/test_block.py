from backend.blockchain.block import Block, GENESIS_DATA



def mine_test_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)

    # first arguement is the object i want to test that is an instance of something
    # second is class what would match it
    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash

# This tests that every attr in the genesis block instance matches the items in the GENESIS_DATA variable
def test_genesis():
    
    genesis = Block.genesis()

    #the genesis variable and the Block class as arguments
    assert isinstance(genesis, Block)

    GENESIS_DATA.items()
    
    #Same attr key is the same value as the values within the GENESIS_DATA global variable
    for key, value in GENESIS_DATA.items():
        getattr(genesis, key) == value
