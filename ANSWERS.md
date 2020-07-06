#### What were the most difficult tasks?

1. Developing a uniform method of communication between the client and server that kept a standard URI convention. The transmission of data between the client and server was split between the following methods:
	1. In some cases I needed a synchronous approach that reloads the page in which case <strong> form submission</strong> was the right option. 
	2. However in other cases I needed an asynchronous appraoch to perform backend code without reloading the page in which case <strong> AJAX </strong> was the right option.

Using one approach would allow the REST API to expect only URL params or only data params. If this was a microservice that had no front-end interface and only communicated with adjacent microservices, the URI structure design would have been easier.


2. Writing reusable code
	1. Adding features down the road can be a difficult task when writing non robust methods. 
		1. The clients/mongodb.py is built in a robust way since developers can toggle between the <strong>customers</strong> and <strong>transactions</strong> Mongo Collection using the dot operator(<strong>.</strong>)
			1. If a developer wants to Insert/Update/Find a record in a new MongoDB collection they will only add a single line of code








#### Did you learn anything new while completing this assignment?

1. I became more familiar with the client-server relationship. Essentially when creating a Flask Micro Service with a front end, the data sent from client to server can cause the API URI to be unorganized. Its important to stick with one form of Client Server Interaction such as <strong>< forms></strong> and  <strong>Ajax</strong>


2. I learned the payment token nonce method of transmitting data on Stripe and Braintree. I have always relied on 3rd party encryption library to securely transmit credit card data. However the generate_client_token() API call provided by Braintree made it much simpler to create transactions 






#### What did you not have time to add? What work took the up majority of your time?

##### What did you not have time to add?
##### Features 
1. App Login/ User signup interface
2. Require admin permission to update a customer
3. View timeline of transactions for individual customers

##### Backend Development
1. Abstract the Braintree/Stripe API integration into its own class. Currently the routes/customer.py and routes/transaction.py directly hit the API calls. I'd like to create a class interface in which a developer can simply call class.create(args) or class.update(args). And simply by reading the contents of the arguments the class will understand which functionality to perform.
	1. An added benenfit of this abstraction is being able to easily integrate with other Payment Processing APIs down the road. Another developer can rely on the same old methods <strong>class.create(args)</strong> or <strong>class.update(args)</strong> while also using new API. This way the maintainer of the Class Abstraction can add new integrations in the abstracted class while the developer can code in the same fashion as before. It's smooth sailing for the developer.

	2. The above brings me into my next point; Exception handling. If I can abstract the API Gateway Integration for Braintree/Stripe, then I can also build try/catch and exception raising logic around its public methods. This way I can succinctly propogate errors back to the API and also have less backend code processing in my routes file.

3. Another thing I wanted to add is using one credit card payload to submit two transactions on Braintree and Stripe. Currently, transactions are processed on the Braintree API because I'm using a dropin checkout UI that creates a payment method nonce token for the customer's credit card data. This is a great way to send sensitive data over the internet however it's challenging for someone (like me) who wants to send one payload to two APIs. 
	1. I would do this by implementing my own <strong>< input></strong> tags then generating two unique tokens based on the input credit card data and finally submitting one payload to both Braintree and Stripe. This way I can meet the PCI security standards of both APIs and also satisfy my own goal for a "one click checkout - two API integration"

##### What work took up the majority of your time?
1. The majority of my time was spent creating a front end interface. This was challenging because the client server relationship has many intricacies. I used both <strong>< forms></strong> and  <strong>Ajax</strong> methods to send client data to the server. However it took a while to implement addEventListener and callbacks. This area of software development is new to me and I learned as I went along.




#### How could the API URI be improved?

	
1. If I was consistent with sending data to my API using URI Params or Request/Data Params my URI structure would improve. This would give an outsider a clear understanding for Creating/Updating Customers and Transactions. If I had the time I would make the changes below. 

	###### Example
		Update Customers

		PATCH /customers/{{customer_id}}

		opposed to

		/update-stripe-braintree-customer?first_name={{first_name}}&customer_id={{customer_id}}&last_name={{last_name}}&spending_limit={{spending_limit}}&customer_method_nonce={{}}'

	This would have been doable had I not opted to create a frontend interface. Because the HTML Forms and Ajax Request features differ in their client-server relationship. It was challenging to stick with request.forms or URL args.

 
	###### Example
	Transaction Create should have been updated as follows. This would have been the logical choice since the word checkouts was not used in the app


		/transactions/{{payment_method_nonce}}

		as opposed to the current setup

		/checkouts/{{payment_method_nonce}}


