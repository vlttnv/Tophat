#!/bin/bash

# To run the script:
#	chmod a+x start_server.sh
#	./start_server.sh balancer_port

#	$1 = port: the port of the worker server
#	$2 = balancer_addr: the address of the balancer server
#	$3 = balancer_port: the port number of the balancer server

python ../run.py $1 $2 $3 &

trap "kill -TERM -$$" SIGINT
wait