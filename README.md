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

## Tests
### All test cases descriptions
	cd tests/
	sublime(or any text editor) TEST_CASES

### Run all tests
	cd tests/
	chmod a+x all_tests.sh
	./all_tests.sh

### Run individual tests
	cd tests/
	chmod a+x test_number.sh
	./test_number.sh
