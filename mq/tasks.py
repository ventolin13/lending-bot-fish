from __future__ import absolute_import, unicode_literals
import config

from celery.decorators import periodic_task
from celery.task.schedules import crontab
from decimal import Decimal
from mongoengine import Q

import datetime
import time
import random
import math

from mq.celery import app as capp
from mq.stats import get_lending_balance, get_lending_history, get_lending_active, get_lending_offers, get_lending_interest, make_lending_offer, cancel_lending_offer, toggle_lending_autorenew, bound_interest
from models.models import connect_db, Investor, LoanHistory, DailyLoanHistory, Interest
from utils import str2time, time2str

MIN_AMOUNT = {"BTC": 0.01}


@capp.task(ignore_result=True)
def ctest(name):
    print "ctest %s" % name


@periodic_task(run_every=datetime.timedelta(seconds=10))
def btest():
    print "btest"


@periodic_task(run_every=datetime.timedelta(seconds=60))
def update_interests():
    print "update_interests"
    connect_db()
    powers = {}
    investor = Investor.objects(is_active=True).first()
    interests = get_lending_interest(investor, "BTC")
    rateq = sorted(interests, key=lambda x:x["rate"])[:5][0] # quantil
    interest = Interest(investor_id=investor.id, currency="BTC", rateq=rqteq)
    interest.save()


@periodic_task(run_every=datetime.timedelta(seconds=2*60))
def make_loans():
    connect_db()
    investor = Investor.objects(is_active=True).first()

    history = get_lending_history(investor) # ***********           hitory
    cash = get_lending_balance(investor) # ***********              cash
    offers = get_lending_offers(investor) # ***********             offers
    active = get_lending_active(investor) # ***********             active
    
    currency = "BTC"
    balance = Decimal(cash.get(currency, 0))
    obalance = sum([Decimal(o["amount"]) for o in offers.get(currency, [])]+[Decimal(0)])
    abalance = sum([Decimal(a["amount"])+Decimal(a["fees"]) for a in active if a["currency"] == currency]+[Decimal(0)])

    for h in history:
        if LoanHistory.objects(order_id=h["id"]).only("id").count(): continue
        currency = h["currency"]
        l = LoanHistory(investor_id=investor.id)
        l.order_id = h["id"]
        l.currency = currency
        l.amount = h["amount"]
        l.rate = h["rate"]
        l.duration = h["duration"]
        l.open = str2time(h["open"])
        l.close = str2time(h["close"])
        l.fee = h["fee"]
        l.earned = h["earned"]
        l.interest = h["interest"]
        l.balance = balance[currency]+obalance[currency]
        l.abalance = abalance[currency]
        l.save()

    total = balance[currency] + obalance[currency] + abalance[currency] #estimate balance
    print "%s balances f: %s, o: %s, a: %s = t: %s" % (currency, balance[currency], obalance[currency], abalance[currency], total)

    qrate_list = Interest.objects(Q(investor_id=investor.id)&Q(currency=currency)).distinct("qrate").order_by("-created")[:240]
    qrate_list = len(qrate_list)
    if len(qrate_list) < 240: return
    
    is_trade = True
    
#    Logic TODO
#    History rate analize and something else
#    if balance < total/2: is_trade = False

    rate = sorted(qrate_list)[120] # average
    amount = min(balance, max(total/5, MIN_AMOUNT["BTC"]))
    
    if is_trade:
        ret = make_lending_offer(investor, "BTC", amount, rate, 2, "", autoRenew=0)
        if ret: balance -= amount

    investor.last_update = datetime.datetime.now()
    investor.save()

























