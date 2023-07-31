from twilio.rest import Client

def load(message, contacts):
    try:
        # Replace these values with your Twilio Account SID and Auth Token
        account_sid = '<SID>'
        auth_token = '<API TOKEN>

        twilio_phone_number = '<PHONE NUMBER>'
        recipient_phone_number = contacts

        client = Client(account_sid, auth_token)


        # Send the message
        message = client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=recipient_phone_number
        )

        # Print the message SID
        return True
    except:
        return False
