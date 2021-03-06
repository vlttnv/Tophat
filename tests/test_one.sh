#!/bin/bash

# To run the script:
#	chmod a+x test_one.sh
#	./test_one.sh

# ports 6000 and 5000 will be used

balancer_addr=localhost
balancer_port=6000

worker_addr=localhost
worker_port=5000

producer_id=1

printf '\n=========\n'
printf 'Test Case 1: 1 producer and 1 consumer.\n'

printf '\nRunning balancer @ %s:%s.\n' "$balancer_addr" "$balancer_port"
python ../run_balancer.py $balancer_port &
sleep 3

printf '\nRunning worker @ %s:%s.\n' "$worker_addr" "$worker_port"
python ../run_worker.py $worker_port $balancer_addr $balancer_port &sleep 3

printf '\nRunning producer: 1.\n'
python ../client/producer.py $balancer_addr $balancer_port $producer_id &
sleep 3

printf '\nRunning consumer: Ask data from producer 1.\n'
python ../client/consumer.py $balancer_addr $balancer_port $producer_id &
sleep 3

printf '\nKill all background processes.\n'
kill $(ps aux | grep '[p]ython ../client/producer.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ../run_worker.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ../run_balancer.py' | awk '{print $2}')

printf '\nTest Case 1: Completed.\n'
printf '=========\n\n'
