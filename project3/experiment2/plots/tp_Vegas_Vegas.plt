set title "Throughput"
set datafile separator ","

set xlabel "CBR(Mbps)"
set ylabel "Throughput(Mbps)"
set xrange [0:10]
set xtics 1,1,10

set terminal eps
set output "exp2_tp_Vegas_Vegas.eps"

plot "throughput.csv" using 1:6 w lp lw 2 pt 5 ps 0.6 title "Vegas", \
"throughput.csv" using 1:7 w lp lw 2 pt 7 ps 0.6 title "Vegas", \
