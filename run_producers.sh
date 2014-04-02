#!/bin/bash

# The script runs multiple producers

# To run the script:
#	chmod a+x producers.sh
#	./producers.sh balancer_addr balancer_port producer_id num_producer

# $1 = balancer_addr : IP address of the balancer
# $2 = balancer_port : Port number of the balancer
# $3 = producer_id : ID of the starting producer
# $4 = num_producer : Number of producers

# e.g. ./producers.sh 138.251.206.64 5000 10 5
#
#		Producers 10, 11, 12, 13, 14 will send heartbeats.
#		All requests will be directed to 138.251.206.64:5000

balancer_addr=$1
balancer_port=$2
producer_id=$3
num_producer=$4

min=$producer_id
max=$(($min + $num_producer - 1))

printf '\nRunning producers: %s - %s.\n' "$min" "$max"
for i in $(seq $min $max)
do
	printf 'Running producer %s.\n' "$i"
	python client/producer.py $balancer_addr $balancer_port $i &
done

kill_all()
{
	kill $(ps aux | grep '[p]ython client/producer.py' | awk '{print $2}')
}

trap "kill_all" SIGINT
wait