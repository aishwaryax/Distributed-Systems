#!/bin/bash
cd ../server/catalog/; python3  unit_test.py &

cd ../order/; python3 unit_test.py &

cd ../../frontend/; python3  unit_test.py 