#!/usr/bin/env python3
import argparse
import pyRofex

def market_data_handler(message):
    print("Último precio operado: $" + message['marketData']['LA']['price'])
    print("Consultando BID")
    
    if (len(message['marketData']['BI'])>0):
        bid = message['marketData']['BI'][0]['price']
        print("Precio de BID: $" + bid)
        place_order(bid - 0.01)
    else:
        print("No hay BIDs activos")
        default_bid=75.25
        place_order(default_bid)
        
    close_connection()

def place_order(bid):
    print("Ingresando orden a: $" + bid)
    pyRofex.send_order(ticker=args.ticker,
                       side=pyRofex.Side.BUY,
                       size=1,
                       price=bid,
                       order_type=pyRofex.OrderType.LIMIT)

def error_handler(message):
    if (message['description'][-11:] == 'don\'t exist'):
        print("Símbolo inválido")
    else:
        print("Error: " + message)
    close_connection()

def exception_handler(e):
    print("Exception: " + e.message)
    close_connection()

def close_connection():
    print("Cerrando sesión en Remarkets")
    pyRofex.close_websocket_connection()
    
def open_connection():
    pyRofex.init_websocket_connection(market_data_handler=market_data_handler,
                                  error_handler=error_handler,
                                  exception_handler=exception_handler)

    instruments = [args.ticker]
    entries = [pyRofex.MarketDataEntry.BIDS, pyRofex.MarketDataEntry.LAST]
    print("Consultando símbolo")
    pyRofex.market_data_subscription(tickers=instruments, entries=entries)
    pyRofex.market_data_subscription(tickers=["InvalidInstrument"], entries=entries)


parser = argparse.ArgumentParser()
parser.add_argument("ticker", help="Ticker de MATBA ROFEX")
parser.add_argument("-u", dest="username", help="Usuario de Remarkets", required=True)
parser.add_argument("-p", dest="password", help="Passowrd de Remarkets", required=True)
parser.add_argument("-a", dest="account", help="Cuenta de Remarkets", required=True)
args = parser.parse_args()

print("Iniciando sesión en Remarkets")
try:
    pyRofex.initialize(user=args.username,
                       password=args.password,
                       account=args.account,
                       environment=pyRofex.Environment.REMARKET)
    open_connection()
except Exception as e:
    if (str(e) == "Authentication fails. Incorrect User or Password"):
        print("Error en la autenticación, usuario o password incorrectos")
    else:
        print(str(e))
