set ns [new Simulator]

# Get rate and tcp variant from command line
set algorithm [lindex $argv 0]
set tcps [lindex $argv 1]

# set output file name
set output exp3_
append output $algorithm _ $tcps.tr
puts "$algorithm, $tcps, $output"

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

#Create links
$ns duplex-link $n0 $n1 10Mb 10ms $algorithm
$ns duplex-link $n1 $n4 10Mb 10ms $algorithm
$ns duplex-link $n1 $n2 10Mb 10ms $algorithm
$ns duplex-link $n2 $n3 10Mb 10ms $algorithm
$ns duplex-link $n2 $n5 10Mb 10ms $algorithm

# set queue limit
$ns queue-limit	$n0 $n1 10
$ns queue-limit	$n1 $n4 10
$ns queue-limit	$n1 $n2 10
$ns queue-limit	$n2 $n3 10
$ns queue-limit	$n2 $n5 10

# #Create a UDP at node n5
set udp [new Agent/UDP]
$ns attach-agent $n4 $udp
# #Create a sink at node n6
set null [new Agent/Null]
$ns attach-agent $n5 $null
# # Create a CBR over udp
set cbr [new Application/Traffic/CBR]
$cbr set rate_ 8Mb
$cbr attach-agent $udp
$cbr set random_ false

# Create tcp at node 1
set tcp [new Agent/TCP/$tcps]
$ns attach-agent $n0 $tcp
# Create tcp v1 sink at node 4
set sink [new Agent/TCPSink]
$ns attach-agent $n3 $sink

# Connection
$ns connect $udp $null
$udp set fid_ 1
$ns connect $tcp $sink
$tcp set fid_ 2

set ftp [new Application/FTP]
$ftp attach-agent $tcp

#Schedule events for the CBR agents
$ns at 4.0 "$cbr start"
$ns at 0.0 "$ftp start"
$ns at 20.0 "$ftp stop"
$ns at 20.0 "$cbr stop"

# #Run the simulation
$ns at 20.1 "finish"
$ns run
