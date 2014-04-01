#!/bin/bash

# To run the script:
#	chmod a+x test_one.sh
#	./test_one.sh

balancer_addr=localhost
balancer_port=1337

worker_addr=localhost
worker_port=5000

producer_id=1

printf '\n=========\n'
printf 'Test Case 1: 1 producer and 1 consumer.\n'

printf 'Running balancer @ %s:%s.\n' "$balancer_addr" "$balancer_port"
./start_balancer.sh $balancer_port &

printf 'Running worker @ %s:%s.\n' "$worker_addr" "$worker_port"
./start_worker.sh $worker_port $balancer_addr $balancer_port &

printf 'Running producer: 1.\n'
./start_producer.sh $balancer_addr, $balancer_port $producer_id &
PID_PRODUCER=$!
sleep 3

printf 'Running consumer: Ask data from producer 1.\n'
./start_consumer.sh $balancer_addr $balancer_port $producer_id &

printf 'Killing producer: 1.\n'
kill $PID_PRODUCER

printf '\nTest Case 1: Completed.\n'
printf '=========\n\n'

exit