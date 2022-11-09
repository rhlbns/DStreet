from smartapi import SmartConnect

class Session:
    def __init__(self, api_key, access_token):
        self.api_key = api_key
        self.access_token = access_token
        self.obj = None
        self.feed_token = None
        self.refresh_token = None
        self.user_profile = None

    def is_logged_in(self):
        if self.user_profile is None:
            return False
        return True

    def login(self):
        if self.is_logged_in():
            print ('already logged in...')
            return

        self.obj = SmartConnect(api_key=self.api_key, access_token=self.access_token)

        client_code = input('Client Code: ')
        password = input('Password: ')
        totp = input('TOTP: ')
        data = self.obj.generateSession(client_code, password, totp)
        if data['status'] is False:
            raise Exception(data['message'])

        try:
            self.feed_token = self.obj.getfeedToken()
            self.refresh_token = data['data']['refreshToken']
            self.user_profile = self.obj.getProfile(self.refresh_token)
        except Exception as e:
            print (str(e))

    def logout(self):
        if not self.is_logged_in():
            print ('already logged out..')
            return

        resp = self.obj.terminateSession(client_code)
        if resp['status'] is True:
            self.obj = None
            self.feed_token = None
            self.refresh_token = None
            self.user_profile = None
        else:
            raise Exception(resp['message'])
        return resp

