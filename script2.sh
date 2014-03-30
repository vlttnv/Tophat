#!/bin/bash
for i in {9000..9030}
do
		#python client/consumer.py 138.251.207.92 5000 $i
		ab -n 1000 -c 100 138.251.207.92:5000/get_data/$i &
done

# The magic line
#   $$ holds the PID for this script
#   Negation means kill by process group id instead of PID
trap "kill -TERM -$$" SIGINT
wait
