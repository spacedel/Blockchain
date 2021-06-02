from backend.blockchain.block import Block
# Import time module
import time

# Refer to backend/blockchain/blockchain.py for the Blockchain class
from backend.blockchain.blockchain import Blockchain

# Refer to backend/config for Global values
from backend.config import SECONDS

blockchain = Blockchain()

# Empty list
times = []


for i in range(1000):
    start_time = time.time_ns()
    # Add block to make unique data attr 
    blockchain.add_block(i)
    
    # Calculate time to mine block
    end_time = time.time_ns()

    time_to_mine = (end_time - start_time) / SECONDS
    times.append(time_to_mine)
    
    # Sum of times list divided by the length of times list
    averagetime = sum(times) / len(times)

    # Print information
    print(f'New Block Difficulty: {blockchain.chain[-1].difficulty}')
    print(f'Time to Mine New Block: {time_to_mine}s')
    print(f'Average Time to Add Blocks: {averagetime}s\n')
