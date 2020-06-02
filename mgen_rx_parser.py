"""
schema:
{
    "flowno" : xx,
    "start_time": xxx,
    "end_time":xxx,
    "packet_size":xxx,
    "packets_received":xxx,
    "packets_lost":xxx,
    "current_seq_no":xxx
}
"""

import re
import sys
import argparse

log_db = {}

def get_kv_keys():
    global log_db
    return log_db.keys()

def update_kv(key, value):
    global log_db
    log_db[key] = value

def get_kv(key):
    global log_db
    if log_db.has_key(key):
        return log_db[key]
    else:
        log_db[key] = {
            "flowno": 0,
            "start_time": None,
            "end_time": None,
            "packet_size": 0,
            "packets_received": 0,
            "packets_lost": 0,
            "current_seq_no": 0
            }
        return log_db[key]


def print_kv():
    global log_db
    for key in log_db:
        print key, log_db[key]

def print_summarized_kv():
    global log_db
    pkt_revd_count = 0
    pkt_lost_count = 0
    Totalflows = 0
    for key in log_db:
         Totalflows = Totalflows + 1
         pkt_revd_count = pkt_revd_count + log_db[key]["packets_received"]
         pkt_lost_count = pkt_lost_count + log_db[key]["packets_lost"]

    print "Total Flows", Totalflows
    print "Packets Revd", pkt_revd_count
    print "Packets Lost", pkt_lost_count


def printresult(flows):
    print "***************************************************************************************"
    print "Flow no \t Start Time \t\t End Time \t PacketSize\t Packets Recived \t Packets Lost"
    print "***************************************************************************************"
    for flow in flows:
        print flow["flowno"], "\t", flow["start_time"], "\t", flow["end_time"], "\t\t",flow["packetsize"],"\t", flow["packets_revd"], "\t\t",flow["packets_lost"]
        print "-----------------------------------------------------------------------------------------------"


def print_summary(flows):
    print "Total Flows", len(flows)
    pkt_revd_count = 0
    pkt_lost_count = 0
    for flow in flows:
        pkt_revd_count = pkt_revd_count + flow["packets_revd"]
        pkt_lost_count = pkt_lost_count + flow["packets_lost"]
    print "Packets Revd", pkt_revd_count
    print "Packets Lost", pkt_lost_count

def calculate_packetloss():
    """
    iterate the inmemory-db 
    update the packetloss for each flow(last seqno - received pkts)
    """
    flows = get_kv_keys()
    for flow in flows:
        j = get_kv(flow)
        j["packets_lost"] = j["current_seq_no"] - j["packets_received"]
        update_kv(flow, j)

def calculate_per_flow(flowno, stime, seqno, packetsize):
    """
    Read the inmemory-db with key as flowno
    update the stattime, endtime,packetsize, seqno in the kv
    """
    j = get_kv(flowno)
    j["flowno"] = flowno
    if j["start_time"] is None:
        j["start_time"] = stime
    j["end_time"] = stime
    j["packet_size"] = packetsize
    j["current_seq_no"] = seqno
    j["packets_received"] = j["packets_received"] + 1
    update_kv(flowno, j)

def calculate_flow_metrics1(inputfname):
    """
    input : filename, flowno
    description:
      read the each line from the input log file,
      #04:10:50.112622 RECV proto>UDP flow>1 seq>1 src>10.1.4.44/1000 dst>10.1.4.44/5001 sent>04:10:50.112517 size>64 gps>INVALID,999.000000,999.000000,4294966297   
      filter with RECV event
      read sequence number,flowno,time,packetsize and pass it to calculate function.
           push this value to inmemory DB with flowno as key

    return :
    {flowno:xxx ,star_time: xxxx, end_time :xxxx, packets_revd: xxx, packets_lost :xxx }

    """
    file = open(inputfname, "r")
    for line in file:
        #print line
        match = re.match(r"(.*) RECV proto>(.*) flow>([0-9]+) seq>([0-9]+) (.*) (.*) (.*) size>([0-9]+)",line,re.M|re.I)
        if match:
            flowno = int(match.group(3))
            stime = match.group(1)
            seqno = int(match.group(4))
            packetsize = int(match.group(8))
            calculate_per_flow(flowno, stime, seqno, packetsize)
    calculate_packetloss()

def calculate_flow_metrics(inputfname, flowno):
    """
    input : filename, flowno
    description:
      read the each line from the input log file,
      #04:10:50.112622 RECV proto>UDP flow>1 seq>1 src>10.1.4.44/1000 dst>10.1.4.44/5001 sent>04:10:50.112517 size>64 gps>INVALID,999.000000,999.000000,4294966297   
      filter with RECV event and flowno
      read sequence number
      increase the packets received
    return :
    {flowno:xxx ,star_time: xxxx, end_time :xxxx, packets_revd: xxx, packets_lost :xxx }

    """
    starttime = None
    endtime = None
    packetsize = 0
    file = open(inputfname, "r")
    packetreceived = 0
    for line in file:
        #print line
        match = re.match(r"(.*) RECV proto>(.*) flow>%s seq>([0-9]+) (.*) (.*) (.*) size>([0-9]+)" % flowno,line,re.M|re.I)
        if match:
            packetreceived = packetreceived + 1
            currseqno = int(match.group(3))
            recvtime = match.group(1)
            if starttime is None:
                starttime = recvtime
            packetsize = int(match.group(7))
    file.close()
    packetlost = currseqno - packetreceived

    return(
        {
        "flowno": flowno, "start_time": starttime, "end_time": recvtime, "packetsize": packetsize,
        "packets_revd": packetreceived, "packets_lost": packetlost
        }
        )

# Main Routine
def main(argv):
    flows = []
    parser = argparse.ArgumentParser("Program for Parsing the MGEN RX LOG")
    parser.add_argument("-f", "--file-name", required=True, help="Input File Name")
    #parser.add_argument("-m", "--max-flow-no", required=True, help="Maximaum Flow Number")

    args = parser.parse_args(argv[1:])
    print args
    #for flow in range(1, int(args.max_flow_no)+1):
    #    flows.append(calculate_flow_metrics(args.file_name, flow))
    #printresult(flows)
    #print_summary(flows)
    calculate_flow_metrics1(args.file_name)
    print_kv()
    print_summarized_kv()



if __name__ == "__main__":
    main(sys.argv)
