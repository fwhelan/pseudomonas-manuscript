import argparse
import statistics

#Author: Fiona J. Whelan
#Date: 23 May 2019

#Motive: Calculate the mean syntenic distance between genes in a gene set.
#        Relies on the output of mean distance calculations for each gene pair as input (see Figure2a.py for eg)

#Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--pairs", "-n", type=str, required=True) #mean syntenic distance information for each gene pair
parser.add_argument("--comps", "-c", type=str, required=True) #_components.tsv output from coinfinder
parser.add_argument("--outpt", "-o", type=str, required=True) #output file
args = parser.parse_args()

#Read in the mean distance between each gene into a dictionary (alphabetically)
d_pairs = {}
with open(args.pairs) as pairs:
    for line in pairs:
        gene1 = line.rstrip().split("\t")[0]
        gene2 = line.rstrip().split("\t")[1]
        if gene1 < gene2:
            if gene1 not in d_pairs:
                d_pairs[gene1] = {}
            d_pairs[gene1][gene2] = float(line.rstrip().split("\t")[5])
        else:
            if gene2 not in d_pairs:
                d_pairs[gene2] = {}
            d_pairs[gene2][gene1] = float(line.tstrip().split("\t")[5])

#Cycle through each line of the component file; i.e. each component
#For each gene in the component, calculate the distance of it to each other (not already counted) gene, add distance to sum and interaction to count. Add gene to gene list
summ = 0
coun = 0
done_genes = []
output = open(args.outpt, 'w')
with open(args.comps) as comps:
    for line in comps:
        curco = line.rstrip().split("\t")[0]
        genes = line.rstrip().split("\t")[1].split(",")
        summ = 0
        coun = 0
        for geneA in genes:
            for geneB in genes:
                if geneB not in done_genes and geneA != geneB:
                    if geneA < geneB and geneA in d_pairs and geneB in d_pairs[geneA]:
                        summ += d_pairs[geneA][geneB]
                        coun += 1
                    elif geneB in d_pairs and geneA in d_pairs[geneB]:
                        summ += d_pairs[geneB][geneA]
                        coun +=1
            done_genes.append(geneA)
        #Mean distance = sum/count
        if coun != 0:
            mean = summ/coun
            #Output component number \t mean distance
            output.write(curco+"\t"+str(mean)+"\n")
