import argparse
from collections import defaultdict
from joblib import Parallel, delayed
import threading
import subprocess

#Author: Fiona J. Whelan
#Date:   3 May 2019; edit 3 June 2020

#Motive: To, in parallel, count the instances of intersecting GO Terms across pairs of coincident or a random subset of abundant accessory genes.
#        Also, to count the number of genes in each of the 3 categories that do not have known GO Terms.

#Based on the output of the following SQL query:
#SELECT gene_cluster_id, accession, go_evidence_code FROM pseudomonas.complete_go_annotations2 INTO OUTFILE '/var/lib/mysql-files/go_terms.txt' FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';
#cat go_terms.txt | sort - | uniq - > go_terms.uniq.txt

#Parse arguments to get input file for reading
parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", type=str, required=True) #go_terms.uniq.txt
parser.add_argument("--edges", "-e", type=str, required=True) #edge file; format as output of coinfinder
parser.add_argument("--outpu", "-o", type=str, required=True) #stats output
parser.add_argument("--out",   "-p", type=str, required=True) #out write for intersecting GO Terms
args = parser.parse_args()

#Read in input file into dictionary of gene_cluster_id to set of GO Terms
#There might be multiple GO Terms per gene_cluster_id on multiple lines of the file
goannots = defaultdict(list)
with open(args.input) as golist:
    for goline in golist:
        goline = goline.rstrip()
        gobits = goline.split('\t')
        if str(gobits[1]) != '\\N':
            if gobits[0] in goannots:
                #gene_cluster_id exists; append GO Term to list
                (goannots[gobits[0]]).append(gobits[1])
            else:
                #first GO Term for gene_cluster_id; start list
                goannots[gobits[0]] = [gobits[1]]

#Define global variables to keep track of occurrences
no_data = 0
no_overlap = 0
ys_overlap = 0
out = open(args.out, 'w')

#Write function to cycle through edge list
def populate_goterms(line):
    group1 = line.split('\t')[0]
    group2 = line.split('\t')[1].rstrip()
    #Compare group1 and group2 GO Terms
    group1_GO_set = set(goannots[group1])
    group2_GO_set = set(goannots[group2])
    if (not group1_GO_set or not group2_GO_set):
        global no_data
        no_data += 1
    elif not group1_GO_set.intersection(group2_GO_set):
        global no_overlap
        no_overlap += 1
    else:
        global ys_overlap
        ys_overlap += 1
        #Write overlapping groups and terms to file
        for term in group1_GO_set.intersection(group2_GO_set):
            out.write(group1+"\t"+group2+"\t"+term+"\n")

edgesfile = open(args.edges, 'r')
line = next(edgesfile)
Parallel(n_jobs=40, require='sharedmem')(delayed(populate_goterms)(line) for line in edgesfile)

print("No data for x pairs: " + str(no_data))
print("Number of overlapping GO annotation pairs: " + str(ys_overlap))
print("Number of non-overlapping GO annotation pairs: " + str(no_overlap))

#Print output to file
output = open(args.outpu, 'w')
output.write("Input: " + args.input + "\n")
output.write("Edges: " + args.edges + "\n")
output.write("No data for x pairs\t"+str(no_data)+"\n")
output.write("Number of overlapping GO annotation pairs\t"+str(ys_overlap)+"\n")
output.write("Number of non-overlapping GO annotation pairs\t"+str(no_overlap)+"\n")
