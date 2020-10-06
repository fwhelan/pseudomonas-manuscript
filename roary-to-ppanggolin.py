import argparse
import csv

#Author: Fiona J. Whelan
#Date:   7 April 2020

#Motive: Parse Roary's gene_presence_absence.csv into PPanGGoLiN's cluster input file format.

#Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--roary", "-r", type=str, required=True) #gene_p_a.csv
parser.add_argument("--pangl", "-p", type=str, required=True) #cluster file input to ppanggolin
args = parser.parse_args()

#Open pangl output file for writing
pangl = open(args.pangl, 'w')
#Cycle through Roary input file, writing each gene to pangl output file in <gene cluster>\t<gene ID>\n format
with open(args.roary) as roary:
    csvreader = csv.reader(roary, delimiter=',')
    next(csvreader, None) #skip header
    for line in csvreader:
        genecluster = line[0]
        geneIDs = line[14:]
        for geneID in geneIDs:
            if not (geneID == ""):
                #There is a geneID in this genome in this cluster; check whether there is >1 geneID in this genome
                geneIDarr = geneID.split( )
                for gene in geneIDarr:
                    if not (gene == ""):
                        pangl.write(genecluster+"\t"+gene+"\n")
pangl.close()
