set title "Dropate"
set datafile separator ","

set xlabel "CBR(Mbps)"
set ylabel "drop_rate"
set xrange [0:10]
set xtics 1,1,10
set yrange [0:0.7]
set ytics 0.1,0.1,0.7

set terminal eps
set output "exp2_dr_Vegas_Vegas.eps"

plot "drop_rate.csv" using 1:6 w lp lw 2 pt 5 ps 0.6 title "Vegas", \
"drop_rate.csv" using 1:7 w lp lw 2 pt 7 ps 0.6 title "Vegas", \
