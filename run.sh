#!/bin/bash

if [ $# -lt 7 ]; then
    echo "Usage():"
    echo "./run.sh size_of_array conductor_x conductor_y conductor_size conductor_value number_of_iteration [sequential|parallel]"
    exit 1
fi

if [ $7 == "parallel" ]; then
    mpiexec -n $1 python main.py $2 $3 $4 $5 $6 parallel
fi

if [ $7 == "sequential" ]; then
    python main.py $1 $2 $3 $4 $5 $6 sequential
fi

