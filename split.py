import sys
import os

parts=10
line_num=394955
with open(sys.argv[1],"rt") as fd:
    part = 0
    outfd = open(sys.argv[2]+"_part{}".format(part),"wt")
    for i,line in enumerate(fd):
        outfd.write(line)
        if i>(part+1)*(line_num/parts+1):
            part+=1
            outfd.close()
            outfd = open(sys.argv[2]+"_part{}".format(part),"wt")
    outfd.close()
