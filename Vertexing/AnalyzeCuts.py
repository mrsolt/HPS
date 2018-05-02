import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input Data file> <input MC file> <input A' files>".format(sys.argv[0])
    print "Arguments: "
    print '\t-v: is L1L1'
    print '\t-x: is L1L2'
    print '\t-y: is L2L2'
    print '\t-z: target position (default 0.5 mm)'
    print '\t-b: use both data and MC files'
    print '\t- : cut tuples (default true)'
    print '\t-h: this help message'
    print

L1L1 = False
L1L2 = False
L2L2 = False
DataMC = False
zTarg = 0.5
ebeam = 1.05
cutTuple = True

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hvxyz:bce:')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-v':
			L1L1 = True
		if opt=='-x':
			L1L2 = True
		if opt=='-y':
			L2L2 = True
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-e':
			ebeam = float(arg)
		if opt=='-b':
			DataMC = True
		if opt=='-c':
			cutTuple = False
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def tupleToHisto(events,inHisto,histo,nBins,minX,maxX):
	events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,histo,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject(histo)
	return histo

def saveTuplePlot(inHisto,nBins,minX,maxX,outfile,canvas):
	events.Draw("{0}>>({1},{2},{3})".format(inHisto,nBins,minX,maxX))
	canvas.Print(outfile+".pdf")

def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",cut="",stats=0,logY=0):
	events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,inHisto1,nBinsX,minX,maxX,nBinsY,minY,maxY),cut)
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
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def getHisto(histoTitle,infile):
	histo = infile.Get(histoTitle)
	return histo

