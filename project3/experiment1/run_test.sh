#!/bin/bash

tcps=("TCP" "TCP/Reno" "TCP/Newreno" "TCP/Vegas")

for var in ${tcps[@]}
do
    for i in {1..10}
    do
        # echo $var $i
        ns experiment_1.tcl $i $var
    done
done