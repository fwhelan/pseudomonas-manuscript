import argparse
import os
import re
import subprocess

#Author: Fiona J. Whelan
#Date:   18 July 2019

#Motive: Convert DR STRING IDs for Pseudomonas aeruginosa into group IDs based on concatenated BLAST output files.
#        Output: a STRING edge interaction file with group IDs in place of STRING IDs

parser = argparse.ArgumentParser()
parser.add_argument("--mapp", "-m", type=str, required=True) #concatenated BLAST outputs with the name of the genome as the first column (just in case); all_STRING.out_subset_cov85ident90.sortk3.txt
parser.add_argument("--ifna", "-p", type=str, required=True) #input path to STRING db file; raw_data/287.protein.links.v11.0.txt 
parser.add_argument("--outp", "-o", type=str, required=True) #output path for write of new STRING db file; string_to_groupID.links.v11.0.txt
args = parser.parse_args()

#Build dictionary of DR to group ID information
d_DRs = {}
with open(args.mapp) as mapp:
    line = mapp.readline()
    while line != '':
        DR = line.rstrip().split("\t")[2]
        while line.rstrip().split("\t")[2] == DR:
            #print(line.rstrip())
            gene = line.rstrip().split("\t")[1]
            #Check if gene is already in d_DRs[ DR ] list; if not, append.
            if DR in d_DRs.keys():
                if gene not in d_DRs[ DR ]:
                    d_DRs[ DR ].append(gene)
            else:
                d_DRs[ DR ] = [ gene ]
            line = mapp.readline()
            if line == '': #eof
                break

#Cycle through lines in input file; convert DRs to group IDs; output line to output file
output = open(args.outp, 'w')
with open(args.ifna) as fna:
    for line in fna:
        node1 = line.rstrip().split(" ")[0]
        node2 = line.rstrip().split(" ")[1]
        score = line.rstrip().split(" ")[2]
        #Get nodes
        if (node1 in d_DRs.keys()) and (node2 in d_DRs.keys()):
            group1 = d_DRs[ node1 ]
            group2 = d_DRs[ node2 ]
            #Print out all combinations of group1 and group2, each on separate lines
            for i in group1:
                for j in group2:
                    output.write(str(i)+" "+str(j)+" "+score+"\n")
