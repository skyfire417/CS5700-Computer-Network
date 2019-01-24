set ns [new Simulator]

# Get rate and tcp variant from command line
set rate [lindex $argv 0]
set tcps [lindex $argv 1]
append rate Mb

# set output file name
set output exp1_
if {[lindex [split $tcps /] 1] != ""} {
    append output [lindex [split $tcps /] 1]
    append output _$rate.tr
} else {
    append output Tahoe
    append output _$rate.tr
}

puts "$rate, $tcps, $output"

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

# Create tcp at node 1
set tcp [new Agent/[lindex $argv 1]]
$ns attach-agent $n0 $tcp
# Create tcp sink at node 4
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
$ns at 0.0 "$cbr start"
$ns at 0.0 "$ftp start"
$ns at 10.0 "$ftp stop"
$ns at 10.0 "$cbr stop"



#Run the simulation
$ns at 10.0 "finish"
$ns run