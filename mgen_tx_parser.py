import re
import sys
import argparse


def printresult(flows):
    for flow in flows:
        print "*************************************************"
        print "flow no ", flow["flowno"]
        print "start time", flow["startime"]
        print "stop time", flow["stoptime"]
        print "sent packet", flow["sent_packet"]
        print "Lost Packet", flow["packet_loss"]


def findflows(filename):
    """
    input : filename
    description:
      read the each line from the input log file,
      filter ON and OFF events
      identify the flow no and start,stop time and populate the dictionary as below,
      {flowno: 1, starttime:06:11:32.686454, stoptime:06:11:32.686454 }
       # 06:11:32.686454 ON flow>1 srcPort>5001 dst>10.24.0.3/5001
       # 06:12:32.688798 OFF flow>1 srcPort>5001 dst>10.24.0.3/5001

    return :
        list of dictionary Ex: [{flowno: 1, starttime:06:11:32.686454, stoptime:06:11:32.686454 },
        {flowno: 2, starttime:06:11:32.686454, stoptime:06:11:32.686454 }]

    """
    flows = []
    file = open(filename, "r")
    for line in file:
        match = re.match(r'(.*) ON flow>([0-9]+)',line,re.M|re.I)
        if match:
            flows.append({"flowno": match.group(2), "startime":  match.group(1)})
            continue
        match = re.match(r'(.*) OFF flow>([0-9]+)',line,re.M|re.I)
        if match:
            for f in flows:
                if f["flowno"] == match.group(2):
                    f["stoptime"] = match.group(1)
    file.close()
    return flows


def calculate_flow_metrics(inputfname, flowno):
    """
    input : filename
    description:
      read the each line from the input log file,
      filter with SEND event and flowno
      read sequence number
      increase the packets sent
      if the (current sequence number - prev sequence number) Not Equal to  1, add the result -1 to packet loss counter
      continue till the end
      #06:11:32.686477 SEND proto>UDP flow>1 seq>1 srcPort>5001 dst>10.24.0.3/5001 size>1240     
          {flowno: startime: xxxx, endtime :xxxx, Number of Pkts Sent: xxx,  Lost Packets : }

    return :

    """
    file = open(inputfname, "r")
    packetcount = 0
    for line in file:
        #print line
        match = re.match(r"(.*) SEND proto>(.*) flow>%s seq>([0-9]+)" % flowno,line,re.M|re.I)
        if match:
            packetcount = packetcount + 1
            currseqno = int(match.group(3))
            #print currseqno
            #flows.append({"flowno": match.group(2), "startime":  match.group(1)})
    file.close()
    packetloss = currseqno - packetcount
    return (packetcount, packetloss)


# Main Routine
def main(argv):
    parser = argparse.ArgumentParser("Program for Parsing the MGEN TX LOG")
    parser.add_argument("-f", "--file-name", required=True, help="Input File Name")
    args = parser.parse_args(argv[1:])
    print args
    flows = []
    flows = findflows(args.file_name)
    for flow in flows:
        flow['sent_packet'], flow['packet_loss'] = calculate_flow_metrics(args.file_name, flow["flowno"])
    printresult(flows)


if __name__ == "__main__":
    main(sys.argv)
