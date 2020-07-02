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
        
        # open database connection
        with MongoDB() as mongo_client: # add the transaction to the collection
            customer_object = mongo_client.customer.count()
            print("customer_object: ", customer_object)



    customer_response = {
        "data": {} if error_dict else data,
        "error": error_dict,
        "success": bool(not error_dict)
    }

    return customer_response
