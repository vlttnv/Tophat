#!/bin/bash

# To run the script:
#	chmod a+x start_producer.sh
#	./start_producer.sh balancer_addr balancer_port producer_id

#	$1 = balancer_addr: the IP address of the balancer server
#	$2 = balancer_port: the port of the balancer server
#	$3 = producer_id: the producer ID

python ../client/producer.py $1 $2 $3 &

trap "kill -TERM -$$" SIGINT
wait