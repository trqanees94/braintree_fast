import os
from dotenv import load_dotenv
import braintree
import stripe

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=os.environ.get('BT_ENVIRONMENT'),
        merchant_id=os.environ.get('BT_MERCHANT_ID'),
        public_key=os.environ.get('BT_PUBLIC_KEY'),
        private_key=os.environ.get('BT_PRIVATE_KEY')
    )
)

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

def stripe_customer(name,spending_limit):
    return stripe.Customer.create(
        name= name,
        metadata =  {
            "spending_limit": spending_limit
        }
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


