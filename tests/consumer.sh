#!/bin/bash

while :
do
	sleep 0.2
	python ../client/consumer.py 138.251.206.64 5000 $1
done
