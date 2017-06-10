from __future__ import absolute_import, unicode_literals
import config

import datetime

def str2time(s):
    return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

def time2str(time):
    return time.strftime("%Y-%m-%d %H:%M:%S")
