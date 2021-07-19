import uuid
import time
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD, MINING_REWARD_INPUT

# Document exchange in currency from 1 to 1, or 1 to many recipients. 
class Transaction:

    def __init__(
        self, 
        sender_wallet = None, 
        recipient = None, 
        amount = None, 
        id = None, 
        output = None, 
        input = None
    ):
        self.id = id or str(uuid.uuid4()) [0:8]
        self.output = output or self.create_output(
            sender_wallet,
            recipient,
            amount
        )

        self.input = input or self.create_input(sender_wallet, self.output)
    
    # Structure of the output data for the transaction.
    def create_output(self, sender_wallet, recipient, amount):
        
        if amount > sender_wallet.balance:
            raise Exception('Amount exceeds balance!')

        output = {}
        output[recipient] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount

        return output

    # Structure of input data for the transaction
    # Sign the transaction and include the sender's public key & address.
    def create_input(self, sender_wallet, output):
        return {
            'timestamp': time.time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output)
        }

    # Update transaction or new sender
    def update(self, sender_wallet, recipient, amount):
        
        if amount > self.output[sender_wallet.address]:
            raise Exception('Amount exceeds balance!')
        
        if recipient in self.output: 
            self.output[recipient] = self.output[recipient] + amount
        else:
            self.output[recipient] = amount

        self.output[sender_wallet.address] = \
            self.output[sender_wallet.address] - amount

        self.input = self.create_input(sender_wallet, self.output)

    # Serialized transaction
    def to_json(self):
        return self.__dict__

    # Deserialized transaction json representation back into a Transaction instance
    @staticmethod
    def from_json(transaction_json):
        return Transaction(**transaction_json)


    # Validate a transaction and raise exception if there is an error / invalid transaction.
    @staticmethod
    def is_valid_transaction(transaction):
        output_total = sum(transaction.output.values())

        # Validate the reward transaction given
        if transaction.input == MINING_REWARD_INPUT:
            if list(transaction.output.values()) != [MINING_REWARD]:
                raise Exception('Invalid mining reward')
            return  


        if transaction.input['amount'] != output_total:
            raise Exception('Invalid transaction output values!')

        # Verify with public key and signature
        if not Wallet.verify(
            transaction.input['public_key'],
            transaction.output,
            transaction.input['signature'],
        ):

            raise Exception('Invalid signature!')

    # Generate a rewards transaction that awards the miner
    @staticmethod
    def reward_transaction(miner_wallet):
        output = {}
        output[miner_wallet.address] = MINING_REWARD

        return Transaction(input=MINING_REWARD_INPUT, output=output )


        


def main():
    # Transaction instance, and needs to be a wallet. Class represents sender, a str address for the second wallet and value = (any). 
    transaction = Transaction(Wallet(), 'recipient', 50)
    print(f'transaction.__dict: {transaction.__dict__}')

    transaction_json = transaction.to_json()
    restored_transaction = Transaction.from_json(transaction_json)
    print(f'restored_transaction: {restored_transaction.__dict__}')

if __name__ == '__main__':
    main()