import unittest
import mock
import test_helpers
import os
import app
import tempfile

@mock.patch('braintree.client_token_gateway.ClientTokenGateway.generate', staticmethod(lambda: 'test_client_token'))
@mock.patch('braintree.TransactionGateway.find', staticmethod(lambda x: test_helpers.MockObjects.TRANSACTION_SUCCESSFUL))
class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_checkout_contains_checkout_form(self):
        res = self.app.get('/checkouts/new')
        self.assertIn(b'<form id="customer-form"', res.data)

    def test_checkout_contains_dropin_div(self):
        res = self.app.get('/checkouts/new')
        self.assertIn(b'<div id="bt-dropin"', res.data)

    def test_checkout_includes_amount_input(self):
        res = self.app.get('/create-child-transaction')
        self.assertIn(b'<label for="amount"', res.data)
        self.assertIn(b'<input id="amount" name="amount" type="tel"', res.data)

    def test_checkouts_show_route_available(self):
        res = self.app.get('/checkouts/1')
        self.assertEqual(res.status_code, 200)

    def test_checkouts_show_displays_info(self):
        res = self.app.get('/checkouts/1')
        self.assertIn(b'my_id', res.data)
        self.assertIn(b'10.00', res.data)
        self.assertIn(b'MasterCard', res.data)
        self.assertIn(b'ijkl', res.data)
        self.assertIn(b'Billson', res.data)
        self.assertIn(b'Billy Bobby Pins', res.data)
        self.assertIn(b'submitted_for_settlement', res.data)

    def test_checkouts_show_displays_success_message_when_transaction_succeeded(self):
        res = self.app.get('/checkouts/1')
        self.assertIn(b'Sweet Success!', res.data)

    def test_checkouts_show_displays_failure_message_when_transaction_failed(self):
        with mock.patch('braintree.TransactionGateway.find', staticmethod(lambda x: test_helpers.MockObjects.TRANSACTION_FAILURE)):
            res = self.app.get('/checkouts/1')
            self.assertIn(b'Transaction Failed', res.data)


if __name__ == '__main__':
    unittest.main()
