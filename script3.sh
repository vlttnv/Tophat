#!/bin/bash
for i in {9000..9200}
do
		../bin/python client/producer.py -lP $i 138.251.207.92 5000 $i &
done

# The magic line
#   $$ holds the PID for this script
#   Negation means kill by process group id instead of PID
trap "kill -TERM -$$" SIGINT
wait