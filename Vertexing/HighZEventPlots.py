import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

tupleName = "ntuple"
ebeam = 1.05

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'ht:e:')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-t':
			tupleName = str(arg)
		if opt=='-e':
			ebeam = arg
		if opt=='-h':
			print_usage()
			sys.exit(0)

#gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

outfile = remainder[0]

file = TFile(remainder[1])
label = remainder[2]

events = file.Get(tupleName)

def saveTuplePlot(events,inHisto,nBinsX,minX,maxX,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBinsX,minX,maxX))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw()
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	del histo

def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,inHisto1,nBinsX,minX,maxX,nBinsY,minY,maxY))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw("COLZ")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	del histo

def openPDF(outfile,canvas):
	canvas.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	canvas.Print(outfile+".pdf]")

nBins = 50
nBins2 = 50
minVZ = 80
maxVZ = 130
minMass = 0
maxMass = 0.1 * ebeam

ParametersList = []
ParametersList.append("uncVZ")
ParametersList.append("uncM")
ParametersList.append("bscVY")
ParametersList.append("bscVX")
ParametersList.append("uncVY")
ParametersList.append("uncVX")
ParametersList.append("uncVY-(uncVZ-0.5)*uncPY/uncPZ")
ParametersList.append("uncVX-(uncVZ-0.5)*uncPX/uncPZ")
ParametersList.append("uncVY-(uncVZ-0.5)*uncPY/uncPZ")
ParametersList.append("uncVY")
ParametersList.append("-(uncVZ-0.5)*uncPY/uncPZ")
ParametersList.append("uncVY")
ParametersList.append("bscVY")
ParametersList.append("uncVZ")
ParametersList.append("sqrt(bscVX*bscVX+bscVY*bscVY)")
ParametersList.append("uncVZ")
ParametersList.append("uncVY")
ParametersList.append("uncVZ")
ParametersList.append("sqrt(uncVX*uncVX+uncVY*uncVY)")
ParametersList.append("uncVZ")
ParametersList.append("uncVX-(uncVZ-0.5)*uncPX/uncPZ")
ParametersList.append("uncVZ")
ParametersList.append("uncVY-(uncVZ-0.5)*uncPY/uncPZ")
ParametersList.append("uncVZ")
ParametersList.append("sqrt((uncVX-(uncVZ-0.5)*uncPX/uncPZ)**2+(uncVY-(uncVZ-0.5)*uncPY/uncPZ)**2)")
ParametersList.append("uncVZ")
ParametersList.append("sqrt((bscVX-(bscVZ-0.5)*bscPX/bscPZ)**2+(bscVY-(bscVZ-0.5)*bscPY/bscPZ)**2)")
ParametersList.append("uncVZ")
ParametersList.append("(pow((uncVX-(uncVZ)*uncPX/uncPZ-0.1)*cos(-0.2)-(uncVY-(uncVZ)*uncPY/uncPZ)*sin(-0.2),2)/0.64+pow((uncVX-(uncVZ)*uncPX/uncPZ)*sin(-0.2)+(uncVY-(uncVZ)*uncPY/uncPZ)*cos(-0.2),2)/0.16)")
ParametersList.append("uncVZ")
ParametersList.append("(uncVZ-0.5)/sqrt(uncCovZZ)")
ParametersList.append("uncVZ")
ParametersList.append("(uncVY-0.5)/sqrt(uncCovYY)")
ParametersList.append("uncVZ")
ParametersList.append("(uncVY+0.5)/sqrt(uncCovYY)")
ParametersList.append("uncVZ")
ParametersList.append("uncPX/uncPZ")
ParametersList.append("uncVZ")
ParametersList.append("uncPY/uncPZ")
ParametersList.append("uncVZ")

TrackParametersList = []
TrackParametersList.append("uncVZ")
TrackParametersList.append("uncM")
TrackParametersList.append("uncP")
TrackParametersList.append("eleP")
TrackParametersList.append("posP")
TrackParametersList.append("uncChisq")
TrackParametersList.append("bscChisq")
TrackParametersList.append("bscChisq-uncChisq")
#TrackParametersList.append("eleTrkExtrpYAxialTopL1")
#TrackParametersList.append("posTrkExtrpYAxialTopL1")
#TrackParametersList.append("eleTrkExtrpYAxialBotL1")
#TrackParametersList.append("posTrkExtrpYAxialBotL1")
#TrackParametersList.append("eleTrkExtrpYSensorAxialTopL1")
#TrackParametersList.append("posTrkExtrpYSensorAxialTopL1")
#TrackParametersList.append("eleTrkExtrpYSensorAxialBotL1")
#TrackParametersList.append("posTrkExtrpYSensorAxialBotL1")
TrackParametersList.append("(uncVZ-0.5)/sqrt(uncCovZZ)")
TrackParametersList.append("(uncVY-0.5)/sqrt(uncCovYY)")
TrackParametersList.append("(uncVY+0.5)/sqrt(uncCovYY)")
TrackParametersList.append("uncPX/uncPZ")
TrackParametersList.append("uncPY/uncPZ")

openPDF(outfile,c)

#saveTuplePlot(events,"uncM",30,0,0.1,outfile,c,"uncM","","L2L2 High Z Events " + label)
#saveTuplePlot(events,"uncP",30,0,1.5,outfile,c,"uncP","","L2L2 High Z Events " + label)

for i in range(len(TrackParametersList)):
	par = TrackParametersList[i]
	minimum = ""#TrackParametersListMin[i]
	maximum = ""#TrackParametersListMax[i]
	saveTuplePlot(events,par,nBins2,minimum,maximum,outfile,c,par,"","L2L2 High Z Events " + label)

for i in range(len(ParametersList)/2):
	par2 = ParametersList[2*i]
	par1 = ParametersList[2*i+1]
	minimum2 = ""#ParametersListMin[2*i]
	maximum2 = ""#ParametersListMax[2*i]
	minimum1 = ""#ParametersListMin[2*i+1]
	maximum1 = ""#ParametersListMax[2*i+1]
	saveTuplePlot2D(events,par1,par2,nBins,minimum1,maximum1,nBins,minimum2,maximum2,outfile,c,par1,par2,"L2L2 High Z Events " + label,1)

closePDF(outfile,c)