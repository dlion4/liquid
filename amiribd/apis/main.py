if __name__ == "__main__":
    import requests

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer VY6FaJv7CPx9yVLe5Pk507CIh5OK",
    }

    payload = {
        "BusinessShortCode": 174379,
        "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjQwNTEzMTUyMTUz",
        "Timestamp": "20240513152153",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254745547755,
        "PartyB": 174379,
        "PhoneNumber": 254745547755,
        "CallBackURL": "https://liquid-investment-c119b5140660.herokuapp.com/apis/mpesa/callback",
        "AccountReference": "SynckPay",
        "TransactionDesc": "Buy Mitumba",
    }

    response = requests.request(
        "POST",
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        headers=headers,
        json=payload,
    )

    print(response.text.encode("utf8"))
