# flask
from flask import Flask, redirect, url_for, render_template, request, flash

# os
import os
from os.path import join, dirname
from dotenv import load_dotenv

# braintree
import braintree

# braintree gateway
from gateway import generate_client_token, transact, find_transaction, find_customer, find_all_customers

# routes
from routes import transaction, customer


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY')

PORT = int(os.environ.get('PORT', 4567))

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('new_checkout'))


@app.route('/checkouts/new', methods=['GET'])
def new_checkout():
    client_token = generate_client_token()
    return render_template('checkouts/new.html', client_token=client_token)


@app.route('/checkouts', methods=['POST'])
def create_checkout():

    transaction_response = transaction.create(request)

    if transaction_response["success"]:
        return redirect(url_for('show_checkout',transaction_id=transaction_response["braintree_transaction_id"]))

    else:
        flash('Error: %s: %s' % (transaction_response["error"]["error_code"], transaction_response["error"]["error_message"]))
        return redirect(url_for('new_checkout'))


@app.route('/customer', methods=['POST'])
def create_customer():

    customer_response = customer.create(request)

    print("customer_response")
    print(customer_response)

    if customer_response["success"]:
        return redirect(url_for('show_customer',customer_id=customer_response["fast_customer_id"]))
    else:
        flash('Error: %s: %s' % (customer_response["error"]["error_code"], customer_response["error"]["error_message"]))
        return redirect(url_for('new_checkout'))


@app.route('/create-child-transaction', methods=['GET'])
def create_child_transaction():

    client_token = generate_client_token()

    customers = customer.retrieve()
    customers_list = [x for x in customers]

    result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Create Parental Control Transaction.'
    }
    return render_template('checkouts/child_checkout.html', customers=customers_list, client_token=client_token, result=result)


@app.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('checkouts/show.html', transaction=transaction, result=result)


@app.route('/customer/<customer_id>', methods=['GET'])
def show_customer(customer_id):
    customer_object = customer.retrieve(customer_id)[0]
    
    result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test customer has been successfully processed.'
    }

    return render_template('customer/show.html', customer=customer_object, result=result)


@app.route('/customers', methods=['GET'])
def show_all_customers():

    customers = customer.retrieve()
    customers_list = [x for x in customers]

    message = 'Your children can be successfully viewed.' if len(customers_list)>0 else 'No children exist in the vault'
    result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': message
    }

    return render_template('customers/show.html', customers=customers_list, result=result)


@app.route('/admin-customer', methods=['get'])
def admin_customer():
    customers = find_all_customers()

    customers_list = [x for x in customers.items]
    message = 'Your children can be successfully viewed.' if len(customers_list)>0 else 'No children exist in the vault'

    result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Select the Customer ID you want to update.'
    }

    
    return render_template('customers/show.html', customers=customers, result=result)


@app.route('/update-admin-customer', methods=['GET'])
def update_admin_customer():


    customer_id = request.args["customer_id"]
    customer_object = customer.retrieve(customer_id)[0]
    customer_object = customer_object["braintree"]


    result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your customers can be successfully updated.'
    }
    return render_template('customer/update.html',customer_id=customer_id ,customer=customer_object, result=result)


@app.route('/update-stripe-braintree-customer', methods=['GET'])
def update_stripe_braintree_customer():
    print("def update_stripe_braintree_customer():")
    print("request")
    print(request)

    customer_response = customer.update(request)

    print("customer_response")
    print(customer_response)

    return redirect(url_for('show_customer', customer_id=customer_response["fast_customer_id"]))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)