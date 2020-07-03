# clients
from clients.mongodb import MongoDB

# braintree gateway
from gateway import generate_client_token, transact, find_transaction, find_customer, customer, find_all_customers

# flask
from flask import jsonify, Response

def create(customer_request):
    ''' Store customer transaction to mongo '''

    data = customer({
            "first_name": customer_request.form['first_name'],
            "last_name":  customer_request.form['last_name'],
            "custom_fields": {
                "spending_limit": customer_request.form['spending_limit']
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

        braintree_customer_id = data.customer.id
        braintree_customer_first_name = data.customer.first_name
        braintree_customer_last_name = data.customer.last_name
        braintree_customer_spending_limit = data.customer.custom_fields["spending_limit"]
        
        # open database connection
        with MongoDB() as mongo_client: # add the transaction to the collection
            customer_object = {
                "braintree":{
                    "customer_id: ": braintree_customer_id,
                    "customer_first_name: ": braintree_customer_first_name,
                    "customer_last_name: ": braintree_customer_last_name,
                    "customer_spending_limit: ": braintree_customer_spending_limit
                }
            }
            customer_object = mongo_client.customers.insert_one(customer_object)

    customer_response = {
        "fast_customer_id": None if error_dict else str(customer_object["_id"]),
        "data": {} if error_dict else data,
        "error": error_dict,
        "success": bool(not error_dict)
    }

    return customer_response
