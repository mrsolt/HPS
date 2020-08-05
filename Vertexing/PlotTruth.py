import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

def saveTuplePlot(events,inHisto,nBins,minX,maxX,outfile,canvas,setLog=False):
	if(not setLog): canvas.SetLogy(0)
	else: canvas.SetLogy(1)
	events.Draw("{0}>>({1},{2},{3})".format(inHisto,nBins,minX,maxX))
	canvas.Print(outfile+".pdf")

def saveTuplePlot2D(events,inHistoX,inHistoY,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas):
	canvas.SetLogy(0)
	events.Draw("{0}:{1}>>({2},{3},{4},{5},{6},{7})".format(inHistoY,inHistoX,nBinsX,minX,maxX,nBinsY,minY,maxY),"","COLZ")
	canvas.Print(outfile+".pdf")

def openPDF(outfile,canvas):
	canvas.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	canvas.Print(outfile+".pdf]")

nBins = 100
eBeam = 1.05
nEcalHits = 3
nLay = 6

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hn:E:e:l:')

# Parse the command line arguments
for opt, arg in options:
	if opt=='-n':
        	nBins = int(arg)
    	if opt=='-E':
        	eBeam = float(arg)
    	if opt=='-e':
       		nEcalHits = int(arg)
    	if opt=='-l':
     		nLay = int(arg)
    	if opt=='-h':
        	print_usage()
        	sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

outfile = remainder[0]
infile = TFile(remainder[1])

events = infile.Get("ntuple")

truthOutfile = outfile + "_truth"

openPDF(truthOutfile,c)
saveTuplePlot(events,"ele1energy",nBins,0,eBeam*1.3,truthOutfile,c)
saveTuplePlot(events,"ele1Px",nBins,-eBeam*0.1,eBeam*0.1,truthOutfile,c)
saveTuplePlot(events,"ele1Py",nBins,-eBeam*0.1,eBeam*0.1,truthOutfile,c)
saveTuplePlot(events,"ele1Pz",nBins,0,eBeam*1.3,truthOutfile,c)
saveTuplePlot(events,"ele1startX",nBins,-100,100,truthOutfile,c)
saveTuplePlot(events,"ele1startY",nBins,-100,100,truthOutfile,c)
saveTuplePlot(events,"ele1startZ",nBins,-10,150,truthOutfile,c)
saveTuplePlot(events,"ele1endX",nBins,-400,400,truthOutfile,c)
saveTuplePlot(events,"ele1endY",nBins,-150,150,truthOutfile,c)
saveTuplePlot(events,"ele1endZ",nBins,-10,150,truthOutfile,c)

saveTuplePlot(events,"ele2energy",nBins,0,eBeam*1.3,truthOutfile,c)
saveTuplePlot(events,"ele2Px",nBins,-eBeam*0.1,eBeam*0.1,truthOutfile,c)
saveTuplePlot(events,"ele2Py",nBins,-eBeam*0.1,eBeam*0.1,truthOutfile,c)
saveTuplePlot(events,"ele2Pz",nBins,0,eBeam*1.3,truthOutfile,c)
saveTuplePlot(events,"ele2startX",nBins,-100,100,truthOutfile,c)
saveTuplePlot(events,"ele2startY",nBins,-100,100,truthOutfile,c)
saveTuplePlot(events,"ele2startZ",nBins,-10,150,truthOutfile,c)
saveTuplePlot(events,"ele2endX",nBins,-400,400,truthOutfile,c)
saveTuplePlot(events,"ele2endY",nBins,-150,150,truthOutfile,c)
saveTuplePlot(events,"ele2endZ",nBins,-10,150,truthOutfile,c)

saveTuplePlot(events,"posenergy",nBins,0,eBeam*1.3,truthOutfile,c)
saveTuplePlot(events,"posPx",nBins,-eBeam*0.1,eBeam*0.1,truthOutfile,c)
saveTuplePlot(events,"posPy",nBins,-eBeam*0.1,eBeam*0.1,truthOutfile,c)
saveTuplePlot(events,"posPz",nBins,0,eBeam*1.3,truthOutfile,c)
saveTuplePlot(events,"posstartX",nBins,-100,100,truthOutfile,c)
saveTuplePlot(events,"posstartY",nBins,-100,100,truthOutfile,c)
saveTuplePlot(events,"posstartZ",nBins,-10,150,truthOutfile,c)
saveTuplePlot(events,"posendX",nBins,-400,400,truthOutfile,c)
saveTuplePlot(events,"posendY",nBins,-150,150,truthOutfile,c)
saveTuplePlot(events,"posendZ",nBins,-10,150,truthOutfile,c)

