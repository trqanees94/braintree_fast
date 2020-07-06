# clients
from clients.mongodb import MongoDB

# braintree gateway
from gateway import transact, find_customer

# flask
from flask import jsonify, Response


def create(transaction_request):
    ''' Store customer transaction to mongo '''


    fast_customer_id = transaction_request.form["customer_id"]

    with MongoDB() as mongo_client:
        fast_customer_object = mongo_client.customers.find_by_id(fast_customer_id)


    
    customer_object = find_customer(fast_customer_object['braintree']['customer_id'])
    customer_spending_limit = fast_customer_object['braintree']["customer_spending_limit"]

    if float(transaction_request.form['amount']) > float(customer_spending_limit):
        error_dict = {
            "error_message": "Transaction Amount: {} Exceeds Limit: {}".format(transaction_request.form['amount'], customer_spending_limit),
            "error_code": "415"
            }
    
    else: 
        data = transact({
            'amount': transaction_request.form['amount'],
            'payment_method_nonce': transaction_request.form['payment_method_nonce'],
            'options': {
                "submit_for_settlement": True
            }
        })

        if not data.is_success:
            errors_list = [[x.code, x.message] for x in data.errors.deep_errors]
            error_dict = {
                "error_message": errors_list[0][1], 
                "error_code": errors_list[0][0]
                }

        else:
            error_dict = {}
            braintree_transaction_id = data.transaction.id
            braintree_transaction_amount = float(data.transaction.amount)

            # open database connection
            with MongoDB() as mongo_client: # add the transaction to the collection
                transaction_pair = {
                    "braintree":{
                        "braintree_transaction_id":braintree_transaction_id,
                        "braintree_transaction_amount":braintree_transaction_amount
                    },
                    "stripe":{

                    }
                }
            transaction_object = mongo_client.transactions.insert_one(transaction_pair)
    

    transaction_response = {
        "fast_transaction_id": None if error_dict else str(transaction_object["_id"]),
        "braintree_transaction_id": {} if error_dict else data.transaction.id,
        "error": error_dict,
        "success": bool(not error_dict)
    }

    return transaction_response
