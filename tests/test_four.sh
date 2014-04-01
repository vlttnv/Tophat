#!/bin/bash

printf '\n=========\n'
printf 'Test Case 4: 15 producers and 1 consumer. Validate the server database and cache.\n'

for i in {1..15}
do
	printf 'Running producer %s.\n' "$i"
	python ../client/producer.py $1 $2 $i &
	PID_PRODUCER=$!
	sleep 3

	printf 'Killing producer: %s.\n' "$i"
	kill $PID_PRODUCER
done

for i in {1..15}
do
	printf 'Running consumer: Ask data from producer %s.\n' "$i"
	python ../client/consumer.py $1 $2 $i &
done

printf '\nTest Case 4: Completed.\n'
printf '=========\n\n'