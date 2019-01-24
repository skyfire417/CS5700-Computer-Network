#!/bin/bash

tcps=('DropTail Reno' "DropTail Sack1" "RED Reno" "RED Sack1")

for(( i=0;i<${#tcps[@]};i++)) do
    # echo $var $i
    ns experiment_3.tcl ${tcps[i]}
done
