#!/bin/bash

# To run the script:
#	chmod a+x all_test.sh
#	./all_test.sh

# Note: ports 6000, 5000, 5001, 5002 will be used

printf 'Make all test scripts executable.\n'
chmod a+x test_one.sh
chmod a+x test_two.sh
chmod a+x test_three.sh
chmod a+x test_four.sh
chmod a+x test_five.sh
chmod a+x test_six.sh

printf 'Run all test scripts.\n'
./test_one.sh
./test_two.sh
./test_three.sh
./test_four.sh
./test_five.sh
./test_six.sh