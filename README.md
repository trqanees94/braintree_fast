# Braintree-Stripe Fast App

Braintree-Stripe integration for python in the Flask framework.

## Purpose of Braintree-Stripe Fast App
This app is meant to limit customers spending online. As people move away from Brick and Mortar stores and shift towards E-commerce, parents can limit their children's spending through this interface.

## App User Interface
1. Create Customer
2. View All Customers
3. Update a customer
4. Create a transaction for a customer


## Setup Instructions

1. git clone https://github.com/trqanees94/braintree_stripe_fast_app.git

2. Install requirements:
  ```sh
  pip3 install -r requirements.txt
  ```

3. Start server:
  ```sh
  python3 app.py
  ```

  By default, this runs the app on port `4567`. You can configure the port by setting the environmental variable `PORT`.


## Running tests

Run `python3 test_app.py`

## Testing Transactions

1.Sandbox transactions must be made with credit card number: <code>4111 1111 1111 1111</code>


## Table of Contents
<ul>
  <li><a href='#api-endpoints'>API Endpoints</a>
    <ul>
      <li><a href='#customer'>Customer</a></li>
        <ul>
          <li><a href='#create'>Create</a></li>
          <li><a href='#update'>Update</a></li>
          <li><a href='#view_customer'>View Customer</a></li>
          <li><a href='#view_all_customers'>View All Customer</a></li>
        </ul>
      </li>
      <li><a href='#transactions'>Transactions</a>
        <ul>
          <li><a href='#create-1'>Create</a></li>
        </ul>
</ul>

## API Endpoints
<table>
  <tr>
    <th>Method</th>
    <th></th>
    <th>Path</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Create Customer</td>
    <td><code>POST</code></td>
    <td><code>/customer</code></td>
    <td>Generate Fast customer details (e.g. spendinglimit, firstname, lastname).</td>
  </tr>
  <tr>
    <td>View All Customers</td>
    <td><code>GET</code></td>
    <td><code>/customers</code></td>
    <td>View all Fast customers.</td>
  </tr>
  <tr>
    <td>View A Single Customer</td>
    <td><code>GET</code></td>
    <td><code>/customer/{{customer_id}}</code></td>
    <td>View a single Fast customer.</td>
  </tr>
  <tr>
    <td>Update Customer</td>
    <td><code>GET</code></td>
    <td><code>/update-stripe-braintree-customer?first_name={{first_name}}&customer_id={{customer_id}}&last_name={{last_name}}&spending_limit={{spending_limit}}&customer_method_nonce={{}}'</code></td>
    <td>Send an update to the Braintree/Stripe API and Fast Customer database.</td>
  </tr>
  <tr>
    <td>Create Transaction</td>
    <td><code>POST</code></td>
    <td><code>/checkouts/{{payment_method_nonce}}</code></td>
    <td>Create the Braintree transaction with supplied payment_method_nonce</td>
  </tr>
<table>


### Customer
#### Create Customer
Create a customer on Braintree and Stripe, store both records in MongoDB
<table>
  <tbody>
    <tr>
      <td align="right"><b>URL</b></td>
      <td align="left"><code>/customer</code></td>
    </tr>
    <tr>
      <td align="right"><b>Method</b></td>
      <td align="left"><code>POST</code></td>
    </tr>
    <tr>
      <td align="right"><b>URL Params</b></td>
      <td align="left">None</td>
    </tr>
    <tr>
      <td align="right"><b>Data Params</b></td>
      <td align="left">request.form: ([('first_name', ''), ('last_name', ''), ('spending_limit', ''), ('customer_method_nonce', '')])</td>
    </tr>
    <tr>
      <td align="right"><b>Success Response</b></td>
      <td align="left">
        <pre><code>
{
    'fast_customer_id': '5f027d475c0f0faf6c863793', 
    'braintree_id': '290457393', 
    'stripe_id': 'cus_HauucCq1RPCyXB', 
    'error': {}, 
    'success': True
}</code></pre>
      </td>
    </tr>
    <tr>
      <td align="right"><b>Error Response</b></td>
      <td align="left">
        <i>See <a href="#error-codes">Error Codes</a> for a complete list of errors.</i>
        <pre><code>
{
    'fast_customer_id': None, 
    'braintree_id': {}, 
    'stripe_id': {}, 
    'error': {
        "error_message": "", 
        "error_code": 302
    }, 
    'success': False
}</code></pre>
      </td>
    </tr>
  </tbody>
</table>

#### Update Customer
Update a customer on Braintree and Stripe, store both records in MongoDB
<table>
  <tbody>
    <tr>
      <td align="right"><b>URL</b></td>
      <td align="left"><code>/update-stripe-braintree-customer?first_name={{first_name}}&customer_id={{customer_id}}&last_name={{last_name}}&spending_limit={{spending_limit}}&customer_method_nonce={{}}
