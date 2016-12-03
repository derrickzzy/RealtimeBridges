def call():
    import twilio
    from twilio.rest import TwilioRestClient

    # put your own credentials here
    ACCOUNT_SID = "ACbb9db4553761639ba50b64b4dc7935a9"
    AUTH_TOKEN = "070e0e67cd1ba5f909f306db5ba0ecfb"
 
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    call = client.calls.create(
        to="6176275185",
        from_="+16172199550",
        url='http://twimlbin.com/external/2ed449b142ce0f87',
        method="POST",
        fallback_method="GET",
        status_callback_method="GET",
        if_machine="Continue",
        record="false"
    )

    print call.sid

if __name__ == '__main__':
    call()
