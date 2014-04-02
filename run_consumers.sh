#!/bin/bash

# The script runs multiple consumers

# To run the script:
#	chmod a+x producers.sh
#	./producers.sh balancer_addr balancer_port producer_id num_producer

# $1 = balancer_addr : IP address of the balancer
# $2 = balancer_port : Port number of the balancer
# $3 = producer_id : ID of the starting producer
# $4 = num_producer : Number of producers

# e.g. ./consumers.sh 138.251.206.64 5000 10 5
#
#		Consumers will request data from producers 10, 11, 12, 13, 14.
#		Each consumer will request data from only one producer.
#		All requests will be directed to 138.251.206.64:5000

balancer_addr=$1
balancer_port=$2
producer_id=$3
num_producer=$4

min=$producer_id
max=$(($min + $num_producer - 1))

printf '\nRunning consumers - Request data from producers %s - %s.\n' "$min" "$max"
while :
do
	for i in $(seq $min $max)
	do
		printf 'Running consumer - Request data from producer %s.\n' "$i"
		python client/consumer.py $balancer_addr $balancer_port $i &
		sleep 0.1
	done
done

kill_all()
{
	kill $(ps aux | grep '[p]ython client/consumer.py' | awk '{print $2}')
}

trap "kill_all" SIGINT
wait