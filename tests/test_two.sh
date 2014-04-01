#!/bin/bash

printf '\n=========\n'
printf 'Test Case 2: 1 producer and 1 consumer. Validate data persistency when the producer is offline.\n'

printf 'Running producer: 1.\n'
python ../client/producer.py $1 $2 1 &
PID_PRODUCER=$!
sleep 3

# Stop the producer server
printf 'Killing producer: 1.\n'
kill $PID_PRODUCER

printf 'Running consumer: Ask data from producer 1.\n'
python ../client/consumer.py $1 $2 1

printf '\nTest Case 2: Completed.\n'
printf '=========\n\n'