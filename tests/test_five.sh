#!/bin/bash

# To run the script:
#	chmod a+x test_five.sh
#	./test_five.sh

balancer_addr=localhost
balancer_port=6000

worker_addr=localhost
worker_one_port=5000
worker_two_port=5001

printf '\n=========\n'
printf 'Test Case 5: 5 producers and 2 workers. Handle worker failure. \n'

printf '\nRunning balancer @ %s:%s.\n' "$balancer_addr" "$balancer_port"
python ../run_balancer.py $balancer_port &
sleep 3

printf '\nRunning worker 1 @ %s:%s.\n' "$worker_addr" "$worker_one_port"
python ../run_worker.py $worker_one_port $balancer_addr $balancer_port &
sleep 3

printf '\nRunning worker 2 @ %s:%s.\n' "$worker_addr" "$worker_two_port"
python ../run_worker.py $worker_two_port $balancer_addr $balancer_port &
PID_WORKER=$!
sleep 3

printf '\nRunning producers: 4000 - 4005.\n'
for i in {4000..4005}
do
	printf 'Running producer %s.\n' "$i"
	python ../client/producer.py $balancer_addr $balancer_port $i &
done

sleep 3
printf '\nStop worker 2.\n'
kill $PID_WORKER

sleep 3

printf '\nStop all background processes.\n'
kill $(ps aux | grep '[p]ython ../client/producer.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ../run_worker.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ../run_balancer.py' | awk '{print $2}')

printf '\nTest Case 5: Completed.\n'
printf '=========\n\n'
