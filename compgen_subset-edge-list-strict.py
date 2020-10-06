import argparse

#Author: Fiona J Whelan
#Date: 5 June 2020; 9 June 2020

#Motive: Take a gene list as input and to subset an edge list to only those edges *both* those genes is found in.

parser = argparse.ArgumentParser()
parser.add_argument("--genes", "-g", type=str, required=True) #list of gene IDs, one per line
parser.add_argument("--edges", "-e", type=str, required=True) #edge file, output of coinfinder
parser.add_argument("--outpu", "-o", type=str, required=True) #subset of edge file with genes
args = parser.parse_args()

#Store genes of interest in dictionary
gene_l = []
with open(args.genes) as genes:
    for line in genes:
        gene_l.append(line.rstrip())

#Cycle through edge file; write to outpu
out = open(args.outpu, 'w')
out.write("Source\tTarget\tpval\n")
with open(args.edges) as edges:
    for line in edges:
        group1 = line.rstrip().split("\t")[0]
        group2 = line.rstrip().split("\t")[1]
        if (group1 in gene_l and group2 in gene_l):
            out.write(line)
