import uuid
import time
from backend.wallet.wallet import Wallet

# Document exchange in currency from 1 to 1, or 1 to many recipients. 
class Transaction:

    def __init__(self, sender_wallet, recipient, amount):
        self.id = str(uuid.uuid4()) [0:8]
        self.output = self.create_output(
            sender_wallet,
            recipient,
            amount
        )

        self.input = self.create_input(sender_wallet, self.output)
    
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

def main():
    # Transaction instance, and needs to be a wallet class represents sender, a str address for the second wallet and value(any). 
    transaction = Transaction(Wallet(), 'recipient', 50)
    print(f'transaction.__dict: {transaction.__dict__}')

if __name__ == '__main__':
    main()