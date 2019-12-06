#!/bin/bash

find ./lib -name test -o -name tests -o -name idle_test | xargs rm -r

rm -r ./include ./lib/pkgconfig ./lib/python3.7/config-3.7m-darwin
rm ./bin/2to3* ./bin/easy_install* ./bin/idle* ./bin/pip* ./bin/pydoc*
rm ./bin/python*-config ./bin/pyvenv*
rm ./bin/miniterm.py* 

find ./lib -name "*.pyc" -delete
find ./lib -name __pycache__ -delete 

./bin/python3.7 -m compileall -b -f ./lib/python3.7
find ./lib -name "*.py" | grep -v "/site-packages/mu/" | while read FILE
do
    rm ${FILE}
done
