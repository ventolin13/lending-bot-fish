from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta
from decimal import Decimal

from mongoengine import *

from bson import ObjectId

def connect_db():
    connect("ptest", "db")

    
# first
# from models.models import *
# connect_db()
# i = Investor(name = "", apikey = "", apisecret = "")
# i.save()

class Investor(Document):
    name =                      StringField()
    phone =                     StringField()
    email =                     StringField()
    apikey =                    StringField()
    apisecret =                 StringField()
    is_active =                 BooleanField(default=True)
    last_update =               DateTimeField()
    settings =                  DictField()


    meta = {
            "db_alias": "db"}

class LoanHistory(Document):
    order_id =                  LongField()
    investor_id =               ObjectIdField()
    currency =                  StringField()
    amount =                    DecimalField(precision=8)
    rate =                      DecimalField(precision=8)
    duration =                  DecimalField(precision=8)
    open =                      DateTimeField()
    close =                     DateTimeField()
    fee =                       DecimalField(precision=8)
    earned =                    DecimalField(precision=8)
    interest =                  DecimalField(precision=8)

    balance =                   DecimalField(precision=8)
    abalance =                  DecimalField(precision=8)
    created =                   DateTimeField(default=datetime.now)

    meta = {
            "db_alias": "db"}


class DailyLoanHistory(Document):
    investor_id =               ObjectIdField()
    currency =                  StringField()
    num_deals =                 IntField()
    amount =                    DecimalField(precision=8)
    rate =                      DecimalField(precision=8)
    date =                      DateTimeField()
    fee =                       DecimalField(precision=8)
    earned =                    DecimalField(precision=8)
    interest =                  DecimalField(precision=8)
    ointerest =                 DecimalField(precision=8)
    created =                   DateTimeField(default=datetime.now)

    meta = {
            "db_alias": "db"}

class Interest(Document):
    investor_id =               ObjectIdField()
    currency =                  StringField()
    qrate =                     DecimalField(precision=8)
    created =                   DateTimeField(default=datetime.now)

    meta = {
            "db_alias": "db"}


