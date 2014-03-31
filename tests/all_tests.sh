#!/bin/bash

# make all test scripts executable
FILES=$(pwd)
printf 'Current directory: %s\n' "$FILES"

for f in $FILES
do
	printf 'Current file: %s\n' "$f"
done

for file in ./*
do
	echo $file
done

#
./test_one.sh


./test_two.sh