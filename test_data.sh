#!/usr/bin/env bash

SIZES_OF_ARRAY=("5" "10" "15" "20" "25" "30" "35")
CONDUCTOR_X=("2" "5" "7" "10" "12" "15" "17")
CONDUCTOR_Y=("2" "5" "7" "10" "12" "15" "17")
CONDUCTOR_SIZE=("1" "2" "3" "4" "5" "6" "7")
CONDUCTOR_VALUE=("20" "50" "100" "200" "300" "400" "600")
NUMBER_OF_ITERATION=("10" "100" "1000" "10000" "20000" "30000" "40000")

for i in 0 1
do
    OUTFILE="parralel_algorithm_${SIZES_OF_ARRAY[$i]}_${CONDUCTOR_X[$i]}_${CONDUCTOR_Y[$i]}_${CONDUCTOR_SIZE[$i]}_${CONDUCTOR_VALUE[$i]}_${NUMBER_OF_ITERATION[$i]}"
    touch $OUTFILE
    for k in 1 2 3 4 5 6 7 8 9 10
    do
        CALC_TIME=$(TIMEFORMAT="%R"; { time ./run.sh ${SIZES_OF_ARRAY[$i]} ${CONDUCTOR_X[$i]} ${CONDUCTOR_Y[$i]} ${CONDUCTOR_SIZE[$i]} ${CONDUCTOR_VALUE[$i]} ${NUMBER_OF_ITERATION[$i]} sequential; }  2>&1 )
        echo "sequential=${CALC_TIME}\n" >> $OUTFILE
    done 
    for k in 1 2 3 4 5 6 7 8 9 10
    do
        CALC_TIME=$(TIMEFORMAT="%R"; { time ./run.sh ${SIZES_OF_ARRAY[$i]} ${CONDUCTOR_X[$i]} ${CONDUCTOR_Y[$i]} ${CONDUCTOR_SIZE[$i]} ${CONDUCTOR_VALUE[$i]} ${NUMBER_OF_ITERATION[$i]} parallel; }  2>&1 )
        echo "parallel=${CALC_TIME}\n" >> $OUTFILE
    done 
done

