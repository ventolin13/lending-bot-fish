requirements
----------------
MongoDB, RabbitMQ


install
-------------------
pip install -r req.txt


run
-------------
celery -A mq worker --beat

