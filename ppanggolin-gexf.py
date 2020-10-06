import argparse
import subprocess
import re

#Author: Fiona J Whelan
#Date:   7 April 2020

#Motive: Adjust the colouring of ppanggolin output graph to match the colour component of the gene clusters output from coinfinder; colour any non-coinfinder gene gray.

#Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--gexfin", "-i", type=str, required=True) #the light gexf output from ppanggolin
parser.add_argument("--compon", "-c", type=str, required=True) #component file output from coinfinder
parser.add_argument("--roary",  "-r", type=str, required=True) #gene_p_a file output from roary
parser.add_argument("--gexfou", "-o", type=str, required=True) #output gexf with coinfinder colours
args = parser.parse_args()

#Define colour array
def componentLookup(ret):
    argument = ret % 276
    switcher = {
        1:"#7c0051", 2: "#76c3ff", 3: "#001106", 4: "#01ca10", 5: "#e56800", 6: "#0005a7", 7: "#0a3700", 8: "#0245ec", 9: "#e3db00", 10: "#671a00",
        11: "#00bf72", 12: "#ff9dd6", 13: "#f386ff", 14: "#d57600", 15: "#20000a", 16: "#ace967", 17: "#840019", 18: "#0094f7", 19: "#006695", 20: "#ff5bf7",
        21: "#b9007e", 22: "#ff89c7", 23: "#360093", 24: "#001733", 25: "#005a69", 26: "#d5dca2", 27: "#61cb00", 28: "#00338b", 29: "#26a600", 30: "#fdd268",
        31: "#ffbdca", 32: "#b9e590", 33: "#ff711b", 34: "#8ce9c7", 35: "#331300", 36: "#a40053", 37: "#02d6cf", 38: "#640015", 39: "#c90039", 40: "#fecdb7",
        41: "#230025", 42: "#008c51", 43: "#ea21dd", 44: "#7a63ff", 45: "#b43b00", 46: "#0068a7", 47: "#01cf41", 48: "#f6d633", 49: "#93a200", 50: "#61f0b9",
        51: "#ffbf91", 52: "#990015", 53: "#c4a8ff", 54: "#02d9b8", 55: "#f2007e", 56: "#ac8b00", 57: "#d0e072", 58: "#ffa368", 59: "#02b096", 60: "#02c1cc",
        61: "#ff8de1", 62: "#fc0072", 63: "#dea3ff", 64: "#c37d00", 65: "#03c4f4", 66: "#ff5dad", 67: "#8990ff", 68: "#d2d9d9", 69: "#b744f6", 70: "#380006",
        71: "#5a3700", 72: "#002a23", 73: "#392ad1", 74: "#238100", 75: "#ff673c", 76: "#9bddff", 77: "#b2e3c0", 78: "#89ef68", 79: "#00726c", 80: "#004376",
        81: "#5d9fff", 82: "#210052", 83: "#009e40", 84: "#ffac48", 85: "#9d1fd7", 86: "#d7d5ef", 87: "#7cf22c", 88: "#b7ddef", 89: "#a8a7ff", 90: "#008634",
        91: "#8c3300", 92: "#8400a7", 93: "#783900", 94: "#0099b3", 95: "#ff3628", 96: "#386700", 97: "#003c45", 98: "#7f7100", 99: "#001f5c", 100: "#b4a200",
        101: "#272200", 102: "#ff9ea3", 103: "#ff325c", 104: "#e19100", 105: "#c80024", 106: "#ff6a61", 107: "#3c5300", 108: "#b9d400", 109: "#fc2109", 110: "#3a3b00",
        111: "#024fd6", 112: "#5d7b00", 113: "#a90009", 114: "#006027", 115: "#6ab200", 116: "#016989", 117: "#4f005e", 118: "#016dbf", 119: "#29000b", 120: "#002700",
        121: "#659700", 122: "#ffc545", 123: "#d7d0ff", 124: "#910085", 125: "#0064db", 126: "#ffa9c8", 127: "#dc0034", 128: "#620028", 129: "#ff5664", 130: "#006842",
        131: "#441500", 132: "#ff7588", 133: "#9ce5da", 134: "#ff55cd", 135: "#c27fff", 136: "#004f31", 137: "#e2da91", 138: "#7bb4ff", 139: "#7c0051", 140: "#76c3ff",
        141: "#001106", 142: "#01ca10", 143: "#e56800", 144: "#0005a7", 145: "#0a3700", 146: "#0245ec", 147: "#e3db00", 148: "#671a00", 149: "#00bf72", 150: "#ff9dd6",
        151: "#f386ff", 152: "#d57600", 153: "#20000a", 154: "#ace967", 155: "#840019", 156: "#0094f7", 157: "#006695", 158: "#ff5bf7", 159: "#b9007e", 160: "#ff89c7",
        161: "#360093", 162: "#001733", 163: "#005a69", 164: "#d5dca2", 165: "#61cb00", 166: "#00338b", 167: "#26a600", 168: "#fdd268", 169: "#ffbdca", 170: "#b9e590",
        171: "#ff711b", 172: "#8ce9c7", 173: "#331300", 174: "#a40053", 175: "#02d6cf", 176: "#640015", 177: "#c90039", 178: "#fecdb7", 179: "#230025", 180: "#008c51",
        181: "#ea21dd", 182: "#7a63ff", 183: "#b43b00", 184: "#0068a7", 185: "#01cf41", 186: "#f6d633", 187: "#93a200", 188: "#61f0b9", 189: "#ffbf91", 190: "#990015",
        191: "#c4a8ff", 192: "#02d9b8", 193: "#f2007e", 194: "#ac8b00", 195: "#d0e072", 196: "#ffa368", 197: "#02b096", 198: "#02c1cc", 199: "#ff8de1", 200: "#fc0072",
        201: "#dea3ff", 202: "#c37d00", 203: "#03c4f4", 204: "#ff5dad", 205: "#8990ff", 206: "#d2d9d9", 207: "#b744f6", 208: "#380006", 209: "#5a3700", 210: "#002a23",
        211: "#392ad1", 212: "#238100", 213: "#ff673c", 214: "#9bddff", 215: "#b2e3c0", 216: "#89ef68", 217: "#00726c", 218: "#004376", 219: "#5d9fff", 220: "#210052",
        221: "#009e40", 222: "#ffac48", 223: "#9d1fd7", 224: "#d7d5ef", 225: "#7cf22c", 226: "#b7ddef", 227: "#a8a7ff", 228: "#008634", 229: "#8c3300", 230: "#8400a7",
        231: "#783900", 232: "#0099b3", 233: "#ff3628", 234: "#386700", 235: "#003c45", 236: "#7f7100", 237: "#001f5c", 238: "#b4a200", 239: "#272200", 240: "#ff9ea3",
        241: "#ff325c", 242: "#e19100", 243: "#c80024", 244: "#ff6a61", 245: "#3c5300", 246: "#b9d400", 247: "#fc2109", 248: "#3a3b00", 249: "#024fd6", 250: "#5d7b00",
        251: "#a90009", 252: "#006027", 253: "#6ab200", 254: "#016989", 255: "#4f005e", 256: "#016dbf", 257: "#29000b", 258: "#002700", 259: "#659700", 260: "#ffc545",
        261: "#d7d0ff", 262: "#910085", 263: "#0064db", 264: "#ffa9c8", 265: "#dc0034", 266: "#620028", 267: "#ff5664", 268: "#006842", 269: "#441500", 270: "#ff7588",
        271: "#9ce5da", 272: "#ff55cd", 273: "#c27fff", 274: "#004f31", 275: "#e2da91", 276: "#7bb4ff",
        0: "#7bb4ff"
    }
    return switcher.get(argument, "black")

