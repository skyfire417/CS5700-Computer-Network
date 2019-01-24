set title "Throughput"
set datafile separator ","

set xlabel "CBR(Mbps)"
set ylabel "Throughput(Mbps)"
set xrange [0:10]
set xtics 1,1,10

set terminal eps
set output "exp2_tp_Reno_Reno.eps"

plot "throughput.csv" using 1:2 w lp lw 2 pt 5 ps 0.6 title "Reno", \
"throughput.csv" using 1:3 w lp lw 2 pt 7 ps 0.6 title "Reno", \
