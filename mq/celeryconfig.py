from __future__ import absolute_import, unicode_literals

import config

broker_url = [config.celery_broker]
result_backend = config.celery_backend

include=['mq.tasks']
accept_content = ['json']