saveTuplePlot(events,"trienergy",nBins,0,eBeam*1.3,truthOutfile,c)
saveTuplePlot(events,"triPx",nBins,-eBeam*0.1,eBeam*0.1,truthOutfile,c)
saveTuplePlot(events,"triPy",nBins,-eBeam*0.1,eBeam*0.1,truthOutfile,c)
saveTuplePlot(events,"triPz",nBins,0,eBeam*1.3,truthOutfile,c)
saveTuplePlot(events,"tristartX",nBins,-100,100,truthOutfile,c)
saveTuplePlot(events,"tristartY",nBins,-100,100,truthOutfile,c)
saveTuplePlot(events,"tristartZ",nBins,-10,150,truthOutfile,c)
saveTuplePlot(events,"triendX",nBins,-400,400,truthOutfile,c)
saveTuplePlot(events,"triendY",nBins,-150,150,truthOutfile,c)
saveTuplePlot(events,"triendZ",nBins,-10,150,truthOutfile,c)
closePDF(truthOutfile,c)

del c

c1 = TCanvas("c1","c1",800,600)
ecalTruthOutfile = outfile + "_ecal"

openPDF(ecalTruthOutfile,c1)
for i in range(nEcalHits):
    saveTuplePlot2D(events,"ele1Hit{0}ecalhitIx".format(str(i)),"ele1Hit{0}ecalhitIy".format(str(i)),46,-23,23,10,-5,5,ecalTruthOutfile,c1)
    saveTuplePlot2D(events,"ele1Hit{0}ecalhitX".format(str(i)),"ele1Hit{0}ecalhitY".format(str(i)),nBins,-300,400,nBins,-100,100,ecalTruthOutfile,c1)
    saveTuplePlot(events,"ele1Hit{0}ecalhitZ".format(str(i)),nBins,-20,200,ecalTruthOutfile,c1)
    saveTuplePlot(events,"ele1Hit{0}ecalhitEnergy".format(str(i)),nBins,0,eBeam*1.3,ecalTruthOutfile,c1)
    saveTuplePlot2D(events,"ele2Hit{0}ecalhitIx".format(str(i)),"ele2Hit{0}ecalhitIy".format(str(i)),46,-23,23,10,-5,5,ecalTruthOutfile,c1)
    saveTuplePlot2D(events,"ele2Hit{0}ecalhitX".format(str(i)),"ele2Hit{0}ecalhitY".format(str(i)),nBins,-300,400,nBins,-100,100,ecalTruthOutfile,c1)
    saveTuplePlot(events,"ele2Hit{0}ecalhitZ".format(str(i)),nBins,-20,200,ecalTruthOutfile,c1)
    saveTuplePlot(events,"ele2Hit{0}ecalhitEnergy".format(str(i)),nBins,0,eBeam*1.3,ecalTruthOutfile,c1)
    saveTuplePlot2D(events,"posHit{0}ecalhitIx".format(str(i)),"posHit{0}ecalhitIy".format(str(i)),46,-23,23,10,-5,5,ecalTruthOutfile,c1)
    saveTuplePlot2D(events,"posHit{0}ecalhitX".format(str(i)),"posHit{0}ecalhitY".format(str(i)),nBins,-300,400,nBins,-100,100,ecalTruthOutfile,c1)
    saveTuplePlot(events,"posHit{0}ecalhitZ".format(str(i)),nBins,-20,200,ecalTruthOutfile,c1)
    saveTuplePlot(events,"posHit{0}ecalhitEnergy".format(str(i)),nBins,0,eBeam*1.3,ecalTruthOutfile,c1)
closePDF(ecalTruthOutfile,c1)

del c1

c2 = TCanvas("c1","c1",800,600)
svtTruthOutfile = outfile + "_svt"

