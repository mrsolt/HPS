import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, gSystem, TFile, gDirectory, gStyle, TCanvas, TH1, TImage
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-h':
			print_usage()
			sys.exit(0)

def openPDF(outfile,canvas):
	canvas.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	canvas.Print(outfile+".pdf]")

outfile = remainder[0]
infile = TFile(remainder[1])

i = 0
for c1 in infile.GetListOfKeys():
	c1 = c1.ReadObj()
	if(c1.ClassName() != "TCanvas"): continue
	i = i + 1
	output = outfile+str(i)
	openPDF(output,c1)
	c1.Print(output+".pdf")
	closePDF(output,c1)
