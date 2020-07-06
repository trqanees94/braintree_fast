#bson
from bson import ObjectId

# clients
from clients.mongodb import MongoDB

# braintree/ stripes gateway
from gateway import generate_client_token, transact, find_transaction, find_customer, customer, update_customer ,find_all_customers, \
                    stripe_customer, update_stripe_customer

# flask
from flask import jsonify, Response

def create(customer_request):
    ''' 
    Input:customer_request (request.form)
    '''

    # customer() uses braintree gateway to create a customer
    braintree_data = customer({
            "first_name": customer_request.form['first_name'],
            "last_name":  customer_request.form['last_name'],
            "custom_fields": {
                "spending_limit": customer_request.form['spending_limit'] if customer_request.form['spending_limit'] else 0
            }
        })

    # stripe_customer() uses stripe gateway to create a customer
    stripe_data = stripe_customer(
            "{} {}".format(customer_request.form['first_name'], customer_request.form['last_name']),
            customer_request.form['spending_limit'] if customer_request.form['spending_limit'] else 0
        )


    if not braintree_data.is_success:
        errors_list = [[x.code, x.message] for x in braintree_data.errors.deep_errors]
        error_dict = {
            "error_message": errors_list[0][1], 
            "error_code": errors_list[0][0]
            }
    else:
        error_dict = {}

        # customer_pair makes up the Fast Customer record
        customer_pair = {
            "braintree":{
                        "customer_id": braintree_data.customer.id,
                        "customer_first_name": braintree_data.customer.first_name,
                        "customer_last_name": braintree_data.customer.last_name,
                        "customer_spending_limit": braintree_data.customer.custom_fields["spending_limit"]
                    },
            "stripe":{
                        "customer_id": stripe_data.id,
                        "customer_first_name": stripe_data.name,
                        "customer_last_name": stripe_data.name,
                        "customer_spending_limit": stripe_data.metadata.spending_limit
            }
        }
        
        # open database connection
        with MongoDB() as mongo_client: 
            # add the customer to the customers collection
            customer_object = mongo_client.customers.insert_one(customer_pair)

    customer_response = {
        "fast_customer_id": None if error_dict else str(customer_object["_id"]),
        "braintree_id": {} if error_dict else braintree_data.customer.id,
        "stripe_id": {} if error_dict else stripe_data.id,
        "error": error_dict,
        "success": bool(not error_dict)
    }

    return customer_response


def update(customer_request):
    ''' 
    Input: customer_request -(request.args)
    '''
    # fast_customer_id is sent from the update html page
    fast_customer_id = customer_request.args["customer_id"]

    updated_first_name=customer_request.args["first_name"]
    updated_last_name=customer_request.args["last_name"]
    updated_spending_limit=customer_request.args["spending_limit"]

    with MongoDB() as mongo_client:
        # customer_object contains the braintree and stripe customer pair
        customer_object = mongo_client.customers.find_by_id(fast_customer_id)
        braintree_id = customer_object['braintree']['customer_id']
        stripe_id = customer_object['stripe']['customer_id']

    #update_params creates the payload that has updated customer data
    update_params = {
                "first_name": updated_first_name,
                "last_name": updated_last_name,
                "custom_fields": {
                    "spending_limit": updated_spending_limit
                }
            }

    # update_customer() uses the braintree gateway to update customer
    braintree_data = update_customer(braintree_id, update_params)

    # update_stripe_customer() uses the stripe gateway to update customer
    stripe_data = update_stripe_customer(
            stripe_id,
            "{} {}".format(customer_request.args['first_name'], customer_request.args['last_name']),
            customer_request.args['spending_limit']
        )

    # New customer data must be updated in the MongoDB customers collection
    with MongoDB() as mongo_client:
        mongo_client.customers.collection.update_one(
            {"_id": ObjectId(fast_customer_id)},
            {"$set": {
                "braintree":{
                    "customer_id":braintree_id,
                    "customer_first_name": updated_first_name,
                    "customer_last_name": updated_last_name,
                    "customer_spending_limit": updated_spending_limit
                },
                "stripe":{
                    "customer_id":stripe_id,
                    "customer_first_name": "{} {}".format(updated_first_name,updated_last_name),
                    "customer_last_name": "{} {}".format(updated_first_name,updated_last_name),
                    "customer_spending_limit": updated_spending_limit
                }
            }}
        )

    if not braintree_data.is_success:
        errors_list = [[x.code, x.message] for x in braintree_data.errors.deep_errors]
        error_dict = {
            "error_message": errors_list[0][1], 
            "error_code": errors_list[0][0]
            }
    else:
        error_dict = {}

    customer_response = {
        "fast_customer_id": None if error_dict else str(customer_object["_id"]),
        "braintree_id": {} if error_dict else braintree_data.customer.id,
        "stripe_id": {} if error_dict else stripe_data.id,
        "error": error_dict,
        "success": bool(not error_dict)
    }

    return customer_response


def retrieve(mongoid=None):
    
    if mongoid:
        with MongoDB() as mongo_client: 
            # pull single customer from mongodb customers collection
            customer_object_list = [mongo_client.customers.find_by_id(mongoid)]
    else:
        with MongoDB() as mongo_client:
            # pull all customers from mongodb customers collection
            customer_object_list = mongo_client.customers.find()

    return customer_object_list
