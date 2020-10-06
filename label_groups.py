import csv
import re
import subprocess
import os
import argparse
import sys

#Author: Fiona J Whelan
#Date: 9 June 2020

#Motive: Add a Label column to the nodes file with the consensus gene name from the Pseudomonas dataset for labelling in gephi

#SQL query to obtain the pseudomonas gene name mappings:
#SELECT DISTINCT gene_cluster_id, name FROM pseudomonas.complete_genes INTO OUTFILE '/var/lib/mysql-files/pa_mapping.txt' FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';

#Parse arguments to get input file for reading
parser = argparse.ArgumentParser()
parser.add_argument("--mapps", "-m", type=str, required=True) #assumed: gene_cluster_id to gene name mapping as per sql query above
parser.add_argument("--nodes", "-n", type=str, required=True) #assumed: node file output from coinfinder
parser.add_argument("--onode", "-o", type=str, required=True) #output for the nodes mapping
args = parser.parse_args()

#Make dictionary of gene cluster names (keys) to pa gene name mappings:
gene_clusters = {}
header = []
with open(args.mapps) as mappfile:
    for mappline in mappfile:
        #Remove any of the following illegal characters- makes a myriad of issues in R later /:?",.|-()'
        name = mappline.split("\t")[1].rstrip()
        name = name.replace('/','').replace(':','').replace('?','').replace('"','').replace(',','').replace('.','').replace('|','').replace('-','').replace('(','').replace(')','').replace("'",'').replace("=",'').replace(' ','').replace('+','').replace('[','').replace(']','')
        gene_clusters[mappline.split("\t")[0]] = name

#Open node output file for write
nodeout = open(args.onode, "w")
nodeout.write("Id\tLabel\n")
mapp = ""
#Cycle through nodes file
with open(args.nodes) as nodefile:
    for line in nodefile:
        node = line.split("\t")[0]
        if node in gene_clusters.keys():
            mapp = gene_clusters[node]
        else:
            mapp = node
        nodeout.write(node+"\t"+node+"_"+mapp+"\n")
