import argparse
import os
import re
import subprocess

#Author: Fiona J. Whelan
#Date: 19 July 2019

#Motive: Count the number of overlapping edges between the STRING protein interaction network (with DR IDs converted to group IDs) and the number of co-occurring edges
#        Output: print lines with overlap values

parser = argparse.ArgumentParser()
parser.add_argument("--coin", "-m", type=str, required=True) #coincident edge output file from coinfinder
parser.add_argument("--ifna", "-p", type=str, required=True) #STRING db file with group IDs; string_to_groupID.links.v11.0.txt 
parser.add_argument("--outp", "-o", type=str, required=True) #output overlapping edges
args = parser.parse_args()

#Build dictionary of coincident edges (alphanumerically)
output = open(args.outp, 'w')
d_coins = {}
with open(args.coin) as coin:
    for line in coin:
        group1 = line.rstrip().split()[0] #","
        group2 = line.rstrip().split()[1] #","
        #Instead of writing the database code twice, if group2 is < group1, just swap the variables around
        if (group2 < group1):
            tmp = group1
            group1 = group2
            group2 = tmp
        #Add to dictionary
        if group1 in d_coins.keys():
            if group2 not in d_coins[ group1 ]:
                d_coins[ group1 ].append(group2)
        else:
            d_coins[ group1 ] = [ group2 ]

#Cycle through lines in STRING db file; count overlaps
overlap = 0
with open(args.ifna) as fna:
    for line in fna:
        node1 = line.rstrip().split(" ")[0]
        node2 = line.rstrip().split(" ")[1]
        #Check if group2 < group1
        if (node2 < node1):
            tmp = node1
            node1 = node2
            node2 = tmp
        #Overlapping nodes?
        if (node1 in d_coins.keys()):
            if (node2 in d_coins[ node1 ]):
                overlap+=1
                output.write(node1+"\t"+node2+"\n")

print("Overlap is: "+str(overlap))
