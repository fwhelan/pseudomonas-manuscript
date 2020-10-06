import argparse

#Author: Fiona J Whelan
#Date: 26 November 2019

#Motive: Generate a .gexf file that contains all coincident pairs, with node colouring matching that of the gene associations and edge colouring matching that of whether association (red) or dissociation (blue)
#        and node colour matching whether the node is involved in both associating and dissociating relationships (black), only associating (white), or only dissociating (gray).

#Parser
parser = argparse.ArgumentParser()
parser.add_argument("--associate", "-a", type=str, required=True) #coinfinder edges output, association
parser.add_argument("--ass_nodes", "-n", type=str, required=True) #coinfinder nodes output, association
parser.add_argument("--dissociate","-d", type=str, required=True) #coinfinder edges output, dissociation
parser.add_argument("--dis_nodes", "-m", type=str, required=True) #coinfinder nodes output, dissociation
parser.add_argument("--output",    "-o", type=str, required=True) #output filename
args = parser.parse_args()
#Open output file & write header information
output = open(args.output, 'w')
output.write("<gexf xmlns=\"http://www.gexf.net/1.2draft\" version=\"1.2\" xmlns:viz=\"http://www.gexf.net/1.1draft/viz\">")
output.write("<graph mode=\"static\" defaultedgetype=\"undirected\">")
output.write("<attributes class=\"node\">")
output.write("<attribute id=\"D-value\" title=\"D-value\" type=\"double\"/>")
output.write("</attributes>")
output.write("<attributes class=\"edge\">")
output.write("<attribute id=\"p-value\" title=\"p-value\" type=\"double\"/>")
output.write("<attribute id=\"coincident-type\" title=\"coincident-type\" type=\"string\"/>")
output.write("</attributes>")
output.write("<nodes>")
#Create a list to keep track of nodes already written to file
l_nodes = []
#Create string of edge information to write at end of file
edge_attr_xml = ""
edge_counter = 0

#Load the D-value of all nodes into a dictionary
d_ass_nodes = {}
with open(args.ass_nodes) as nodes:
    line = nodes.readline() #skip header
    for line in nodes:
        d_ass_nodes[ line.rstrip().split("\t")[0] ] = line.rstrip().split("\t")[1]
d_dis_nodes = {}
with open(args.dis_nodes) as nodes:
    line = nodes.readline() #skip header
    for line in nodes:
        d_dis_nodes[ line.rstrip().split("\t")[0] ] = line.rstrip().split("\t")[1]

#Cycle through each file, adding to .gexf output file
with open(args.associate) as associate:
    line = associate.readline() #skip header
    for line in associate:
        group1 = line.rstrip().split("\t")[0]
        d1     = float(d_ass_nodes[ group1 ])
        group2 = line.rstrip().split("\t")[1]
        d2     = float(d_ass_nodes[ group2 ])
        pvalue = line.rstrip().split("\t")[2]
        #Colour node by component number
        #Colour: cream if unique to association
        #        black if common to association and dissociation
        #        gray  if unique to dissociation
        if ((group1 in d_ass_nodes) and (group1 in d_dis_nodes) and (d1 >= -0.4)):
            alpha1_col = "#000000" #black
        else:
            alpha1_col = "#f0f0f0" #cream
        if ((group2 in d_ass_nodes) and (group2 in d_dis_nodes) and (d2 >= -0.4)):
            alpha2_col = "#000000" #black
        else:
            alpha2_col = "#f0f0f0" #cream
        if (group1 not in l_nodes) and (d1 >= -0.4):
            output.write("<node id=\"" + group1 + "\" label=\"" + group1 + "\">\n" + "<attvalues>\n" + "  <attvalue for=\"D-value\" value=\"" + str(d1) + "\"/>\n" + " </attvalues>\n" + "<viz:color hex=\"" + alpha1_col + "\"/>" + "</node>\n")
            l_nodes.append(group1)
        if (group2 not in l_nodes) and (d2 >= -0.4):
            output.write("<node id=\"" + group2 + "\" label=\"" + group2 + "\">\n" + "<attvalues>\n" + "  <attvalue for=\"D-value\" value=\"" + str(d2) + "\"/>\n" + " </attvalues>\n" + "<viz:color hex=\"" + alpha2_col + "\"/>" + "</node>\n")
            l_nodes.append(group2)
        #Edges, red for association
        if (d1 >= -0.4) and (d2 >= -0.4):
            edge_attr_xml += "<edge id=\"" + str(edge_counter) + "\" label=\"" + str(edge_counter) + "\" source=\"" + group1 + "\" target=\"" + group2 + "\" weight=\"" + str(1) + "\">" + " <attvalues>\n" + "  <attvalue for=\"coincident-type\" value=\"" + "associate" + "\"/>\n" + "   <attvalue for=\"p-value\" value=\"" + str(pvalue) + "\"/>\n" + " </attvalues>\n" + "<viz:color r=\"255\" g=\"82\" b=\"82\"/>" + "</edge>\n"
            edge_counter = edge_counter+1

with open(args.dissociate) as dissociate:
    line = dissociate.readline() #skip header
    for line in dissociate:
        group1 = line.rstrip().split("\t")[0]
        d1     = float(d_dis_nodes[ group1 ])
        group2 = line.rstrip().split("\t")[1]
        d2     = float(d_dis_nodes[ group2 ])
        pvalue = line.rstrip().split("\t")[2]
        #Nodes
        alpha1_col = "#969696" #gray
        if (group1 not in l_nodes) and (d1 >= -0.4):
           output.write("<node id=\"" + group1 + "\" label=\"" + group1 + "\">\n" + "<attvalues>\n" + "  <attvalue for=\"D-value\" value=\"" + str(d1) + "\"/>\n" + " </attvalues>\n" + "<viz:color hex=\"" + alpha1_col + "\"/>" + "</node>\n")
           l_nodes.append(group1)
        if (group2 not in l_nodes) and (d2 >= -0.4):
           output.write("<node id=\"" + group2 + "\" label=\"" + group2 + "\">\n" + "<attvalues>\n" + "  <attvalue for=\"D-value\" value=\"" + str(d2) + "\"/>\n" + " </attvalues>\n" + "<viz:color hex=\"" + alpha1_col + "\"/>" + "</node>\n")
           l_nodes.append(group2)
        #Edges, blue for dissociation
        if (d1 >= -0.4) and (d2 >= -0.4):
            edge_attr_xml += "<edge id=\"" + str(edge_counter) + "\" label=\"" + str(edge_counter) + "\" source=\"" + group1 + "\" target=\"" + group2 + "\" weight=\"" + str(1) + "\">" + " <attvalues>\n" + "  <attvalue for=\"coincident-type\" value=\"" + "dissociate" + "\"/>\n" + "   <attvalue for=\"p-value\" value=\"" + str(pvalue) + "\"/>\n" + " </attvalues>\n" + "<viz:color r=\"25\" g=\"118\" b=\"210\"/>" + "</edge>\n"
            edge_counter = edge_counter+1

#Output to gexf file
output.write("</nodes>")
output.write("<edges>")
output.write(edge_attr_xml)
output.write("</edges>")
output.write("</graph>")
output.write("</gexf>")
