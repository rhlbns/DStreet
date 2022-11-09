from services.angelone.session import Session
from smartapi import SmartConnect
from dotenv import dotenv_values
from services.angelone.helper import Helper
from datetime import datetime
import json

class Candles:
    def __init__(self, api_key, access_token):
        # create object of call
        self.helper = Helper()
        self.sess = Session(api_key, access_token)
        self.sess.login()

    def logged_in(self):
        if not hasattr(self, 'sess'):
            return False
        return self.sess.is_logged_in()

    def logout(self):
        if hasattr(self, 'sess'):
           self.sess.logout() 

    def get_payload(self, scrip, exchange, interval, fromdate, todate):
        # historical data
        scrip_token = self.helper.get_scrip_token(scrip)
        payload = {
            "exchange": exchange,
            "symboltoken": scrip_token,
            "interval": interval,
            "fromdate": fromdate, 
            "todate": todate
            }
        return payload

    def get_data(self, scrip, exchange, interval, fromdate, todate):
        if not self.logged_in():
            print ('currently logged out..')
            print ("call \"login\" function to login")
            return

        payload = self.get_payload(scrip, exchange, interval, fromdate, todate)
        data = self.sess.obj.getCandleData(payload)
        return data

    def prepare_candles(self, data):
        candles = list()
        keys = ['datetime', 'open', 'high', 'low', 'close', 'volume']
        for values in data:
            candle = {key: value  for key, value in zip(keys, values)}
            candle['datetime'] = self.helper.convert_to_default_dt_format(candle['datetime'])
            candles.append(candle)
        return candles

    def get_candles(self, scrip, exchange, interval, fromdate, todate):
        data = self.get_data(scrip, exchange, interval, fromdate, todate)
        if data['status'] is True:
            if data['data'] is None:
                data = list()
            else:
                data = data['data']
        else:
            raise Exception(data['message'])
        candles = self.prepare_candles(data)
        return candles
