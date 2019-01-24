#!/bin/bash

tcps=('Reno Reno' "Newreno Reno" "Vegas Vegas" "Newreno Vegas")

for(( i=0;i<${#tcps[@]};i++)) do
    for j in {1..10}
    do
        # echo $var $i
        ns experiment_2.tcl $j ${tcps[i]}
    done
done
