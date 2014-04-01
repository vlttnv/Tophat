#!/bin/bash

# To run the script:
#	chmod a+x test_one.sh
#	./test_one.sh

balancer_addr=localhost
balancer_port=6000

worker_addr=localhost
worker_port=5000

printf '\n=========\n'
printf 'Test Case 4: 15 producers and 1 consumer. Validate the server database and cache.\n'

printf '\nRunning balancer @ %s:%s.\n' "$balancer_addr" "$balancer_port"
python ../balance.py $balancer_port &
sleep 3

printf '\nRunning worker @ %s:%s.\n' "$worker_addr" "$worker_port"
python ../run.py $worker_port $balancer_addr $balancer_port &
sleep 3

printf '\nRunning producers: 3000 - 3015.\n'
for i in {3000..3015}
do
	printf 'Running producer %s.\n' "$i"
	python ../client/producer.py $balancer_addr $balancer_port $i &
done

sleep 3
printf '\nKill the producers.\n'
kill $(ps aux | grep '[p]ython ../client/producer.py' | awk '{print $2}')

printf '\nRunning consumer: Ask data from producer 3214214.\n'
for i in {3000..3015}
do
	printf 'Running consumer: Ask data from producer %s.\n' "$i"
	python ../client/consumer.py $balancer_addr $balancer_port $i &
	sleep 3
done

printf '\nKill all background processes.\n'
kill $(ps aux | grep '[p]ython ../run.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ../balance.py' | awk '{print $2}')

printf '\nTest Case 4: Completed.\n'
printf '=========\n\n'
