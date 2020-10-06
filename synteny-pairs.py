import argparse
import statistics

#Author: Fiona J. Whelan
#Date: 23 May 2019

#Motive: Calculate the mean distance between 2 gene clusters based on their start and end locations in the genomes in which they overlap.

#Synteny mapping file created from SQL using the following query.
#SELECT gene_cluster_id,genome_id,start,end,seqid FROM pseudomonas.complete_genes INTO OUTFILE '/var/lib/mysql-files/gene-cluster-id_synteny_mapping-seqid.txt' FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';

parser = argparse.ArgumentParser()
parser.add_argument("--mapp", "-m", type=str, required=True) #output of sql query w/ seqid
parser.add_argument("--glen", "-l", type=str, required=True) #genome.lengths; made by pulling the sequence-regions out of the gff files for all genomes
parser.add_argument("--pair", "-p", type=str, required=True) #_pairs.tsv output from coinfinder
parser.add_argument("--outp", "-o", type=str, required=True) #output file
args = parser.parse_args()

#Build dictionary of dictionaries of gene start/end information
##CAVEAT: THIS REQUIRES SORTED INPUT BY GENE CLUSTER (COLUMN 1)
d_clusters = {}
with open(args.mapp) as mapp:
    line = mapp.readline()
    while line:
        cur_cluster = line.rstrip().split("\t")[0]
        d_clusters[cur_cluster] = {}
        while(line.rstrip().split("\t")[0] == cur_cluster):
            genome = line.rstrip().split("\t")[1]
            start  = line.rstrip().split("\t")[2]
            end    = line.rstrip().split("\t")[3]
            seqid  = line.rstrip().split("\t")[4]
            #Adjust order if start > end; make life easier in the next bit of work
            if start > end:
                tmp = start
                start = end
                end = tmp
            d_clusters[cur_cluster][genome] = [ start, end, seqid ]
            line = mapp.readline()

#Build dictionary of genome length information
d_genlengths = {}
with open(args.glen) as glen:
    line = glen.readline()
    while line:
        strain = line.rstrip().split(" ")[0]
        gentyp = line.rstrip().split(" ")[1]
        genstr = int(line.rstrip().split(" ")[2])
        genend = int(line.rstrip().split(" ")[3])
        #All genome starts should be 1, right?
        if (genstr != 1):
            print("Genome start doesn't equal 1\n"+line)
            print(strain+"\n"+gentyp+"\n"+genstr+"\n"+genend+"\n")
        d_genlengths[ strain, gentyp ] = genend
        line = glen.readline()

#Cycle through all gene cluster sets and calculate D
output = open(args.outp, 'w')
with open(args.pair) as pair:
    line = pair.readline() #skip header
    for line in pair:
        group1 = line.rstrip().split("\t")[0]
        group2 = line.rstrip().split("\t")[1]
        pvalue = line.rstrip().split("\t")[2]
        obrate = int(line.rstrip().split("\t")[4])/int(line.rstrip().split("\t")[5]) #successes / observations = observed rate
        exrate = line.rstrip().split("\t")[6]
        if group1 not in d_clusters:
            continue
        genomes_g1 = list(d_clusters[group1].keys())
        if group2 not in d_clusters:
            continue
        genomes_g2 = list(d_clusters[group2].keys())
        #Find the intersecting genomes; genomes where both gene cluster 1 and 2 are in
        intersect = list(set(genomes_g1) & set(genomes_g2))
        list_d = []
        if(len(intersect)>0):
            for genome in intersect:
                start_g1 = int(d_clusters[group1][genome][0])
                end_g1   = int(d_clusters[group1][genome][1])
                seqid_g1 = d_clusters[group1][genome][2]
                start_g2 = int(d_clusters[group2][genome][0])
                end_g2   = int(d_clusters[group2][genome][1])
                seqid_g2 = d_clusters[group2][genome][2]
                #Be sure g1 and g2 are on the same chromosome/plasmid etc.
                if (seqid_g1 == seqid_g2):
                    #Collect length of genome information
                    genlength = d_genlengths[ genome, seqid_g1 ]
                    #Calculate distance between g1 and g2 in genome
                    if end_g1 < start_g2:
                        std = start_g2 - end_g1
                        crc = (start_g1 - 1) + (genlength - end_g2)
                        d = min(std, crc)
                    elif end_g2 < start_g1:
                        std = start_g1 - end_g2
                        crc = (start_g2 - 1) + (genlength - end_g1)
                        d = min(std, crc)
                    else: #overlapping
                        d = 0
                    #Debug
                    if d<0:
                        print("group1: "+group1+"\n")
                        print("genomes_g1: "+str(genomes_g1)+"\n")
                        print("genomes_g2: "+str(genomes_g2)+"\n")
                        print(str(intersect))
                        print(line.rstrip())
                        print(str(genlength))
                        print(genome)
                        print(seqid_g1)
                        print(str(start_g1) +" "+ str(end_g1) +" "+ str(start_g2) +" "+ str(end_g2))
                        print(d)
                        quit()
                    list_d.append(d)
        #Check to see if there was no intersection
        if(len(list_d)==0):
            list_d.append(-1)
            continue
        D = statistics.mean(list_d)
        output.write(group1 +"\t"+ group2 +"\t"+ str(pvalue) +"\t"+ str(obrate) +"\t"+ str(exrate) +"\t"+ str(D) +"\n")
