from __future__ import absolute_import, unicode_literals
import config

from decimal import Decimal
from mongoengine import Q

import calendar

from models.models import connect_db, Investor, LoanHistory, DailyLoanHistory, Interest
from poloniex import poloniex


#Loan stats
#----------------------------------------------------------------------------------------------
def get_lending_balance(investor, currency=None):
    p = poloniex(investor.apikey.encode("utf8"), investor.apisecret.encode("utf8"))
    ret = p.api_query("returnAvailableAccountBalances")
    if not isinstance(ret, dict): return Decimal(0)
    if currency: return Decimal(ret.get("lending", {}).get(currency, 0))
    return ret.get("lending", {})


def get_lending_history(investor, currency=None):
    p = poloniex(investor.apikey.encode("utf8"), investor.apisecret.encode("utf8"))
    ret = p.api_query("returnLendingHistory", {"limit":500})
    if not isinstance(ret, list): return []
    if currency: return [l for l in ret if l.get("currency", []) == currency]
    return ret

def get_lending_offers(investor, currency=None):
    p = poloniex(investor.apikey.encode("utf8"), investor.apisecret.encode("utf8"))
    ret = p.api_query("returnOpenLoanOffers")
    if not isinstance(ret, dict): return {}
    if currency: return [l for l in ret if l.get("currency", []) == currency]
    return ret

def get_lending_active(investor, currency=None):
    p = poloniex(investor.apikey.encode("utf8"), investor.apisecret.encode("utf8"))
    ret = p.api_query("returnActiveLoans")
    if not isinstance(ret, dict): return []
    if currency: return [l for l in ret.get("provided", []) if l.get("currency") == currency]
    return ret.get("provided", [])

def get_lending_interest(investor, currency):
    p = poloniex(investor.apikey.encode("utf8"), investor.apisecret.encode("utf8"))
    ret = p.api_query("returnLoanOrders", {"currency": currency})
    if not isinstance(ret, dict): return []
    return [l for l in ret.get("offers", [])]


# Loan control
#----------------------------------------------------------------------------------------------
def make_lending_offer(investor, currency, amount, rate, duration, strategy, autoRenew=1):
    p = poloniex(investor.apikey.encode("utf8"), investor.apisecret.encode("utf8"))
    data = {"currency":currency, "amount": amount, "lendingRate": rate, "duration":duration, "autoRenew": autoRenew}
    print data
    ret = p.api_query("createLoanOffer", data)
    print ret
    if not isinstance(ret, dict): return 0
    return ret.get("orderID", 0)


def cancel_lending_offer(investor, order_id):
    p = poloniex(investor.apikey.encode("utf8"), investor.apisecret.encode("utf8"))
    ret = p.api_query("cancelLoanOffer", {"orderNumber": str(order_id)})
    if not isinstance(ret, dict): return False
    return ret.get("success") == 1


def toggle_lending_autorenew(investor, order_id):
    p = poloniex(investor.apikey.encode("utf8"), investor.apisecret.encode("utf8"))
    ret = p.api_query("toggleAutoRenew", {"orderNumber": str(order_id)})
    if not isinstance(ret, dict): return False
    return ret.get("success") == 1



# Statistics
#----------------------------------------------------------------------------------------------
def bound_interest(interests, bound):
    rate, brate = Decimal(0), Decimal(0)
    mrate = Decimal(99)
    xrate = Decimal(0)
    score = Decimal(0)
    max_num = 0
    for num, i in enumerate(interests):
        score += Decimal(i["amount"])
        mrate = min(mrate, Decimal(i["rate"]))
        xrate = max(xrate, Decimal(i["rate"]))
        if score < Decimal(bound):
            brate = xrate
            max_num = num
    brate = brate or mrate
    return mrate, brate, xrate




















