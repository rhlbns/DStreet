from services import angelone

class Candles:
    def __init__(self, service, api_conf):
        if service == 'angelone':
            self.load_angelone(api_conf)
        else:
            raise ValueError("Currently {%v} is not supported".format(v=service))

    def load_angelone(self, api_conf):
        api_key = api_conf['api_key']
        access_token = api_conf['access_token']
        self.candles = angelone.candles.Candles(api_key, access_token)

    def get_candles(self, scrip, exchange, interval, fromdate, todate):
        data = self.candles.get_candles(scrip, exchange, interval, fromdate, todate)
        return data
