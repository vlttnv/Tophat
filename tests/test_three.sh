#!/bin/bash

printf '\n=========\n'
printf 'Test Case 3: 1 consumer. Ask data from a producer that does not exist in the database.\n'

printf 'Running consumer: Ask data from producer -13214214.\n'
python ../client/consumer.py $1 $2 -13214214

printf '\nTest Case 3: Completed.\n'
printf '=========\n\n'