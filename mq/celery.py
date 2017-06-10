from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('mq')
app.config_from_object('mq.celeryconfig')

if __name__ == '__main__':
   app.start()