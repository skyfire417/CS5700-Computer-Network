set title "Throughput"
set datafile separator ","

set xlabel "Time(s)"
set ylabel "Throughput(Mbps)"
set xrange [0:20]
set xtics 1,1,20
set yrange [0:3.2]
set ytics 0.5,0.5,3

set terminal eps
set output "exp3_throughput.eps"

plot "throughput.csv" using 1:2 w lp lw 2 pt 5 ps 0.6 title "DropTail-Reno", \
"throughput.csv" using 1:3 w lp lw 2 pt 7 ps 0.6 title "DropTail-Sack1", \
"throughput.csv" using 1:4 w lp lw 2 pt 9 ps 0.6 title "RED-Reno", \
"throughput.csv" using 1:5 w lp lw 2 pt 13 ps 0.6 title "RED-Sack1", \