</code></td>
    </tr>
    <tr>
      <td align="right"><b>Method</b></td>
      <td align="left"><code>GET</code></td>
    </tr>
    <tr>
      <td align="right"><b>URL Params</b></td>
      <td align="left">request.args: [('first_name'), ('last_name'), ('spending_limit'), ('customer_method_nonce')]</td>
    </tr>
    <tr>
      <td align="right"><b>Data Params</b></td>
      <td align="left">None</td>
    </tr>
    <tr>
      <td align="right"><b>Success Response</b></td>
      <td align="left">
        <pre><code>
{
    'fast_customer_id': '5f026a6342b689f3294745a4', 
    'braintree_id': '853421331',
    'stripe_id': 'cus_Hatbs5pT0jqfrI',
    'error': {},
    'success': True
}</code></pre>
      </td>
    </tr>
    <tr>
      <td align="right"><b>Error Response</b></td>
      <td align="left">
        <i>See <a href="#error-codes">Error Codes</a> for a complete list of errors.</i>
        <pre><code>
{
    'fast_customer_id': None, 
    'braintree_id': {}, 
    'stripe_id': {}, 
    'error': {
        "error_message": "", 
        "error_code": 302
    }, 
    'success': False
}</code></pre>
      </td>
    </tr>
  </tbody>
</table>


#### View Customer
View a customer using Fast Customer ID
<table>
  <tbody>
    <tr>
      <td align="right"><b>URL</b></td>
      <td align="left"><code>/customer/{{customer_id}}</code></td>
    </tr>
    <tr>
      <td align="right"><b>Method</b></td>
      <td align="left"><code>GET</code></td>
    </tr>
    <tr>
      <td align="right"><b>URL Params</b></td>
      <td align="left">customer_id</td>
    </tr>
    <tr>
      <td align="right"><b>Data Params</b></td>
      <td align="left">None</td>
    </tr>
  </tbody>
</table>


#### View All Customers
View all Fast Customers
<table>
  <tbody>
    <tr>
      <td align="right"><b>URL</b></td>
      <td align="left"><code>/customers</code></td>
    </tr>
    <tr>
      <td align="right"><b>Method</b></td>
      <td align="left"><code>GET</code></td>
    </tr>
    <tr>
      <td align="right"><b>URL Params</b></td>
      <td align="left">None</td>
    </tr>
    <tr>
      <td align="right"><b>Data Params</b></td>
      <td align="left">None</td>
    </tr>
  </tbody>
</table>



### Transactions 
#### Create
Create a transaction for a customer on Braintree and store record in MongoDB
<table>
  <tbody>
    <tr>
      <td align="right"><b>URL</b></td>
      <td align="left"><code>/checkouts/{{payment_method_nonce}}</code></td>
    </tr>
    <tr>
      <td align="right"><b>Method</b></td>
      <td align="left"><code>POST</code></td>
    </tr>
    <tr>
      <td align="right"><b>URL Params</b></td>
      <td align="left"><b>payment_method_nonce [Required]</b> | payment_method_nonce assigned to the bt-drop-in-wrapper.</td>
    </tr>
    <tr>
      <td align="right"><b>Data Params</b></td>
      <td align="left">
      <ul>
        <li>customer_id (<i>string</i>)</li>
        <ul>
            <li>Fast customer ID.</li>
        </ul>
        <li>amount (<i>string</i>)</li>
        <ul>
            <li>Amount inserted in form</li>
        </ul>
        <li>payment_method_nonce (<i>string</i>)</li>
        <ul>
            <li>payment_method_nonce issued from bt-drop-in-wrapper <a href="https://developers.braintreepayments.com/guides/transactions/python">docs</a>]</b></li>
        </ul>
      </ul>
      <b>Example Request Form</b>
        <pre><code>
{
    ('customer_id', '5f026a6342b689f3294745a4'), 
    ('amount', '10'), 
    ('payment_method_nonce', 'tokencc_bf_yqz6gt_3spr4t_ddk2hr_8cr7qb_my8')
}</code></pre>
      </td>
    </tr>
    <tr>
      <td align="right"><b>Success Response</b></td>
      <td align="left">
        <pre><code>
{
    'fast_transaction_id': '5f02874560e0ee8612916cb2', 
    'braintree_transaction_id': 'caqapryb', 
    'error': {}, 
    'success': True
}</code></pre>   
      </td>
    </tr>
    <tr>
      <td align="right"><b>Error Response</b></td>
      <td align="left">
        <pre><code>
{
    'fast_transaction_id': None, 
    'braintree_transaction_id': {}, 
    'error': 
        {
        'error_message': 'Transaction Amount: 1000000 Exceeds Limit: 100', 
        'error_code': '415'
        }, 
    'success': False
}</code></pre>
      </td>
    </tr>****
  </tbody>
</table>

<pre>

</pre>
