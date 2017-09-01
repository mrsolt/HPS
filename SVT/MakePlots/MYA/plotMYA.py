import argparse
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import time

def plot(textFile1,textFile2,title,output,pdf):
    
    time1 = getArray(textFile1,1)
    time2 = getArray(textFile2,1) 
    var1 = getArray(textFile1,2)
    var2 = getArray(textFile2,2)
    plt.plot(time1, var1,"ro",label="2015")
    plt.plot(time2, var2,"bo",label="2016")
    plt.xlabel('time')
    plt.title(title)
    plt.xlim(0,60)
    #plt.legend([],["2015","2016"])
    #plt.legend()
    pdf.savefig()
    plt.clf()
                    

def getArray(textFile,j):
    inFile = open(textFile,"r")
    lines = inFile.readlines()[1:]
    readline=[]
    result = []
    for i in lines:
        readline.append(i.split()[j])
    inFile.close()  
    if(j == 1): result = convertTime(readline)
    if(j == 2): result = convertFloat(readline)
    return result

def convertTime(timeArray):
    result = []
    for i in range (len(timeArray)):
	result.append(time.strptime(timeArray[i], '%H:%M:%S'))
    return result

def convertFloat(varArray):
    result = []
    for i in range (len(varArray)):
	result.append(float(varArray[i]))
    return result

def main() : 

# Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--Output",   help="Output Directory")
    parser.add_argument("-i", "--Input",   help="Input Directory")

    args = parser.parse_args()

    #Output variables of interest
    plotVar = []
    plotVar.append("avdd:i_rd")
    plotVar.append("avdd:stat")
    plotVar.append("avdd:vf")
    plotVar.append("avdd:vn")
    plotVar.append("avdd:v_set_rd")
    #plotVar.append("dpm:dpm_rd")
    plotVar.append("dvdd:i_rd")
    plotVar.append("dvdd:stat")
    plotVar.append("dvdd:vf")
    plotVar.append("dvdd:vn")
    plotVar.append("dvdd:v_set_rd")
    plotVar.append("stat")
    plotVar.append("sync:sync_rd")
    plotVar.append("v125:i_rd")
    plotVar.append("v125:stat")
    plotVar.append("v125:vf")
    plotVar.append("v125:vn")
    plotVar.append("v125:v_set_rd")

    nFEBs = 10
    nHYBs = 4
    for k in range (len(plotVar)):
	output = args.Output + plotVar[k]
        pdf = PdfPages(output + ".pdf")
        for i in range (nFEBs):
	    for j in range (nHYBs):
		print str(i) + " " + str(j) + " " + plotVar[k]
	        feb = i
	        hybrid = j
  		inputFile2015 = args.Input + "Eng2015Mya/" + plotVar[k] + "/" + "feb_" + str(feb) + "_hyb_" + str(hybrid) + ".txt"
		inputFile2016 = args.Input + "Phys2016Mya/" + plotVar[k] + "/" + "feb_" + str(feb) + "_hyb_" + str(hybrid) + ".txt"
		title = "SVT:lv:" + str(feb) + ":" + str(hybrid) + ":" + plotVar[k]
	    	plot(inputFile2015,inputFile2016,title,output,pdf)	    
	pdf.close()

if __name__ == "__main__" : 
    main() 
