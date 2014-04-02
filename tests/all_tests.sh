#!/bin/bash

# To run the script:
#	chmod a+x all_test.sh
#	./all_test.sh

printf 'Make all test scripts executable.\n'
chmod a+x test_one.sh
chmod a+x test_two.sh
chmod a+x test_three.sh
chmod a+x test_four.sh

printf 'Run all test scripts.\n'
./test_one.sh
./test_two.sh
./test_three.sh
<<<<<<< HEAD
./test_four.sh
=======
./test_four.sh
>>>>>>> 4c491669f52a688c13280ff4dcb52184f9ce6b61
