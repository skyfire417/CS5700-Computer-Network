set ns [new Simulator]

# Get rate and tcp variant from command line
set rate [lindex $argv 0]
set tcp1 [lindex $argv 1]
set tcp2 [lindex $argv 2]
append rate Mb

# set output file name
set output exp2_
append output $tcp1 _ $tcp2
append output _$rate.tr
puts "$rate, $tcp1, $tcp2, $output"

# Open the trace file
set nf [open data/$output w]
$ns trace-all $nf

#Define a 'finish' procedure
proc finish {} {
    global ns nf
    $ns flush-trace
    # Close the trace file
    close $nf
    exit 0
}

#Define six nodes
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]

#Create links using DropTail
$ns duplex-link $n0 $n1 10Mb 10ms DropTail
$ns duplex-link $n1 $n4 10Mb 10ms DropTail
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n2 $n5 10Mb 10ms DropTail

#Create a UDP at node n2
set udp [new Agent/UDP]
$ns attach-agent $n1 $udp
#Create a sink at node n3
set null [new Agent/Null]
$ns attach-agent $n2 $null
# Create a CBR over udp
set cbr [new Application/Traffic/CBR]
$cbr set rate_ $rate
$cbr attach-agent $udp
$cbr set random_ false

# Create tcp v1 at node 1
set tcpv1 [new Agent/TCP/$tcp1]
$ns attach-agent $n0 $tcpv1
# Create tcp v1 sink at node 4
set sink1 [new Agent/TCPSink]
$ns attach-agent $n3 $sink1

# Create tcp v2 at node 5
set tcpv2 [new Agent/TCP/$tcp2]
$ns attach-agent $n4 $tcpv2
# Create tcp v2 sink at node 6
set sink2 [new Agent/TCPSink]
$ns attach-agent $n5 $sink2

# Connection
$ns connect $udp $null
$udp set fid_ 1
$ns connect $tcpv1 $sink1
$tcpv1 set fid_ 2
$ns connect $tcpv2 $sink2
$tcpv2 set fid_ 3

set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcpv1
set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcpv2

#Schedule events for the CBR agents
$ns at 0.0 "$cbr start"
$ns at 0.0 "$ftp1 start"
$ns at 0.0 "$ftp2 start"
$ns at 10.0 "$ftp1 stop"
$ns at 10.0 "$ftp2 stop"
$ns at 10.0 "$cbr stop"

#Run the simulation
$ns at 10.1 "finish"
$ns run
