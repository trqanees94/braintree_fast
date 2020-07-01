import os
from dotenv import load_dotenv
import braintree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=os.environ.get('BT_ENVIRONMENT'),
        merchant_id=os.environ.get('BT_MERCHANT_ID'),
        public_key=os.environ.get('BT_PUBLIC_KEY'),
        private_key=os.environ.get('BT_PRIVATE_KEY')
    )
)

def generate_client_token():
    return gateway.client_token.generate()

def transact(options):
    return gateway.transaction.sale(options)

def customer(options):
    return gateway.customer.create(options)

def find_transaction(id):
    return gateway.transaction.find(id)

def find_customer(id):
    return gateway.customer.find(id)

def find_all_customers():
    return gateway.customer.search([])