"""
python mgen-client.py -- server-ip 192.168.0.2 --server-port 5000  --duration 30 --pkt-size 1024
python mgen-server.py  --server-port 5000  --duration 30
"""

import os
import sys
import argparse
from threading import Timer
from time import sleep
import time
import subprocess
import shutil

FLOWS_PER_PROCESS = 30
FLOW_NO = 1
SRC_PORT_NO = 5000


def process_mgen_output():
    pass

def run_mgen_test(filenames):
    #mgen input input.mgen txlog output outputtx.log
    for fname in filenames:
        #retcode = subprocess.call(["mgen", "input", fname,  "&"])
        p1 = subprocess.Popen(["mgen", "input", fname, "nolog"])
        print p1
    return

def writefile(filename, data):
    file = open(filename, "a")
    file.write(data)
    file.write("\n")
    file.close()

def write_mgen_file(args, fname, flowseqno, srcportno, totalflows, flowpersec, server_ip):
    # 0.0 ON 1 UDP SRC 192.168.0.1/5000  DST 192.168.0.2/5000 PERIODIC [1 1024]
    # 60.0OFF 1
    writefile(fname, "TXBUFFER 999999999999")
    iteration = int(totalflows) / int(flowpersec)
    flowno = flowseqno
    for i in range(0, iteration):
        for f in range (0, int(flowpersec)):
            d = str(i) + ".0 ON "+ str(flowno) + " " + args.protocol + " SRC " + str(srcportno) + " DST " + str(server_ip) + "/" + str(args.server_port) + " PERIODIC ["+ str(args.pkts_per_sec)+ " "+ str(args.pkt_size)+ "] " 
            flowno = flowno+1
            srcportno = srcportno + 1
            # print d
            writefile(fname, d)

    for i in range(flowseqno, flowno):
        d =  str(args.duration) + ".0 OFF " + str(i)
        # print d
        writefile(fname, d)

def main(argv):
    parser = argparse.ArgumentParser("Program for MGEN traffic analysis")
    parser.add_argument("--server-ip", required=True, help="Input Server IP",action="append")
    parser.add_argument("--server-port", required=True, help="Server Port")
    parser.add_argument("--duration", required=True, help="Measure Duration")
    parser.add_argument("--pkt-size", required=False, default=1024, help="Packet Size")
    parser.add_argument("--pkts-per-sec", required=False, default=1, help="Packet Size")
    parser.add_argument("--protocol", required=False, default="UDP", help="Protocol[UDP/TCP]")
    args = parser.parse_args(argv[1:])
    print args
 
    directory = "mgen"
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)
    filenames = []
    fileindex = 0
    for server in args.server_ip:
        if int(args.total_flows) <= FLOWS_PER_PROCESS:
            filename = directory +"/input"+ str(fileindex) +".mgen"
            filenames.append(filename)
            write_mgen_file(args, filename, FLOW_NO, SRC_PORT_NO, args.total_flows, args.flows_per_sec, server )
            fileindex +=1
        else:
            q = int(args.total_flows) / FLOWS_PER_PROCESS
            r = int(args.total_flows) % FLOWS_PER_PROCESS

            current_flow_no = FLOW_NO
            current_src_port_no = SRC_PORT_NO

            for p in range(0, q):
                filename = directory +"/input"+ str(fileindex) +".mgen"
                fileindex +=1
                filenames.append(filename)
                write_mgen_file(args, filename, current_flow_no, current_src_port_no, FLOWS_PER_PROCESS, int(args.flows_per_sec)/q , server)
                current_flow_no = current_flow_no + FLOWS_PER_PROCESS
                current_src_port_no = current_src_port_no + FLOWS_PER_PROCESS
    print filenames
    run_mgen_test(filenames)
    #process_mgen_output()
    
if __name__ == '__main__':
    main(sys.argv)
