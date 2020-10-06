import argparse
import subprocess
import glob
from joblib import Parallel,delayed
import re

#Author: Fiona J. Whelan
#Date:   29 May 2019

#Motive: Map all Pseudomonas aeruginosa genomes to the Pseudomonas aeruginosa RNA project that I've downloaded with download_fastq.py.

parser = argparse.ArgumentParser()
parser.add_argument("--rnaR1", "-1", type=str, required=True) #rna R1 
parser.add_argument("--rnaR2", "-2", type=str, required=True) #rna R2
parser.add_argument("--outpr", "-o", type=str, required=True) #prefix of output sam files
args = parser.parse_args()

#Cycle through all files to map, and map each
def map_rna(pathmapto, R1, R2, prefix):
    mapto = re.search(r'/.*/(.*?.fna)',pathmapto).group(1)
    print(pathmapto)
    print(mapto)
    ret = 0
    print("bowtie2-build "+pathmapto+" bowtie2-build-libs/"+mapto)
    ret = subprocess.call("bowtie2-build "+pathmapto+" bowtie2-build-libs/"+mapto, shell=True)
    if (ret !=0):
        output = open("log_"+mapto+".log", "w")
        output.write("bowtie2-build on "+mapto+" with prefix "+prefix+" failed with exit code "+str(ret)+"\n")
        return
    print("bowtie2 -x bowtie2-build-libs/"+mapto+" -p 1 -1 "+R1+" -2 "+R2+" -S "+prefix+"."+mapto+".sam")
    ret = subprocess.call("bowtie2 -x bowtie2-build-libs/"+mapto+" -p 1 -1 "+R1+" -2 "+R2+" -S "+prefix+"."+mapto+".sam", shell=True)
    if (ret !=0):
        output = open("log_"+mapto+".log", 'w')
        output.write("bowtie2 on "+mapto+" with prefix "+prefix+" failed with exit code "+str(ret)+"\n")
        return
    #Convert sam to bam to save space on device...
    print("samtools view -Sb "+prefix+"."+mapto+".sam > "+prefix+"."+mapto+".bam")
    ret = subprocess.call("samtools view -Sb "+prefix+"."+mapto+".sam > "+prefix+"."+mapto+".bam", shell=True)
    if (ret !=0):
        output = open("log_"+mapto+".log", 'w')
        output.write("samtools view on "+mapto+" with prefix "+prefix+" failed with exit code "+str(ret)+"\n")
        return
    #Remove sam file to save space on device...
    os.remove(prefix+"."+mapto+".sam")
    #Sort bam
    print("samtools sort "+prefix+"."+mapto+".bam > "+prefix+"."+mapto+".sort.bam")
    ret = subprocess.call("samtools sort "+prefix+"."+mapto+".bam > "+prefix+"."+mapto+".sort.bam", shell=True)
    if (ret !=0):
        output = open("log_"+mapto+".log", 'w')
        output.write("samtools sort on "+mapto+" with prefix "+prefix+" failed with exit code "+str(ret)+"\n")
        return
    #Remove bam file to save space on device...
    os.remove(prefix+"."+mapto+".bam")
    #Run bedtools genomecov
    print("bedtools genomecov -max 2 -ibam "+prefix+"."+mapto+".sort.bam > "+prefix+"."+mapto+".sort.bam.genomecov")
    ret = subprocess.call("bedtools genomecov -max 2 -ibam "+prefix+"."+mapto+".sort.bam > "+prefix+"."+mapto+".sort.bam.genomecov", shell=True)
    if (ret !=0):
        output = open("log_"+mapto+".log", 'w')
        output.write("bedtools genomecov on "+mapto+" with prefix "+prefix+" failed with exit code "+str(ret)+"\n")
        return
    #Remove sorted bam file to save space on device...
    os.remove(prefix+"."+mapto+".sort.bam")
    return


#Get list of all files to map
filelist = [ fil for fil in glob.glob("/data0/fwhelan/pseudomonas/complete-genomes/gff3-all/Pseudomonas_aeruginosa_*CDS.fna", recursive=True) ]

#Run mapping in parallel on filelist
Parallel(n_jobs=15)(delayed(map_rna)(k, args.rnaR1, args.rnaR2, args.outpr) for k in filelist)
