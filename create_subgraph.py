import argparse
import subprocess
import os

#Date: 9 June 2020 (Happy birthday broski!)
#Author: Fiona J Whelan

#Motive: To use a list of gene IDs to create node and edge files for input into gephi.
#   --all will pull any edge that a gene in the list is associated with
#   --strict will pull only those edges between 2 genes in the gene ID list

parser = argparse.ArgumentParser()
parser.add_argument("--geneID", "-g", type=str, required=True) #list of geneIDs, one per line
parser.add_argument("--aedge",  "-a", type=str, required=True) #edge file output from coinfinder, associate
parser.add_argument("--dedge",  "-d", type=str, required=True) #edge file output from coinfinder, dissociate
parser.add_argument("--onode",  "-n", type=str, required=True) #node output with labels
parser.add_argument("--oedge",  "-o", type=str, required=True) #edge output with CoincidentType column to differentiate associations from dissociations
parser.add_argument("--strict", "-s", type=bool,required=False)#flag for strict, see above
parser.add_argument("--all",    "-f", type=bool,required=False)#flag for all, see above
args = parser.parse_args()

#Call compgen_subset-edge-list or edge-list-strict to get the node and edge file outputs
#Associate edge list
ret = ""
if (args.strict):
    ret = "python3 compgen_subset-edge-list-strict.py --genes "+args.geneID+" --edges "+args.aedge+" --outpu pipeline-temp-Aedges.tsv"
else:
    ret = "python3 compgen_subset-edge-list.py --genes "+args.geneID+" --edges "+args.aedge+" --outpu pipeline-temp-Aedges.tsv"
out = subprocess.getoutput(ret)
if (out != ""):
    print(ret)
    print(out)
ret = "cut -f 1 pipeline-temp-Aedges.tsv | sort - | uniq - > pipeline-temp1.txt"
out = subprocess.getoutput(ret)
if (out != ""):
    print(ret)
    print(out)
ret = "cut -f 2 pipeline-temp-Aedges.tsv | sort - | uniq - > pipeline-temp2.txt"
out = subprocess.getoutput(ret)
if (out != ""):
    print(ret)
    print(out)
ret = "cat pipeline-temp1.txt pipeline-temp2.txt | sort - | uniq - > pipeline-temp-Anodes.tsv"
out = subprocess.getoutput(ret)
if (out != ""):
    print(ret)
    print(out)
#Dissociate edge list
ret = ""
if (args.strict):
    ret = "python3 compgen_subset-edge-list-strict.py --genes "+args.geneID+" --edges "+args.dedge+" --outpu pipeline-temp-Dedges.tsv"
else:
    ret = "python3 compgen_subset-edge-list.py --genes "+args.geneID+" --edges "+args.dedge+" --outpu pipeline-temp-Dedges.tsv"
out = subprocess.getoutput(ret)
if (out != ""):
    print(ret)
    print(out)
ret = "cut -f 1 pipeline-temp-Dedges.tsv | sort - | uniq - > pipeline-temp1.txt"
out = subprocess.getoutput(ret)
if (out != ""):
    print(ret)
    print(out)
ret = "cut -f 2 pipeline-temp-Dedges.tsv | sort - | uniq - > pipeline-temp2.txt"
out = subprocess.getoutput(ret)
if (out != ""):
    print(ret)
    print(out)
ret = "cat pipeline-temp1.txt pipeline-temp2.txt | sort - | uniq - > pipeline-temp-Dnodes.tsv"
out = subprocess.getoutput(ret)
if (out != ""):
    print(ret)
    print(out)
#Combine them
ret = "perl -i -pe 's/\n/\tZAssociate\n/g' pipeline-temp-Aedges.tsv"
out = subprocess.getoutput(ret)
if (out != ""):
    print(ret)
    print(out)
ret = "perl -i -pe 's/\n/\tDissociate\n/g' pipeline-temp-Dedges.tsv"
out = subprocess.getoutput(ret)
if (out != ""):
    print(ret)
    print(out)
ret = "sed '1d' pipeline-temp-Dedges.tsv > pipeline-temp-Dedges-nohead.tsv"
out = subprocess.getoutput(ret)
if (out != ""):
    print(ret)
    print(out)
ret = "cat pipeline-temp-Aedges.tsv pipeline-temp-Dedges-nohead.tsv > "+args.oedge
out = subprocess.getoutput(ret)
if (out != ""):
    print(ret)
    print(out)
ret = "cat pipeline-temp-Dnodes.tsv pipeline-temp-Anodes.tsv > pipeline-temp-nodes.tsv"
out = subprocess.getoutput(ret)
if (out != ""):
    print(ret)
    print(out)
ret = "sort pipeline-temp-nodes.tsv | uniq - > pipeline-temp-nodes-uniq.tsv"
out = subprocess.getoutput(ret)
if (out != ""):
    print(ret)
    print(out)
ret = "python3 label_groups.py --mapps pa_mapping.txt --nodes pipeline-temp-nodes-uniq.tsv --onode "+args.onode
out = subprocess.getoutput(ret)
if (out != ""):
    print(ret)
    print(out)
#Remove temporary files
os.remove("pipeline-temp-Aedges.tsv")
os.remove("pipeline-temp1.txt")
os.remove("pipeline-temp2.txt")
os.remove("pipeline-temp-Anodes.tsv")
os.remove("pipeline-temp-Dedges.tsv")
os.remove("pipeline-temp-Dedges-nohead.tsv")
os.remove("pipeline-temp-Dnodes.tsv")
os.remove("pipeline-temp-nodes.tsv")
os.remove("pipeline-temp-nodes-uniq.tsv")
