# clients
# from clients.mongodb import MongoDB

# braintree gateway
from gateway import transact, find_customer

# flask
from flask import jsonify, Response


def create(transaction_request):
    ''' Store customer transaction to mongo '''

    customer_object = find_customer(transaction_request.form['customer_id'])
    
    print("def create(transaction_request)")
    print(customer_object)
    print("********************************** custom_fields **********************************")
    print(customer_object.custom_fields)
    customer_spending_limit = customer_object.custom_fields["spending_limit"]

    print("transaction_request.form['amount']")
    print(transaction_request.form['amount'])
    print(type(transaction_request.form['amount']))

    print("customer_spending_limit")
    print(customer_spending_limit)
    print(type(customer_spending_limit))


    if float(transaction_request.form['amount']) > float(customer_spending_limit):
        error_dict = {
            "error_message": "Transaction Amount Exceeds Limit", 
            "error_code": "415",
            "spending_limit": customer_spending_limit, 
            "transaction_amount": transaction_request.form['amount']
            }
    else:
        error_dict = {}

    print("error_dict")
    print(error_dict)

    if not error_dict:
        data = transact({
            'amount': transaction_request.form['amount'],
            'payment_method_nonce': transaction_request.form['payment_method_nonce'],
            'options': {
                "submit_for_settlement": True
            }
        })
    
    

    transaction_response = {
        "data": {} if error_dict else data,
        "error": error_dict,
        "success": bool(not error_dict)
    }

    print("transaction_response")
    print(transaction_response)

    return transaction_response
    # return jsonify(
    # {
    #     "data": {} if error_dict else data,
    #     "error": error_dict,
    #     "success": bool(not error_dict)
    # })
