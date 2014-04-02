#!/bin/bash

# To run the script:
#	chmod a+x test_two.sh
#	./test_two.sh

balancer_addr=localhost
balancer_port=6000

worker_addr=localhost
worker_port=5000

producer_id=1

printf '\n=========\n'
printf 'Test Case 2: 1 producer and 1 consumer. Validate data persistency when the producer is offline.\n'

printf '\nRunning balancer @ %s:%s.\n' "$balancer_addr" "$balancer_port"
../venv/bin/python ../run_balancer.py $balancer_port &
sleep 3

printf '\nRunning worker @ %s:%s.\n' "$worker_addr" "$worker_port"
../venv/bin/python ../run_worker.py $worker_port $balancer_addr $balancer_port &sleep 3

printf '\nRunning producer: 1.\n'
../venv/bin/python ../client/producer.py $balancer_addr $balancer_port $producer_id &
sleep 3

printf '\nKill the producer.\n'
kill $(ps aux | grep '[p]ython ../client/producer.py' | awk '{print $2}')

printf '\nRunning consumer: Ask data from producer 1.\n'
../venv/bin/python ../client/consumer.py $balancer_addr $balancer_port $producer_id &
sleep 3

printf '\nKill all background processes.\n'
kill $(ps aux | grep '[p]ython ../run_balancer.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ../run_worker.py' | awk '{print $2}')

printf '\nTest Case 2: Completed.\n'
printf '=========\n\n'
