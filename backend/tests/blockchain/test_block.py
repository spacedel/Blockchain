# Import time module
import time

# Refer to backend/blockchain/bolock.py for Block class and GENESIS DATA
from backend.blockchain.block import Block, GENESIS_DATA
from backend.config import MINE_RATE, SECONDS


def mine_test_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)

    # first arguement is the object i want to test that is an instance of something
    # second is class what would match it
    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert block.hash[0:block.difficulty] == '0' * block.difficulty 

# This tests that every attr in the genesis block instance matches the items in the GENESIS_DATA variable
def test_genesis():
    
    genesis = Block.genesis()

    #the genesis variable and the Block class as arguments
    assert isinstance(genesis, Block)

    GENESIS_DATA.items()
    
    #Same attr key is the same value as the values within the GENESIS_DATA global variable
    for key, value in GENESIS_DATA.items():
        getattr(genesis, key) == value

def test_quickly_mine_block():
    last_block = Block.mine_block(Block.genesis(), 'Ultimate')
    mined_block = Block.mine_block(last_block, 'Rich')

    assert mined_block.difficulty == last_block.difficulty + 1

def test_slowly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'Ultimate')
    time.sleep(MINE_RATE / SECONDS )
    mined_block = Block.mine_block(last_block, 'Rich')

    assert mined_block.difficulty == last_block.difficulty -  1

def test_mined_block_difficulty_limit_1():
    last_block = Block(
        time.time_ns(),
        'test-last_hash',
        'test-hash',
        'test-data',
        1,
        0
    )
    time.sleep(MINE_RATE / SECONDS)

    mined_block = Block.mine_block(last_block, 'Rich')
    assert mined_block.difficulty == 1



