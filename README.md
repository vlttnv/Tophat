Requirements
=======
pip install sqlalchemy  
pip install sqlalchemy-migrate  
pip install flask-sqlalchemy  
pip install flask  
pip install requests

Balancer
=======
python run_balancer.py $balancer_port

Worker
=======
python run_worker.py $worker_port $balancer_addr $balancer_port

Tests
=======
This will take a long time
    cd tests/
    chmod a+x all_tests.sh
    ./all_tests.sh

Producer
=======
Generate its own id
Register with consumer

Broker
=======


Consumer
=======