def buildLegend(entries,options):
	legend = TLegend()
	legend = TLegend(.68,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(Histo1,"L0L0","LP")
	return legend

def drawHisto(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	histo.Draw("")
	#histo.GetXaxis().SetRangeUser(-5,150)
	#histo.GetYaxis().SetRangeUser(0,1.1)
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)

def saveHisto(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	drawHisto(histo,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.Print(outfile+".pdf")

def getPlot(string):
	arr = string.split(" ")
	return arr[0]

def getMin(string):
	arr = string.split(" ")
	if(len(arr) < 2): return ""
	else: return float(arr[1])

def getMax(string):
	arr = string.split(" ")
	if(len(arr) < 3): return ""
	else: return float(arr[2])

def getCut(string):
	arr = string.split(" ")
	if(len(arr) < 4): return ""
	else: return arr[3]

nBins = 50
minVZ = -20
maxVZ = 150
maxX = 3
minX = -maxX
maxY = 3
minY = -maxY


outfile = remainder[0]
datafile = TFile(remainder[1])

firstAp = 2
if(DataMC == True):
	mcfile = TFile(remainder[2])
	firstAp = 3
	mcevents = mcfile.Get("ntuple")

dataevents = datafile.Get("ntuple")

apfiles = []
events = []
mass = []

for i in range(firstAp,len(remainder)):
	apfiles.append(TFile(remainder[i]))
	events.append(apfiles[i-firstAp].Get("ntuple"))
	events[i-firstAp].Draw("triM>>dummy({0},{1},{2})".format(1000,0,1))
	dummy = ROOT.gROOT.FindObject("dummy")
	mass.append(dummy.GetMean())
	del dummy

cuts = []
cuts.append("eleClY*posClY -10000 10000")
cuts.append("uncP 0 1.4")
cuts.append("eleTrkChisq 0 100")
cuts.append("posTrkChisq 0 100")
cuts.append("eleP 0 1.4")
cuts.append("uncChisq 0 20")
cuts.append("bscChisq 0 20")
cuts.append("bscChisq-uncChisq 0 10")
cuts.append("eleMatchChisq 0 20")
cuts.append("posMatchChisq 0 20")
cuts.append("eleTrkChisq 0 40")
cuts.append("posTrkChisq 0 40")
cuts.append("eleTrkChisq/eleNTrackHits 0 10")
cuts.append("posTrkChisq/posNTrackHits 0 10")
cuts.append("eleTrkD0 -15 15")
cuts.append("posTrkD0 -15 15")
cuts.append("eleTrkZ0 -15 15")
cuts.append("posTrkZ0 -15 15")
cuts.append("abs(eleClT-eleTrkT-43) 0 10")
cuts.append("abs(posClT-posTrkT-43) 0 10")
cuts.append("abs(eleClT-posClT) 0 10")
cuts.append("abs(eleP-posP)/(eleP+posP) 0 2")
cuts.append("abs(elePX-posPX)/(elePX+posPX) 0 20")
cuts.append("abs(elePY-posPY)/(elePY+posPY) 0 20")
cuts.append("abs(sqrt(elePX**2+elePY**2)-sqrt(posPX**2+elePY**2))/(sqrt(elePX**2+elePY**2)+sqrt(posPX**2+elePY**2)) 0 20")
cuts.append("abs(sqrt((elePX-posPY)**2+(elePY-posPY)**2))/sqrt((elePX+posPX)**2+(elePY+posPY)**2) 0 2")
cuts.append("posTrkD0+{0}*posPX/posP -5 5".format(zTarg))
cuts.append("eleTrkD0+{0}*elePX/eleP -5 5".format(zTarg))
cuts.append("eleTrkChisq/(2*eleNTrackHits-5)+posTrkChisq/(2*posNTrackHits-5) 0 20")
cuts.append("eleClE/eleP 0 2")
cuts.append("posClE/posP 0 2")
cuts.append("sqrt((uncVX-(uncVZ-{0})*uncPX/uncPZ)**2+(uncVY-(uncVZ-{0})*uncPY/uncPZ)**2) 0 2".format(zTarg))
cuts.append("sqrt((uncVX-(uncVZ-{0})*uncPX/uncPZ)**2+(uncVY-(uncVZ-{0})*uncPY/uncPZ)**2/0.25) 0 8".format(zTarg))
cuts.append("sqrt((bscVX-(bscVZ-{0})*bscPX/bscPZ)**2+(bscVY-(bscVZ-{0})*bscPY/bscPZ)**2) 0 2".format(zTarg))
cuts.append("sqrt((bscVX-(bscVZ-{0})*bscPX/bscPZ)**2/0.25+(bscVY-(bscVZ-{0})*bscPY/bscPZ)**2/0.125) 0 5".format(zTarg))
cuts.append("sqrt(uncVX*uncVX+uncVY*uncVY) 0 2")
cuts.append("sqrt(bscVX*bscVX+bscVY*bscVY) 0 2")
cuts.append("sqrt((uncVX-(uncVZ-{0})*uncPX/uncPZ-(bscVX-(bscVZ-{0})*bscPX/bscPZ))**2+(uncVY-(uncVZ-{0})*uncPY/uncPZ-(bscVY-(bscVZ-{0})*bscPY/bscPZ))**2) 0 5".format(zTarg))
cuts.append("sqrt((uncVX-(uncVZ-{0})*uncPX/uncPZ-(bscVX-(bscVZ-{0})*bscPX/bscPZ))**2+(uncVY-(uncVZ-{0})*uncPY/uncPZ-(bscVY-(bscVZ-{0})*bscPY/bscPZ))**2/0.25) 0 5".format(zTarg))

if(L1L1):
	cuts.append("eleTrkExtrpYSensorAxialTopL1 -25 25")
	cuts.append("eleTrkExtrpYSensorStereoTopL1 -25 25")
	cuts.append("eleTrkExtrpYSensorAxialBotL1 -25 25")
	cuts.append("eleTrkExtrpYSensorStereoBotL1 -25 25")
	cuts.append("posTrkExtrpYSensorAxialTopL1 -25 25")
	cuts.append("posTrkExtrpYSensorStereoTopL1 -25 25")
	cuts.append("posTrkExtrpYSensorAxialBotL1 -25 25")
	cuts.append("posTrkExtrpYSensorStereoBotL1 -25 25")
	cuts.append("eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY) -5 5".format(zTarg))
	cuts.append("posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY) -5 5".format(zTarg))

if(L1L2):
	cuts.append("eleTrkExtrpYSensorAxialTopL1 -25 25 !eleHasL1")
	cuts.append("eleTrkExtrpYSensorStereoTopL1 -25 25 !eleHasL1")
	cuts.append("eleTrkExtrpYSensorAxialBotL1 -25 25 !eleHasL1")
	cuts.append("eleTrkExtrpYSensorStereoBotL1 -25 25 !eleHasL1")
	cuts.append("posTrkExtrpYSensorAxialTopL1 -25 25 !posHasL1")
	cuts.append("posTrkExtrpYSensorStereoTopL1 -25 25 !posHasL1")
	cuts.append("posTrkExtrpYSensorAxialBotL1 -25 25 !posHasL1")
	cuts.append("posTrkExtrpYSensorStereoBotL1 -25 25 !posHasL1")
	cuts.append("eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY) -5 5 !posHasL1".format(zTarg))
	cuts.append("posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY) -5 5 !eleHasL1".format(zTarg))
	cuts.append("eleMinPositiveIsoL2+0.33*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY) -5 5 !eleHasL1".format(zTarg))
	cuts.append("posMinPositiveIsoL2+0.33*(posTrkZ0+{0}*posPY/posP)*sign(posPY) -5 5 !posHasL1".format(zTarg))

if(L2L2):
	cuts.append("eleTrkExtrpYSensorAxialTopL1 -25 25")
	cuts.append("eleTrkExtrpYSensorStereoTopL1 -25 25")
	cuts.append("eleTrkExtrpYSensorAxialBotL1 -25 25")
	cuts.append("eleTrkExtrpYSensorStereoBotL1 -25 25")
	cuts.append("posTrkExtrpYSensorAxialTopL1 -25 25")
	cuts.append("posTrkExtrpYSensorStereoTopL1 -25 25")
	cuts.append("posTrkExtrpYSensorAxialBotL1 -25 25")
	cuts.append("posTrkExtrpYSensorStereoBotL1 -25 25")
	cuts.append("eleMinPositiveIsoL2+0.33*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY) -5 5".format(zTarg))
	cuts.append("posMinPositiveIsoL2+0.33*(posTrkZ0+{0}*posPY/posP)*sign(posPY) -5 5".format(zTarg))

histos = []
openPDF(outfile,c)

for i in range(len(cuts)):
	plot = getPlot(cuts[i])
	minimum = getMin(cuts[i])
	maximum = getMax(cuts[i])
	cut = ""
	if(cutTuple):
		cut = getCut(cuts[i])
	histos.append(TH1F(cuts[i],cuts[i],nBins,minimum,maximum))
	saveTuplePlot2D(dataevents,"uncVZ",plot,nBins,minVZ,maxVZ,nBins,minimum,maximum,outfile,c,"uncVZ",plot," Data " + plot + " " + cut,cut)
	if(DataMC == True):
		saveTuplePlot2D(mcevents,"uncVZ",plot,nBins,minVZ,maxVZ,nBins,minimum,maximum,outfile,c,"uncVZ",plot," MC " + plot + " " + cut,cut)
	for j in range(len(events)):
		saveTuplePlot2D(events[j],"uncVZ",plot,nBins,minVZ,maxVZ,nBins,minimum,maximum,outfile,c,"uncVZ",plot,str(mass[j]) + " GeV A' " + plot + " " + cut,cut)

saveTuplePlot2D(dataevents,"uncVX-(uncVZ-{0})*uncPX/uncPZ".format(zTarg),"uncVY-(uncVZ-{0})*uncPY/uncPZ".format(zTarg),nBins,minX,maxX,nBins,minY,maxY,outfile,c,"unc proj x [mm]","unc proj y [mm]","Data")
saveTuplePlot2D(dataevents,"bscVX-(bscVZ-{0})*bscPX/bscPZ".format(zTarg),"bscVY-(bscVZ-{0})*bscPY/bscPZ".format(zTarg),nBins,minX,maxX,nBins,minY,maxY,outfile,c,"bsc proj x [mm]","bsc proj y [mm]","Data")
saveTuplePlot2D(dataevents,"uncVX-(uncVZ-{0})*uncPX/uncPZ - (bscVX-(bscVZ-{0})*bscPX/bscPZ)".format(zTarg),"uncVY-(uncVZ-{0})*uncPY/uncPZ - (bscVY-(bscVZ-{0})*bscPY/bscPZ)".format(zTarg),nBins,minX,maxX,nBins,minY,maxY,outfile,c,"unc - bsc proj x [mm]","unc -bsc proj y [mm]","Data")

if(DataMC == True):
	saveTuplePlot2D(mcevents,"uncVX-(uncVZ-{0})*uncPX/uncPZ".format(zTarg),"uncVY-(uncVZ-{0})*uncPY/uncPZ".format(zTarg),nBins,minX,maxX,nBins,minY,maxY,outfile,c,"unc proj x [mm]","unc proj y [mm]","MC")
	saveTuplePlot2D(mcevents,"bscVX-(bscVZ-{0})*bscPX/bscPZ".format(zTarg),"bscVY-(bscVZ-{0})*bscPY/bscPZ".format(zTarg),nBins,minX,maxX,nBins,minY,maxY,outfile,c,"bsc proj x [mm]","bsc proj y [mm]","MC")
	saveTuplePlot2D(mcevents,"uncVX-(uncVZ-{0})*uncPX/uncPZ - (bscVX-(bscVZ-{0})*bscPX/bscPZ)".format(zTarg),"uncVY-(uncVZ-{0})*uncPY/uncPZ - (bscVY-(bscVZ-{0})*bscPY/bscPZ)".format(zTarg),nBins,minX,maxX,nBins,minY,maxY,outfile,c,"unc - bsc proj x [mm]","unc -bsc proj y [mm]","MC")

for i in range(len(events)):
	saveTuplePlot2D(events[i],"uncVX-(uncVZ-{0})*uncPX/uncPZ".format(zTarg),"uncVY-(uncVZ-{0})*uncPY/uncPZ".format(zTarg),nBins,minX,maxX,nBins,minY,maxY,outfile,c,"unc proj x [mm]","unc proj y [mm]",str(mass[i]) + " GeV A' ")
	saveTuplePlot2D(events[i],"bscVX-(bscVZ-{0})*bscPX/bscPZ".format(zTarg),"bscVY-(bscVZ-{0})*bscPY/bscPZ".format(zTarg),nBins,minX,maxX,nBins,minY,maxY,outfile,c,"bsc proj x [mm]","bsc proj y [mm]",str(mass[i]) + " GeV A' ")
	saveTuplePlot2D(events[i],"uncVX-(uncVZ-{0})*uncPX/uncPZ - (bscVX-(bscVZ-{0})*bscPX/bscPZ)".format(zTarg),"uncVY-(uncVZ-{0})*uncPY/uncPZ - (bscVY-(bscVZ-{0})*bscPY/bscPZ)".format(zTarg),nBins,minX,maxX,nBins,minY,maxY,outfile,c,"unc - bsc proj x [mm]","unc -bsc proj y [mm]",str(mass[i]) + " GeV A' ")

saveTuplePlot2D(dataevents,"uncM","uncVZ",nBins,0,0.1,nBins,minVZ,maxVZ,outfile,c,"uncM","uncVZ","Data","sqrt((uncVX-(uncVZ-{0})*uncPX/uncPZ-(bscVX-(bscVZ-{0})*bscPX/bscPZ))**2+(uncVY-(uncVZ-{0})*uncPY/uncPZ-(bscVY-(bscVZ-{0})*bscPY/bscPZ))**2/0.25)<0.6 && sqrt((bscVX-(bscVZ-{0})*bscPX/bscPZ)**2/0.25+(bscVY-(bscVZ-{0})*bscPY/bscPZ)**2/0.125)<1 && sqrt((uncVX-(uncVZ-{0})*uncPX/uncPZ)**2+(uncVY-(uncVZ-{0})*uncPY/uncPZ)**2/0.25)<0.8".format(zTarg))

closePDF(outfile,c)