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

def update_stripe_customer(customer_id,name,spending_limit):
    return stripe.Customer.modify(
        customer_id,
        name=name,
        metadata =  {
            "spending_limit": spending_limit
        }
    )


def stripe_charge(amount):
    return stripe.Charge.create(
        amount=2000,
        currency="usd",
    )


def generate_client_token():
    return gateway.client_token.generate()

def transact(options):
    return gateway.transaction.sale(options)

def customer(options):
    return gateway.customer.create(options)

def update_customer(customer_id, params):
    return gateway.customer.update(customer_id, params)


def find_transaction(id):
    return gateway.transaction.find(id)

def find_customer(id):
    return gateway.customer.find(id)

def find_all_customers():
    return gateway.customer.search([])


