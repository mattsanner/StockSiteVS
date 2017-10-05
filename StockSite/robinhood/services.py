from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
from decimal import Decimal

import requests
import datetime

from .models import RobinhoodUser

def encrypt_value(encrypt_me):
    f = Fernet(settings.FERNET_KEY)
    bitValue = bytes(encrypt_me, 'utf-8')
    return f.encrypt(bitValue)

def decrypt_value(decrypt_me):
    f = Fernet(settings.FERNET_KEY)
    return f.decrypt(decrypt_me).decode("utf-8")

def get_auth_header(user):
    key = decrypt_value(user.robinhooduser.token)
    return {"Authorization": ("Token " + key)}

class RobinhoodServices():
    #Registers robinhood user and saves to DB
    def register(user, username, password): 
        r = requests.post('https://api.robinhood.com/api-token-auth/', {"username": username, "password": password})
        data = r.json()
        if 'token' in data.keys():
            rh_user = RobinhoodUser(user=user, username=username)
            rh_user.token = encrypt_value(data['token'])
            rh_user.signedin = True
            rh_user.save()            
            return True
        else:
            return False   #TODO log an error and possibly an error code/value in this case   
        
    #Authenticates robinhooduser if they already exist. Registers if they don't
    def authenticate(user, username, password):
        try:
            user.robinhooduser
            r = requests.post('https://api.robinhood.com/api-token-auth/', {"username": username, "password": password})
            data = r.json()
            if 'token' in data.keys():
                user.robinhooduser.token = encrypt_value(data['token'])
                user.robinhooduser.signedin = True
                user.robinhooduser.save()
        except RobinhoodUser.DoesNotExist as e:
            register(user, username, password)
        except Exception as e:
            return e

    #Calls RH account API for account info
    def get_account_info(user):
        try:            
            header = get_auth_header(user)
            r = requests.get("https://api.robinhood.com/accounts/", headers=header)
            return r.json()
        except Exception as e:
            return e

    #Uses user account info to get API URL for positions API
    #Returns position user has an active stake in
    def get_current_positions(user):
        try:            
            data = RobinhoodServices.get_account_info(user)
            positionsUrl = data['results'][0]['positions']
            header = get_auth_header(user)
            posRequest = requests.get(positionsUrl, headers=header)
            posData = posRequest.json()['results']                 
            return RobinhoodServices.filter_to_current_positions(posData)
        except Exception as e:
            return e

    #Gets stocks and info based on user's current positions.
    #TODO Refactor the hell out of this
    def get_stocks(user):
        try:
            position_data = RobinhoodServices.get_current_positions(user)
            stocks_info = { }
            i = 0
            #for i = 0; i < position_data.items().count; i++: position_data[i], want ['instrument'] ['average_buy_price'], ['quantity']
            for i in range(0, len(position_data)):
                instLink = position_data[i]['instrument']
                avgBuy = position_data[i]['average_buy_price']
                quant = position_data[i]['quantity']
                stock_info = RobinhoodServices.get_stock_info(instLink)
                symbol = stock_info['symbol']
                name = stock_info['simple_name']
                fundLink = stock_info['fundamentals']
                type= stock_info['type']
                openPrices = RobinhoodServices.get_price_movement_table_info(symbol)
                stock = {
                            "symbol": symbol,
                            "type": type,
                            "averageBuyPrice": avgBuy,
                            "quantity": quant,
                            "instrumentLink": instLink,
                            "fundamentalsLink": fundLink,
                            "day_open_price": openPrices['day_open_price'],
                            "week_open_price": openPrices['week_open_price'], 
                            "month_open_price": openPrices['month_open_price'],
                        }
                stock = RobinhoodServices.get_price_difference_info(stock)
                stocks_info.update({name: stock})
                i = i+1
            return stocks_info
        except Exception as e:
            return e

    #Get stock info based on stock's URL
    def get_stock_info(stock_url):
        r = requests.get(stock_url)
        data = r.json()
        return data

    #Filters full list of positions down to only those currently held
    def filter_to_current_positions(positions_data):
        currentPositions = {}
        i = 0
        for entry in positions_data:
            if int(entry['quantity'].split('.')[0]) > 0:
                currentPositions.update({i: entry})
                i = i + 1                    
        return currentPositions

    def get_historical_data(ticker, interval, span, bounds):
        apiUrl = RobinhoodServices.endpoints['historical_data'] + ticker + '/'
        params = {"interval": interval, "span": span, "bounds": bounds }
        r = requests.get(apiUrl, params)
        return r.json()

    def get_historical_month_data(ticker):
        data = RobinhoodServices.get_historical_data(ticker, "day", "year", "regular")
        length = len(data['historicals'])
        cutData = data['historicals'][(length-30):length]
        return cutData
        
    #TODO Find way to conveniently calculate price differences between start of day, 5 day, 1 month
    def get_price_movement_table_info(ticker):
        prices = {}
        dataDay = RobinhoodServices.get_historical_data(ticker, "5minute", "day", "regular")['historicals'][0]
        dataWeek = RobinhoodServices.get_historical_data(ticker, "10minute", "week", "regular")['historicals'][0]
        dataMonth = RobinhoodServices.get_historical_data(ticker, "day", "year", "regular")
        length = len(dataMonth['historicals'])
        dataMonth = dataMonth['historicals'][length-31]
        return {"day_open_price": dataDay['open_price'], "week_open_price": dataWeek['open_price'], "month_open_price": dataMonth['open_price'] } 

    #TODO Will need refactoring
    def get_price_difference_info(stock):
        currentPrice = Decimal(RobinhoodServices.get_last_trade_price(stock['symbol']))
        dayDiff = currentPrice - Decimal(stock['day_open_price'])
        weekDiff = currentPrice - Decimal(stock['week_open_price'])
        monthDiff = currentPrice - Decimal(stock['month_open_price'])
        stock.update({"current_price": currentPrice, "day_diff": dayDiff, "week_diff": weekDiff, "month_diff": monthDiff})
        return stock

    def get_last_trade_price(ticker):
        r = requests.get(RobinhoodServices.endpoints['quotes'] + ticker + '/')
        return r.json()['last_trade_price']

    #TODO: Replace hardcoded URLs with references to this list
    endpoints = {
            "login": "https://api.robinhood.com/api-token-auth/",
            "accounts": "https://api.robinhood.com/accounts/",
            "historical_data": "https://api.robinhood.com/quotes/historicals/",
            "quotes": "https://api.robinhood.com/quotes/",
        }