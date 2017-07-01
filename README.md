requirements
----------------
MongoDB, RabbitMQ


install
-------------------
pip install -r req.txt

python
from models.models import *
connect_db()
i = Investor(name = "", apikey = "", apisecret = "")
i.save()


run
-------------
celery -A mq worker --beat

