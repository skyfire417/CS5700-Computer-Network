set title "Latency"
set datafile separator ","

set xlabel "Time(s)"
set ylabel "latency(s)"
set xrange [0:20]
set xtics 1,1,20


set terminal eps
set output "exp3_latency.eps"

plot "latency.csv" using 1:2 w lp lw 2 pt 5 ps 0.6 title "DropTail-Reno", \
"latency.csv" using 1:3 w lp lw 2 pt 7 ps 0.6 title "DropTail-Sack1", \
"latency.csv" using 1:4 w lp lw 2 pt 9 ps 0.6 title "RED-Reno", \
"latency.csv" using 1:5 w lp lw 2 pt 13 ps 0.6 title "RED-Sack1", \