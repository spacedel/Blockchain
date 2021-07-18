import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration

from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction

pn_config = PNConfiguration()
pn_config.subscribe_key = 'sub-c-685a65da-d5d5-11eb-92a6-1ab188f49893'
pn_config.publish_key = 'pub-c-fd8c5fe9-c5c0-435a-b124-4d5be8370db9'

pubnub = PubNub(pn_config)

# List of channels to run
CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK',
    'TRANSACTION': 'TRANSACTION'
}


# Network request in the background
pubnub.subscribe().channels(CHANNELS.values()).execute()

class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_object):
        print (f'\n-- Channel: {message_object.channel} | Message: {message_object.message}' )

        # Send message to node about replaced chain
        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                self.transaction_pool.clear_blockchain_transactions(
                    self.blockchain
                )
                print('\n -- Successfully replaced the local chain')
            except Exception as e:
                print(f'\n -- Did not replace chain: {e}')
        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print(f'\n -- Set the new transaction in the transaction pool...CHECKMARK!')



# Handles the publish/subcribe of the application
# Communication between nodes of blockchain network
class PubSub():
    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(pn_config)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    # Publish the message object to channel
    def publish(self, channel, message):
        self.pubnub.publish().channel(channel).message(message).sync()

    # Broadcast block object to all nodes
    def broadcast_block(self, block):
      self.publish(CHANNELS['BLOCK'], block.to_json())  

    # Broadcast transactions to all nodes
    def broadcast_transaction(self, transaction):
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json()) 


# Message in listener is shown when the subscribed channel completes the request. 
# Time delay of 1 before its published.
def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'], {'foo': 'bar'})

    
if __name__ == '__main__':
    main()

