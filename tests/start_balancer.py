#!/bin/bash

# To run the script:
#	chmod a+x start_consumer.sh
#	./start_consumer.sh balancer_port

#	$1 = port: the port of the balancer server

python ../balance.py $1 &

trap "kill -TERM -$$" SIGINT
wait