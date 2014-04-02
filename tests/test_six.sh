#!/bin/bash

# To run the script:
#	chmod a+x test_five.sh
#	./test_five.sh

# ports 6000, 5000, 5001, 5002 will be used

balancer_addr=localhost
balancer_port=6000

worker_addr=localhost
worker_one_port=5000
worker_two_port=5001
worker_three_port=5002

printf '\n=========\n'
printf 'Test Case 5: 15 producers, 3 workers, and 15 consumers. Handle worker failure. \n'

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

printf '\nRunning worker 3 @ %s:%s.\n' "$worker_addr" "$worker_three_port"
python ../run_worker.py $worker_three_port $balancer_addr $balancer_port &
sleep 3

printf '\nRunning producers: 4000 - 4015.\n'
for i in {4000..4015}
do
	printf 'Running producer: %s.\n' "$i"
	python ../client/producer.py $balancer_addr $balancer_port $i &
done
sleep 3

# consumers should get data successfully
for i in {4000..4015}
do
	printf 'Running consumer: Ask data from producer %s.\n' "$i"
	python ../client/consumer.py $balancer_addr $balancer_port $i &
	sleep 3
done
sleep 3

printf '\nStop workers.\n'
kill $(ps aux | grep '[p]ython ../run_worker.py' | awk '{print $2}')
sleep 3

# consumers should fail to get data
for i in {4000..4015}
do
	printf 'Running consumer: Ask data from producer %s.\n' "$i"
	python ../client/consumer.py $balancer_addr $balancer_port $i &
done

printf '\nRestart workers.\n'

printf '\nRunning worker 1 @ %s:%s.\n' "$worker_addr" "$worker_one_port"
python ../run_worker.py $worker_one_port $balancer_addr $balancer_port &

printf '\nRunning worker 2 @ %s:%s.\n' "$worker_addr" "$worker_two_port"
python ../run_worker.py $worker_two_port $balancer_addr $balancer_port &

printf '\nRunning worker 3 @ %s:%s.\n' "$worker_addr" "$worker_three_port"
python ../run_worker.py $worker_three_port $balancer_addr $balancer_port &

# consumers should get data successfully
for i in {4000..4015}
do
	printf 'Running consumer: Ask data from producer %s.\n' "$i"
	python ../client/consumer.py $balancer_addr $balancer_port $i &
	sleep 3
done
sleep 3

printf '\nStop all background processes.\n'
kill $(ps aux | grep '[p]ython ../client/producer.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ../run_worker.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ../run_balancer.py' | awk '{print $2}')

printf '\nTest Case 6: Completed.\n'
printf '=========\n\n'
