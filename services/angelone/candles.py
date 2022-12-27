from services.angelone.session import Session
from smartapi import SmartConnect
from dotenv import dotenv_values
from services.angelone.helper import Helper
from utils import Utils
from datetime import datetime
import json
import time

class Candles:
    def __init__(self, api_key, access_token):
        # create object of call
        self.helper = Helper()
        self.sess = Session(api_key, access_token)
        self.sess.login()
        self.utils = Utils()

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

    def hop_duration(self, fromdate, todate, interval):
        max_candles_per_request = 500
        _start = self.helper.convert_str_to_dt(fromdate)
        _end = self.helper.convert_str_to_dt(fromdate)
        end = self.helper.convert_str_to_dt(todate)
        while True:
            delta = self.utils.hop_candles(_end, interval, max_candles_per_request)
            _end += delta

            start_str = self.helper.convert_dt_to_str(_start)
            if _end >= end:
                end_str = self.helper.convert_dt_to_str(end)
            else:
                end_str = self.helper.convert_dt_to_str(_end)
            
            yield start_str, end_str
            
            _start = _end

            if _end >= end:
                break

    def append_candles_data(self, c1, c2):
        if len(c1) == 0:
            return c2
        
        if c1[-1] == c2[0]:
            data = c1[:-1] + c2
        else:
            data = c1 + c2
        return data

    def get_candles(self, scrip, exchange, interval, fromdate, todate):
        candles = list()
        start_date = fromdate
        for start_date, end_date in self.hop_duration(fromdate, todate, interval):
            data = self.get_data(scrip, exchange, interval, start_date, end_date)
            start_date = end_date
            if data['status'] is True:
                if data['data'] is not None:
                    data = data['data']
            else:
                raise Exception(data['message'])
            new_candles = self.prepare_candles(data)
            candles = self.append_candles_data(candles, new_candles)
            time.sleep(1) # angleone's throttling limit 3/sec
        return candles
