Requirements
=======
	python 2.x

	pip install sqlalchemy
	pip install sqlalchemy-migrate
	pip install flask-sqlalchemy
	pip install flask
	pip install requests
	pip install tornado

Database Setup
=======
	python db_create.py  

Balancer
=======
	python run_balancer.py $balancer_port

Worker
=======
	python run_worker.py $worker_port $balancer_addr $balancer_port

Producer
=======
	chmod a+x run_producers.sh
	./run_producers.sh $balancer_addr $balancer_port $start_producer_id $num_producer
	
Consumer
=======
	chmod a+x run_consumers.sh
	./run_consumers.sh $balancer_addr $balancer_port $start_producer_id $num_producer

Tests
=======
### All test cases descriptions
	cd tests/
	sublime(or any text editor) test_cases.txt

### Read individual test results
	cd tests/results/
	sublime(or any text editor) test_number.txt

### Run all tests
	cd tests/
	chmod a+x all_tests.sh
	./all_tests.sh

### Run individual tests
	cd tests/
	chmod a+x test_number.sh
	./test_number.sh
