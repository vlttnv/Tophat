Requirements
=======
(All installed in venv)
pip install sqlalchemy  
pip install sqlalchemy-migrate  
pip install flask-sqlalchemy  
pip install flask  
pip install requests

Balancer
=======
venv/bin/python run_balancer.py $port

Worker
=======
venv/bin/python run_worker.py $port $balancer_addr $balancer_port

Producer
=======
Generate its own id
Register with consumer

Broker
=======


Consumer
=======

