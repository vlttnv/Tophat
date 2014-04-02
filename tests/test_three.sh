#!/bin/bash

# To run the script:
#	chmod a+x test_three.sh
#	./test_three.sh

balancer_addr=localhost
balancer_port=6000

worker_addr=localhost
worker_port=5000

producer_id=3214214

printf '\n=========\n'
printf 'Test Case 3: 1 consumer. Ask data from a producer that does not exist in the database.\n'

printf '\nRunning balancer @ %s:%s.\n' "$balancer_addr" "$balancer_port"
python ../balance.py $balancer_port &
sleep 3

printf '\nRunning worker @ %s:%s.\n' "$worker_addr" "$worker_port"
python ../run.py $worker_port $balancer_addr $balancer_port &
sleep 3

printf '\nRunning consumer: Ask data from producer 3214214.\n'
python ../client/consumer.py $balancer_addr $balancer_port $producer_id
sleep 3

printf '\nKill all background processes.\n'
kill $(ps aux | grep '[p]ython ../run.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ../balance.py' | awk '{print $2}')

printf '\nTest Case 3: Completed.\n'
printf '=========\n\n'
