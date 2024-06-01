import os
import k2connect

CLIENT_ID = 'nTsZIxrmuTKQ3JaTpiB5CrKgpzL4YAXKM8qwrgnxpqY'
CLIENT_SECRET = 'ePXiz5gGeA9HQk0CCbkKnQ9M3vn3YmME8FNebugTBOk'
BASE_URL = 'https://sandbox.kopokopo.com/'



# Using Kopo Kopo Connect - https://github.com/kopokopo/k2-connect-python (Recommended)
k2connect.initialize(CLIENT_ID, CLIENT_SECRET, BASE_URL)
stk_service = k2connect.ReceivePayments
# create an instance of the service 
authenticator = k2connect.Tokens

# access a method provided by the service
token = authenticator.request_access_token()['access_token']

request_body = {
  "access_token": token,
  "callback_url": "https://webhook.site",
  "first_name": "python_first_name",
  "last_name": "python_last_name",
  "email": "test@gmail.com",
  "payment_channel": "MPESA",
  "phone_number": "+254745547755",
  "till_number": "K000000",
  "amount": "10",
    "metadata": {
        "customerId": '123456789',
        "reference": '123456',
        "notes": 'Payment for invoice 123456'
    }
}

stk_push_location = stk_service.create_payment_request(request_body)
stk_push_location # => 'https://sandbox.kopokopo.com/api/v1/incoming_payments/247b1bd8-f5a0-4b71-a898-f62f67b8ae1c'

print(stk_push_location)
