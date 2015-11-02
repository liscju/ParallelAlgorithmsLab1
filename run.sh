#!/bin/bash

if [ $# -lt 5 ]; then
    echo "Usage():"
    echo "./run.sh size_of_array conductor_x conductor_y conductor_size conductor_value number_of_iteration"
    exit 1
fi

mpiexec -n $1 python main.py $2 $3 $4 $5 $6