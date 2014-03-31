#!/bin/bash

printf '\n=========\n'
printf 'Test Case One: 1 producer and 1 consumer.\n'

printf 'Running producer: 1.\n'
python ../client/producer.py $1 $2 1 &
PID_PRODUCER=$!
sleep 10

printf 'Running consumer: 1.\n'
python ../client/consumer.py $1 $2 1

printf 'Killing producer: 1.\n'
kill $PID_PRODUCER

printf '\nTest Case One: Completed.\n'
printf '=========\n\n'