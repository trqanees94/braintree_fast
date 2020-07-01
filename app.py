from flask import Flask, redirect, url_for, render_template, request, flash

import os
from os.path import join, dirname
from dotenv import load_dotenv
import braintree
from gateway import generate_client_token, transact, find_transaction, find_customer, customer, find_all_customers

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


@app.route('/checkouts', methods=['POST'])
def create_checkout():
    result = transact({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        return redirect(url_for('show_checkout',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('new_checkout'))


@app.route('/customer/<customer_id>', methods=['GET'])
def show_customer(customer_id):
    customer = find_customer(customer_id)
    # result = {}
    
    result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test customer has been successfully processed.'
    }

    return render_template('customer/show.html', customer=customer, result=result)


@app.route('/customers', methods=['GET'])
def show_all_customers():
    customers = find_all_customers()

    customers_list = [x for x in customers.items]
    message = 'Your children can be successfully viewed.' if len(customers_list)>0 else 'No children exist in the vault'

    result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': message
    }

    return render_template('customers/show.html', customers=customers, result=result)


@app.route('/customer', methods=['POST'])
def create_customer():
    result = customer({
        "first_name": request.form['first_name'],
        "last_name":  request.form['last_name'],
        # 'options': {
        #     "fail_on_duplicate_payment_method": True
        # }
    })

    if result.is_success or result.customer.id:
        return redirect(url_for('show_customer',customer_id=result.customer.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('new_checkout'))

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


@app.route('/update-admin-customer', methods=['POST'])
def update_admin_customer():

    customer_id = request.form['customer_id']
    print("customer_id:")
    print(customer_id)
    customer_object = find_customer(customer_id)
    print(customer_object)

    result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your customers can be successfully updated.'
    }

    return render_template('customer/update.html', result=result ,customer=customer_object)



@app.route('/create-child-transaction', methods=['GET'])
def create_child_transaction():

    customers = find_all_customers()
    print("---------------------------")
    print(customers)
    print("---------------------------")
    customers_list = [x.id for x in customers.items]
    customers_collection_list = [x for x in customers.items]
    print(customers_list)
    print("---------------------------")
    print(customers_collection_list)
    print("---------------------------")


    result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Create Parental Control Transaction.'
    }
    return render_template('checkouts/child_checkout.html', customers=customers_list, result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)





# <form id="update-admin-customer-form" method="post" action="/update_admin_customer">
#               <input type="hidden" name="customer_id" value='{{ customer.id }}'>
#             </form>
# <input type="hidden" name="customer_id" value='{{ customer.id }}'>
# <tr onclick="document.getElementById('update-admin-customer-form').submit();"></tr>



# <script>
#   $(document).ready(function(){
#     // code to read selected table row cell data (values).
#     $("#myTable").on('click','.btnSelect',function(){
#         // get the current row
#         var currentRow=$(this).closest("tr"); 
        
#         var col1=currentRow.find("td:eq(0)").text(); // get current row 1st TD value
#         var col2=currentRow.find("td:eq(1)").text(); // get current row 2nd TD
#         var col3=currentRow.find("td:eq(2)").text(); // get current row 3rd TD
#         var data=col1+"\n"+col2+"\n"+col3;
        
#         alert(data);
#     });
#   });
# </script>

# tr onclick="myFunction(this)">