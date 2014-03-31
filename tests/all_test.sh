#!/bin/bash

# To run the script:
#	chmod a+x all_test.sh
#	./all_test.sh balancer_addr balancer_port

#	$1 = balancer_addr: the IP address of the balancer server
#	$2 = balancer_port: the port of the balancer server

printf 'Make all test scripts executable.\n'
chmod a+x test_one.sh
chmod a+x test_two.sh

printf 'Run all test scripts.\n'
printf 'Make requests to the balancer @ $1:$2'
./test_one.sh $1 $2
./test_two.sh $1 $2