#Define roary definitions
def roaryDefinition(num):
    numgenomes = 209
    percent = (num/numgenomes)*100
    if (percent >= 90): #(90% <= strains <= 100%) 
        return("core")
    elif (percent >=89): #(89% <= strains < 90%)
        return("soft core")
    elif (percent >= 15): #(15% <= strains < 89%)
        return("shell")
    elif (percent >=0): #(0% <= strains < 15%)
        return("cloud")
    return("")

#Open output file for writing
out = open(args.gexfou, 'w')

#Cycle through the input gexf, adding to the output gexf
with open(args.gexfin) as gexfin:
    #Add roary attribute to the header
    line = gexfin.readline() #xml version
    out.write(line)
    line = gexfin.readline() #gexf xmlns
    out.write(line)
    line = gexfin.readline() #graph mode
    out.write(line)
    line = gexfin.readline() #attributes class
    out.write(line)
    out.write("      <attribute id=\"12\" title=\"roary_definition\" type=\"string\" />\n")
    line = gexfin.readline()
    while(len(line)!=0):
        if ("<node id=" not in line):
            out.write(line)
            line = gexfin.readline()
            continue
        #Node id line; grab label i.e. gene cluster name
        group1 = re.search("<node id=\".*?\" label=\"(.*?)\">", line).group(1)
        #Get component name
        syscall = "grep -E \"," + group1 + ",|," + group1 + "$|\\s" + group1 + ",|\\s" + group1 + "$\" " + args.compon + " | cut -f 1"
        ret = subprocess.getoutput(syscall)
        col = ""
        if (ret != ""):
            col = componentLookup(int(ret))
        else:
            col = "#ffffff"
        out.write(line)
        line = gexfin.readline()
        out.write("        <viz:color hex=\""+col+"\" />\n")
        line = gexfin.readline() #viz size line
        out.write(line)
        line = gexfin.readline() #attvalues opening
        out.write(line)
        #Add roary definition attvalue
        syscall = "grep -E \"^\\\""+group1+"\\\"\" "+args.roary+" | cut -d, -f 4"
        num = subprocess.getoutput(syscall)
        #Remove quotes from num
        if ("\"" in num):
            numr = num.split("\"")
            if (len(numr) == 3):
                num = num.split("\"")[1]
            else:
                num=""
        else:
            num=""
        roa = ""
        if (num != ""):
            roa = roaryDefinition(int(num))
        else:
            roa = "other"
        out.write("          <attvalue for=\"12\" value=\""+roa+"\" />\n")
        line = gexfin.readline()
