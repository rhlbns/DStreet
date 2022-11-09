
# DalalStreetData

DalalStreetData is a python library for downloading the prices of various equities listed in the Indian Stock market.
Using this library, you can access and download historical as well as live stock market data.

Currently, the library only supports Angelone's smartapi integration. Since Angelone provides free API for accessing historical and live stock market data, this is the go-to choice of most developers who want to experiment with algo-trading patterns.

Moving forward I will integrate more providers such as Zerodha/Upstock etc with this library. But for the time being you need to have a demat account with Angelone.


## Usage

#### Get data in candle-stick format

```
    from candles import Candles

    client_id = 'angelone-client-code'
    password = 'angelone-login-password'
    api_key = 'api-key'
    access_token = 'access-token'
    conf = {'api_key': api_key, 'access_token': access_token}

    scrip = 'INFY'
    exchange = "NSE"
    interval = 'ONE_HOUR'
    fromdate = '2022-09-01 09:15'
    todate = '2022-09-30 15:30'

    c = Candles(service='angelone', api_conf=conf)
    candles = c.get_candles(scrip, exchange, interval, fromdate, todate)
    print (candles)
```

## Upcoming Features
- Indefinate candles download - currrent version only allows us to access 500 candles per request.
- F&O candles with OI
- Live ticker data for equity
- Live ticker data for F&O

## Authors

- [@rhlbns](https://github.com/rhlbns)

