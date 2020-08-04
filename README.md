This is a prototype/PoC

requires rabbitmq-server and celery. Also docker-compose

first install the requirements (in a virtualenv, ideally)

`pip3 install requirements.txt`

in a new terminal window start rabbitmq-server

`rabbitmq-server`

in an even newer terminal window, cd into zauth/ and run the celery worker

`celery -A zauth worker -l info`

in yet another terminal window, cd into docker/ and run the regtest zcashd node in docker

`docker-compose up`

finally, in another terminal window, cd into zautha/ and setup then run the auther server app

`python3 manage.py makemigrations`

`python3 manage.py migrate`

`python3 manage.py loaddata backend/currency_fixtures.json`

`export AUTHLIB_INSECURE_TRANSPORT=1 && python3 manage.py runserver`

to interact with the demo, in a final terminal window, run the admin controller to create a product 

`python3 admin/controller.py`

then run the client controller to pay for the product, authenticate against the endpoint and access the premium resource 

`python3 client/controller.py`