openPDF(svtTruthOutfile,c2)
for i in range(1,nLay+1):
    saveTuplePlot(events,"ele1L{0}svthitPx".format(str(i)),nBins,-eBeam*0.1,eBeam*0.1,svtTruthOutfile,c2)
    saveTuplePlot(events,"ele1L{0}svthitPy".format(str(i)),nBins,-eBeam*0.1,eBeam*0.1,svtTruthOutfile,c2)
    saveTuplePlot(events,"ele1L{0}svthitPz".format(str(i)),nBins,0,eBeam*1.3,svtTruthOutfile,c2)
    saveTuplePlot2D(events,"ele1L{0}svthitX".format(str(i)),"ele1L{0}svthitY".format(str(i)),nBins,-100,100,nBins,-100,100,svtTruthOutfile,c2)
    saveTuplePlot(events,"ele1L{0}thetaX".format(str(i)),nBins,-0.1,0.1,svtTruthOutfile,c2,True)
    saveTuplePlot(events,"ele1L{0}thetaY".format(str(i)),nBins,-0.1,0.1,svtTruthOutfile,c2,True)
    saveTuplePlot2D(events,"ele1L{0}thetaX".format(str(i)),"ele1L{0}thetaY".format(str(i)),nBins,-0.1,0.1,nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot(events,"ele1L{0}residualX".format(str(i)),nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot(events,"ele1L{0}residualY".format(str(i)),nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot2D(events,"ele1L{0}residualX".format(str(i)),"ele1L{0}residualY".format(str(i)),nBins,-0.1,0.1,nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot2D(events,"ele1L{0}residualX".format(str(i)),"ele1L{0}thetaX".format(str(i)),nBins,-0.5,0.5,nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot2D(events,"ele1L{0}residualY".format(str(i)),"ele1L{0}thetaY".format(str(i)),nBins,-0.5,0.5,nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot(events,"ele2L{0}svthitPx".format(str(i)),nBins,-eBeam*0.1,eBeam*0.1,svtTruthOutfile,c2)
    saveTuplePlot(events,"ele2L{0}svthitPy".format(str(i)),nBins,-eBeam*0.1,eBeam*0.1,svtTruthOutfile,c2)
    saveTuplePlot(events,"ele2L{0}svthitPz".format(str(i)),nBins,0,eBeam*1.3,svtTruthOutfile,c2)
    saveTuplePlot2D(events,"ele2L{0}svthitX".format(str(i)),"ele2L{0}svthitY".format(str(i)),nBins,-100,100,nBins,100,-100,svtTruthOutfile,c2)
    saveTuplePlot(events,"ele2L{0}thetaX".format(str(i)),nBins,-0.1,0.1,svtTruthOutfile,c2,True)
    saveTuplePlot(events,"ele2L{0}thetaY".format(str(i)),nBins,-0.1,0.1,svtTruthOutfile,c2,True)
    saveTuplePlot2D(events,"ele2L{0}thetaX".format(str(i)),"ele2L{0}thetaY".format(str(i)),nBins,-0.1,0.1,nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot(events,"ele2L{0}residualX".format(str(i)),nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot(events,"ele2L{0}residualY".format(str(i)),nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot2D(events,"ele2L{0}residualX".format(str(i)),"ele2L{0}residualY".format(str(i)),nBins,-0.1,0.1,nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot2D(events,"ele2L{0}residualX".format(str(i)),"ele2L{0}thetaX".format(str(i)),nBins,-0.5,0.5,nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot2D(events,"ele2L{0}residualY".format(str(i)),"ele2L{0}thetaY".format(str(i)),nBins,-0.5,0.5,nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot(events,"posL{0}svthitPx".format(str(i)),nBins,-eBeam*0.1,eBeam*0.1,svtTruthOutfile,c2)
    saveTuplePlot(events,"posL{0}svthitPy".format(str(i)),nBins,-eBeam*0.1,eBeam*0.1,svtTruthOutfile,c2)
    saveTuplePlot(events,"posL{0}svthitPz".format(str(i)),nBins,0,eBeam*1.3,svtTruthOutfile,c2)
    saveTuplePlot2D(events,"posL{0}svthitX".format(str(i)),"posL{0}svthitY".format(str(i)),nBins,-100,100,nBins,-100,100,svtTruthOutfile,c2)
    saveTuplePlot(events,"posL{0}thetaX".format(str(i)),nBins,-0.1,0.1,svtTruthOutfile,c2,True)
    saveTuplePlot(events,"posL{0}thetaY".format(str(i)),nBins,-0.1,0.1,svtTruthOutfile,c2,True)
    saveTuplePlot2D(events,"posL{0}thetaX".format(str(i)),"posL{0}thetaY".format(str(i)),nBins,-0.1,0.1,nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot(events,"posL{0}residualX".format(str(i)),nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot(events,"posL{0}residualY".format(str(i)),nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot2D(events,"posL{0}residualX".format(str(i)),"posL{0}residualY".format(str(i)),nBins,-0.1,0.1,nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot2D(events,"posL{0}residualX".format(str(i)),"posL{0}thetaX".format(str(i)),nBins,-0.5,0.5,nBins,-0.1,0.1,svtTruthOutfile,c2)
    saveTuplePlot2D(events,"posL{0}residualY".format(str(i)),"posL{0}thetaY".format(str(i)),nBins,-0.5,0.5,nBins,-0.1,0.1,svtTruthOutfile,c2)
closePDF(svtTruthOutfile,c2)

del c2