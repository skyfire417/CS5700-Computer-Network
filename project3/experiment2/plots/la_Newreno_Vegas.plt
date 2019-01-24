set title "Latency"
set datafile separator ","

set xlabel "CBR(Mbps)"
set ylabel "latency(s)"
set xrange [0:10]
set xtics 1,1,10
set yrange [0:1.2]
set ytics 0.1,0.1,1.2

set terminal eps
set output "exp2_la_Newreno_Vegas.eps"

plot "latency.csv" using 1:8 w lp lw 2 pt 5 ps 0.6 title "Newreno", \
"latency.csv" using 1:9 w lp lw 2 pt 7 ps 0.6 title "Vegas", \