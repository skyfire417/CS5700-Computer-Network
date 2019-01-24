set title "Latency"
set datafile separator ","

set xlabel "CBR(Mbps)"
set ylabel "latency(s)"
set xrange [0:10]
set xtics 1,1,10
set yrange [0:0.11]
set ytics 0.01,0.01,0.11

set terminal eps
set output "exp2_la_Newreno_Reno.eps"

plot "latency.csv" using 1:4 w lp lw 2 pt 5 ps 0.6 title "Newreno", \
"latency.csv" using 1:5 w lp lw 2 pt 7 ps 0.6 title "Reno", \