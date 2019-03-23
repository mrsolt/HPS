import sys
tmpargv = sys.argv
sys.argv = []
import getopt
from array import array
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH2F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-m: minimum uncVZ'
    print '\t-n: maximum uncVZ'
    print '\t-z: target z position'
    print '\t-x: is L1L2'
    print '\t-y: is L2L2'
    print '\t-h: this help message'
    print

def getPlotX(string):
	arr = string.split(" ")
	return arr[0]

def getPlotY(string):
	arr = string.split(" ")
	if(len(arr) < 2): return ""
	else: return arr[1]

def getMinX(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

def getMaxX(string):
	arr = string.split(" ")
	if(len(arr) < 4): return -9999
	else: return float(arr[3])

def getMinY(string):
	arr = string.split(" ")
	if(len(arr) < 5): return -9999
	else: return float(arr[4])

def getMaxY(string):
	arr = string.split(" ")
	if(len(arr) < 6): return -9999
	else: return float(arr[5])

def getCut(string):
	arr = string.split(" ")
	if(len(arr) < 7): return ""
	else: return arr[6]

def getMin(string):
	arr = string.split(" ")
	if(len(arr) < 2): return -9999
	else: return float(arr[1])

def getMax(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",cut="",stats=1,logY=0):
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


def saveplot(events,inHisto,nBinsX,minX,maxX,outfile,canvas,XaxisTitle="",plotTitle="",cut="",stats=1,logY=0):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBinsX,minX,maxX),cut)
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.SetStats(stats)
	histo.Draw("COLZ")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	del histo

def plotVert(events,inHisto,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",plotTitle="",cut="",stats=0,logY=0):
	events.Draw("{0}>>histoBad({1},{2},{3})".format("Bad"+inHisto,nBinsX,minX,maxX),cut)
	histoBad = ROOT.gROOT.FindObject("histoBad")
	events.Draw("{0}>>histoTruth({1},{2},{3})".format("Truth"+inHisto,nBinsX,minX,maxX),cut)
	histoTruth = ROOT.gROOT.FindObject("histoTruth")
	#histoBad = getHisto(events,"Bad"+inHisto,nBinsX,minX,maxX,cut)
	#histoTruth = getHisto(events,"Truth"+inHisto,nBinsX,minX,maxX,cut)
	maximum = histoBad.GetMaximum()
	if(histoTruth.GetMaximum() > maximum):
		maximum = histoTruth.GetMaximum()
	histoBad.SetTitle(plotTitle)
	histoBad.GetXaxis().SetTitle(XaxisTitle)
	histoBad.SetStats(stats)
	histoBad.GetYaxis().SetRangeUser(0,1.2*maximum)
	histoBad.Draw()
	canvas.SetLogy(logY)
	histoTruth.SetLineColor(2)
	histoTruth.Draw("same")
	legend = TLegend(.68,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histoBad,"Bad Fit","LP")
	legend.AddEntry(histoTruth,"Truth Fit","LP")
	legend.Draw()
	canvas.Print(outfile+".pdf")
	saveTuplePlot2D(events,"Bad"+inHisto,"BaduncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Bad "+XaxisTitle,"Bad uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"Bad"+inHisto,"TruthuncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Bad "+XaxisTitle,"Truth uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"Truth"+inHisto,"BaduncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Truth "+XaxisTitle,"Bad uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"Truth"+inHisto,"TruthuncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Truth "+XaxisTitle,"Truth uncVZ [mm]",plotTitle,cut)
	del histoBad
	del histoTruth
	del legend

def plotPart(events,inHisto,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",plotTitle="",cut="",stats=0,logY=0):
	events.Draw("{0}>>histoEleBad({1},{2},{3})".format("eleBad"+inHisto,nBinsX,minX,maxX),cut)
	histoEleBad = ROOT.gROOT.FindObject("histoEleBad")
	events.Draw("{0}>>histoEleTruth({1},{2},{3})".format("eleTruth"+inHisto,nBinsX,minX,maxX),cut)
	histoEleTruth = ROOT.gROOT.FindObject("histoEleTruth")
	events.Draw("{0}>>histoPosBad({1},{2},{3})".format("posBad"+inHisto,nBinsX,minX,maxX),cut)
	histoPosBad = ROOT.gROOT.FindObject("histoPosBad")
	events.Draw("{0}>>histoPosTruth({1},{2},{3})".format("posTruth"+inHisto,nBinsX,minX,maxX),cut)
	histoPosTruth = ROOT.gROOT.FindObject("histoPosTruth")
	#histoEleBad = getHisto(events,"eleBad"+inHisto,nBinsX,minX,maxX,cut)
	#histoEleTruth = getHisto(events,"eleTruth"+inHisto,nBinsX,minX,maxX,cut)
	#histoPosBad = getHisto(events,"posBad"+inHisto,nBinsX,minX,maxX,cut)
	#histoPosTruth = getHisto(events,"posTruth"+inHisto,nBinsX,minX,maxX,cut)
	maximumEle = histoEleBad.GetMaximum()
	if(histoEleTruth.GetMaximum() > maximumEle):
		maximumEle = histoEleTruth.GetMaximum()
	maximumPos = histoPosBad.GetMaximum()
	if(histoPosTruth.GetMaximum() > maximumPos):
		maximumPos = histoPosTruth.GetMaximum()
	histoEleBad.SetTitle("Ele "+plotTitle)
	histoEleBad.GetXaxis().SetTitle(XaxisTitle)
	histoEleBad.SetStats(stats)
	histoEleBad.GetYaxis().SetRangeUser(0,1.2*maximumEle)
	histoEleBad.Draw()
	canvas.SetLogy(logY)
	histoEleTruth.SetLineColor(2)
	histoEleTruth.Draw("same")
	legend = TLegend(.68,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histoEleBad,"Bad Fit","LP")
	legend.AddEntry(histoEleTruth,"Truth Fit","LP")
	legend.Draw()
	canvas.Print(outfile+".pdf")
	histoPosBad.SetTitle("Pos "+plotTitle)
	histoPosBad.GetXaxis().SetTitle(XaxisTitle)
	histoPosBad.SetStats(stats)
	histoPosBad.GetYaxis().SetRangeUser(0,1.2*maximumPos)
	histoPosBad.Draw()
	canvas.SetLogy(logY)
	histoPosTruth.SetLineColor(2)
	histoPosTruth.Draw("same")
	legend.Draw()
	canvas.Print(outfile+".pdf")
	saveTuplePlot2D(events,"eleBad"+inHisto,"BaduncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Bad Ele "+XaxisTitle,"Bad uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"eleBad"+inHisto,"TruthuncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Bad Ele "+XaxisTitle,"Truth uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"eleTruth"+inHisto,"BaduncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Truth Ele "+XaxisTitle,"Bad uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"eleTruth"+inHisto,"TruthuncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Truth Ele "+XaxisTitle,"Truth uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"posBad"+inHisto,"BaduncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Bad Pos "+XaxisTitle,"Bad uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"posBad"+inHisto,"TruthuncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Bad Pos "+XaxisTitle,"Truth uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"posTruth"+inHisto,"BaduncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Truth Pos "+XaxisTitle,"Bad uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"posTruth"+inHisto,"TruthuncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Truth Pos "+XaxisTitle,"Truth uncVZ [mm]",plotTitle,cut)
	del histoEleBad
	del histoEleTruth
	del histoPosBad
	del histoPosTruth
	del legend

def getHisto(events,inHisto,nBinsX,minX,maxX,cut=""):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBinsX,minX,maxX),cut)
	histo = ROOT.gROOT.FindObject("histo")
	print histo
	print inHisto
	return histo

minVZ = -30
maxVZ = 80
maxTheta = 0.03
minTheta = -maxTheta
zTarg = 0.5
isL1L2 = False
isL2L2 = False

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'm:n:z:xyh')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-x':
			isL1L2 = True
		if opt=='-y':
			isL2L2 = True
		if opt=='-h':
			print_usage()
			sys.exit(0)

if(isL1L2 and isL2L2):
	print "L1L2 and L2L2 can't both be true!"
	sys.exit(0)	

gStyle.SetOptStat(110011)
c = TCanvas("c","c",800,600)

outfile = remainder[0]
events = TChain("ntuple")
for i in range(1,len(remainder)):
    events.Add(remainder[i])

nBins = 100
#minX = ""
#maxX = ""
#minY = ""
#maxY = ""

isoEle = "eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY)".format(zTarg)
isoPos = "posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY)".format(zTarg)

#minx = -30
#maxx = -minx
#miny = -8
#maxy = -miny
maxTheta = 0.03
minTheta = -maxTheta

cut = "(((!eleL1tIsGoodTruthHit||!eleL2tIsGoodTruthHit||!eleL1bIsGoodTruthHit||!eleL2bIsGoodTruthHit)||(!posL1tIsGoodTruthHit||!posL2tIsGoodTruthHit||!posL1bIsGoodTruthHit||!posL2bIsGoodTruthHit))&&elePurity>0.8&&posPurity>0.8)"

cuts = []
cuts.append("elePurity<0.99||posPurity<0.99")
cuts.append("elePurity>0.99&&posPurity<0.99")
cuts.append("elePurity<0.99&&posPurity>0.99")
cuts.append("elePurity<0.99&&posPurity<0.99")
cuts.append("elePurity>0.99&&posPurity<0.99&&posPurity>0.79")
cuts.append("elePurity<0.99&&posPurity>0.99&&elePurity>0.79")
cuts.append("elePurity<0.99&&posPurity<0.99&&elePurity>0.79&&posPurity>0.79")

if(not isL1L2 and not isL2L2):
	cuts.append("(!eleL1tIsGoodTruthHit||!eleL2tIsGoodTruthHit||!eleL1bIsGoodTruthHit||!eleL2bIsGoodTruthHit)")
	cuts.append("(!posL1tIsGoodTruthHit||!posL2tIsGoodTruthHit||!posL1bIsGoodTruthHit||!posL2bIsGoodTruthHit)")
	cuts.append("(!eleL1tIsGoodTruthHit||!eleL2tIsGoodTruthHit||!eleL1bIsGoodTruthHit||!eleL2bIsGoodTruthHit)")
	cuts.append("(!posL1tIsGoodTruthHit||!posL2tIsGoodTruthHit||!posL1bIsGoodTruthHit||!posL2bIsGoodTruthHit)")
	cuts.append("(!eleL1tIsGoodTruthHit||!eleL2tIsGoodTruthHit||!eleL1bIsGoodTruthHit||!eleL2bIsGoodTruthHit)&&elePurity>0.8")
	cuts.append("(!posL1tIsGoodTruthHit||!posL2tIsGoodTruthHit||!posL1bIsGoodTruthHit||!posL2bIsGoodTruthHit)&&posPurity>0.8")
	cuts.append("(!eleL1tIsGoodTruthHit||!eleL2tIsGoodTruthHit||!eleL1bIsGoodTruthHit||!eleL2bIsGoodTruthHit)&&elePurity>0.8")
	cuts.append("(!posL1tIsGoodTruthHit||!posL2tIsGoodTruthHit||!posL1bIsGoodTruthHit||!posL2bIsGoodTruthHit)&&posPurity>0.8")
	cuts.append("(!eleL1tIsGoodTruthHit||!eleL2tIsGoodTruthHit||!eleL1bIsGoodTruthHit||!eleL2bIsGoodTruthHit)&&(!posL1tIsGoodTruthHit||!posL2tIsGoodTruthHit||!posL1bIsGoodTruthHit||!posL2bIsGoodTruthHit)&&elePurity>0.8&&posPurity>0.8")
	cuts.append("((!eleL1tIsGoodTruthHit||!eleL2tIsGoodTruthHit||!eleL1bIsGoodTruthHit||!eleL2bIsGoodTruthHit)||(!posL1tIsGoodTruthHit||!posL2tIsGoodTruthHit||!posL1bIsGoodTruthHit||!posL2bIsGoodTruthHit))&&elePurity>0.8&&posPurity>0.8")

if(isL1L2):
	cuts.append("eleBadHasL1&&(!eleL1tIsGoodTruthHit||!eleL2tIsGoodTruthHit||!eleL1bIsGoodTruthHit||!eleL2bIsGoodTruthHit)")
	cuts.append("posBadHasL1&&(!posL1tIsGoodTruthHit||!posL2tIsGoodTruthHit||!posL1bIsGoodTruthHit||!posL2bIsGoodTruthHit)")
	cuts.append("eleBadHasL1&&(!eleL1tIsGoodTruthHit||!eleL2tIsGoodTruthHit||!eleL1bIsGoodTruthHit||!eleL2bIsGoodTruthHit)")
	cuts.append("posBadHasL1&&(!posL1tIsGoodTruthHit||!posL2tIsGoodTruthHit||!posL1bIsGoodTruthHit||!posL2bIsGoodTruthHit)")
	cuts.append("!eleBadHasL1&&(!eleL3tIsGoodTruthHit||!eleL4tIsGoodTruthHit||!eleL3bIsGoodTruthHit||!eleL4bIsGoodTruthHit)")
	cuts.append("!posBadHasL1&&(!posL3tIsGoodTruthHit||!posL4tIsGoodTruthHit||!posL3bIsGoodTruthHit||!posL4bIsGoodTruthHit)")
	cuts.append("!eleBadHasL1&&(!eleL3tIsGoodTruthHit||!eleL4tIsGoodTruthHit||!eleL3bIsGoodTruthHit||!eleL4bIsGoodTruthHit)")
	cuts.append("!posBadHasL1&&(!posL3tIsGoodTruthHit||!posL4tIsGoodTruthHit||!posL3bIsGoodTruthHit||!posL4bIsGoodTruthHit)")
	cuts.append("eleBadHasL1&&(!eleL1tIsGoodTruthHit||!eleL2tIsGoodTruthHit||!eleL1bIsGoodTruthHit||!eleL2bIsGoodTruthHit)&&elePurity>0.79")
	cuts.append("posBadHasL1&&(!posL1tIsGoodTruthHit||!posL2tIsGoodTruthHit||!posL1bIsGoodTruthHit||!posL2bIsGoodTruthHit)&&posPurity>0.79")
	cuts.append("eleBadHasL1&&(!eleL1tIsGoodTruthHit||!eleL2tIsGoodTruthHit||!eleL1bIsGoodTruthHit||!eleL2bIsGoodTruthHit)&&elePurity>0.79")
	cuts.append("posBadHasL1&&(!posL1tIsGoodTruthHit||!posL2tIsGoodTruthHit||!posL1bIsGoodTruthHit||!posL2bIsGoodTruthHit)&&posPurity>0.79")
	cuts.append("!eleBadHasL1&&(!eleL3tIsGoodTruthHit||!eleL4tIsGoodTruthHit||!eleL3bIsGoodTruthHit||!eleL4bIsGoodTruthHit)&&elePurity>0.79")
	cuts.append("!posBadHasL1&&(!posL3tIsGoodTruthHit||!posL4tIsGoodTruthHit||!posL3bIsGoodTruthHit||!posL4bIsGoodTruthHit)&&posPurity>0.79")
	cuts.append("!eleBadHasL1&&(!eleL3tIsGoodTruthHit||!eleL4tIsGoodTruthHit||!eleL3bIsGoodTruthHit||!eleL4bIsGoodTruthHit)&&elePurity>0.79")
	cuts.append("!posBadHasL1&&(!posL3tIsGoodTruthHit||!posL4tIsGoodTruthHit||!posL3bIsGoodTruthHit||!posL4bIsGoodTruthHit)&&posPurity>0.79")
	cuts.append("(eleBadHasL1&&((!eleL1tIsGoodTruthHit||!eleL2tIsGoodTruthHit||!eleL1bIsGoodTruthHit||!eleL2bIsGoodTruthHit)||(!posL3tIsGoodTruthHit||!posL4tIsGoodTruthHit||!posL3bIsGoodTruthHit||!posL4bIsGoodTruthHit)))||(posBadHasL1&&((!eleL3tIsGoodTruthHit||!eleL4tIsGoodTruthHit||!eleL3bIsGoodTruthHit||!eleL4bIsGoodTruthHit)||(!posL1tIsGoodTruthHit||!posL2tIsGoodTruthHit||!posL1bIsGoodTruthHit||!posL2bIsGoodTruthHit)))&&elePurity>0.79&&posPurity>0.79")
	cut = "((eleBadHasL1&&((!eleL1tIsGoodTruthHit||!eleL2tIsGoodTruthHit||!eleL1bIsGoodTruthHit||!eleL2bIsGoodTruthHit)||(!posL3tIsGoodTruthHit||!posL4tIsGoodTruthHit||!posL3bIsGoodTruthHit||!posL4bIsGoodTruthHit)))||(posBadHasL1&&((!eleL3tIsGoodTruthHit||!eleL4tIsGoodTruthHit||!eleL3bIsGoodTruthHit||!eleL4bIsGoodTruthHit)||(!posL1tIsGoodTruthHit||!posL2tIsGoodTruthHit||!posL1bIsGoodTruthHit||!posL2bIsGoodTruthHit)))&&elePurity>0.79&&posPurity>0.79)"

if(isL2L2):
	cuts.append("(!eleL3tIsGoodTruthHit||!eleL4tIsGoodTruthHit||!eleL3bIsGoodTruthHit||!eleL4bIsGoodTruthHit)")
	cuts.append("(!posL3tIsGoodTruthHit||!posL4tIsGoodTruthHit||!posL3bIsGoodTruthHit||!posL4bIsGoodTruthHit)")
	cuts.append("(!eleL3tIsGoodTruthHit||!eleL4tIsGoodTruthHit||!eleL3bIsGoodTruthHit||!eleL4bIsGoodTruthHit)")
	cuts.append("(!posL3tIsGoodTruthHit||!posL4tIsGoodTruthHit||!posL3bIsGoodTruthHit||!posL4bIsGoodTruthHit)")
	cuts.append("(!eleL3tIsGoodTruthHit||!eleL4tIsGoodTruthHit||!eleL3bIsGoodTruthHit||!eleL4bIsGoodTruthHit)&&elePurity>0.79")
	cuts.append("(!posL3tIsGoodTruthHit||!posL4tIsGoodTruthHit||!posL3bIsGoodTruthHit||!posL4bIsGoodTruthHit)&&posPurity>0.79")
	cuts.append("(!eleL3tIsGoodTruthHit||!eleL4tIsGoodTruthHit||!eleL3bIsGoodTruthHit||!eleL4bIsGoodTruthHit)&&elePurity>0.79")
	cuts.append("(!posL3tIsGoodTruthHit||!posL4tIsGoodTruthHit||!posL3bIsGoodTruthHit||!posL4bIsGoodTruthHit)&&posPurity>0.79")
	cuts.append("(!eleL3tIsGoodTruthHit||!eleL4tIsGoodTruthHit||!eleL3bIsGoodTruthHit||!eleL4bIsGoodTruthHit)&&(!posL3tIsGoodTruthHit||!posL4tIsGoodTruthHit||!posL3bIsGoodTruthHit||!posL4bIsGoodTruthHit)&&elePurity>0.79&&posPurity>0.79")
	cuts.append("((!eleL3tIsGoodTruthHit||!eleL4tIsGoodTruthHit||!eleL3bIsGoodTruthHit||!eleL4bIsGoodTruthHit)||(!posL3tIsGoodTruthHit||!posL4tIsGoodTruthHit||!posL3bIsGoodTruthHit||!posL4bIsGoodTruthHit))&&elePurity>0.79&&posPurity>0.79")
	cut = "(((!eleL3tIsGoodTruthHit||!eleL4tIsGoodTruthHit||!eleL3bIsGoodTruthHit||!eleL4bIsGoodTruthHit)||(!posL3tIsGoodTruthHit||!posL4tIsGoodTruthHit||!posL3bIsGoodTruthHit||!posL4bIsGoodTruthHit))&&elePurity>0.79&&posPurity>0.79)" 

plotsvert = []
plotsvert.append("uncVZ {0} {1}".format(minVZ,maxVZ))
plotsvert.append("uncCovZZ 0 400")
plotsvert.append("uncVX -1 1")
plotsvert.append("uncVY -1 1")
plotsvert.append("uncM 0 0.1")
plotsvert.append("uncChisq 0 20")
plotsvert.append("bscChisq 0 20")
plotsvert.append("tarChisq 0 50")
plotsvert.append("uncTargProjX -1 1")
plotsvert.append("uncTargProjY -1 1")

plotspart = []
plotspart.append("TrkChisq 0 50")
plotspart.append("TrkZ0 -5 5")
plotspart.append("P 0 1.5")
#plotspart.append("LambdaKink0 -0.01 0.01")
plotspart.append("LambdaKink1 -0.01 0.01")
plotspart.append("LambdaKink2 -0.01 0.01")
plotspart.append("LambdaKink3 -0.01 0.01")
if(isL1L2 or isL2L2):
	plotspart.append("LambdaKink4 -0.01 0.01")
	plotspart.append("LambdaKink5 -0.01 0.01")
	plotspart.append("LambdaKink6 -0.01 0.01")
	plotspart.append("PhiKink0 -0.01 0.01")
plotspart.append("PhiKink1 -0.01 0.01")
plotspart.append("PhiKink2 -0.01 0.01")
plotspart.append("PhiKink3 -0.01 0.01")
if(isL1L2 or isL2L2):
	plotspart.append("PhiKink4 -0.01 0.01")
	plotspart.append("PhiKink5 -0.01 0.01")
	plotspart.append("PhiKink6 -0.01 0.01")

othercuts = []
othercuts.append("BaduncP<9999")
othercuts.append("otherEleP<-9998&&othereleTrackP<-9998")
othercuts.append("otherEleP>-9998&&othereleTrackP<-9998")
othercuts.append("otherEleP<-9998&&othereleTrackP>-9998")
othercuts.append("otherEleP>-9998&&othereleTrackP>-9998")
othercuts.append("otherPosP<-9998&&otherposTrackP<-9998")
othercuts.append("otherPosP>-9998&&otherposTrackP<-9998")
othercuts.append("otherPosP<-9998&&otherposTrackP>-9998")
othercuts.append("otherPosP>-9998&&otherposTrackP>-9998")

otherplots = []
otherplots.append("otherEleP 0 1.5")
otherplots.append("otherPosP 0 1.5")
otherplots.append("othereleTrackP 0 1.5")
otherplots.append("otherposTrackP 0 1.5")
otherplots.append("otherElepdgid -25 25")
otherplots.append("otherPospdgid -25 25")
otherplots.append("otherEleparentID -25 650")
otherplots.append("otherPosparentID -25 650")
otherplots.append("otherEleP+eleP+posP 0 2.5")
otherplots.append("otherPosP+eleP+posP 0 2.5")
otherplots.append("otherEleP+eleBadP+posBadP 0 2.5")
otherplots.append("otherPosP+eleBadP+posBadP 0 2.5")
otherplots.append("otherEleP+eleTruthP+posTruthP 0 2.5")
otherplots.append("otherPosP+eleTruthP+posTruthP 0 2.5")
otherplots.append("othereleTrackP+eleBadP+posBadP 0 2.5")
otherplots.append("otherposTrackP+eleBadP+posBadP 0 2.5")
otherplots.append("othereleTrackP+eleTruthP+posTruthP 0 2.5")
otherplots.append("otherposTrackP+eleTruthP+posTruthP 0 2.5")
otherplots.append("othereleTrackP-otherEleP -2.5 2.5")
otherplots.append("otherposTrackP-otherPosP -2.5 2.5")

plots2D = []
plots2D.append("eleL1tthetaY+eleL2tthetaY BaduncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("posL1tthetaY+posL2tthetaY BaduncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("eleL1tthetaY+eleL2tthetaY TruthuncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("posL1tthetaY+posL2tthetaY TruthuncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("eleL1bthetaY+eleL2bthetaY BaduncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("posL1bthetaY+posL2bthetaY BaduncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("eleL1bthetaY+eleL2bthetaY TruthuncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("posL1bthetaY+posL2bthetaY TruthuncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("eleL3tthetaY+eleL4tthetaY BaduncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("posL3tthetaY+posL4tthetaY BaduncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("eleL3tthetaY+eleL4tthetaY TruthuncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("posL3tthetaY+posL4tthetaY TruthuncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("eleL3bthetaY+eleL4bthetaY BaduncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("posL3bthetaY+posL4bthetaY BaduncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("eleL3bthetaY+eleL4bthetaY TruthuncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("posL3bthetaY+posL4bthetaY TruthuncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
if(isL1L2 or isL2L2):
	plots2D.append("eleL5tthetaY+eleL6tthetaY BaduncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
	plots2D.append("posL5tthetaY+posL6tthetaY BaduncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
	plots2D.append("eleL5tthetaY+eleL6tthetaY TruthuncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
	plots2D.append("posL5tthetaY+posL6tthetaY TruthuncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
	plots2D.append("eleL5bthetaY+eleL6bthetaY BaduncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
	plots2D.append("posL5bthetaY+posL6bthetaY BaduncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
	plots2D.append("eleL5bthetaY+eleL6bthetaY TruthuncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
	plots2D.append("posL5bthetaY+posL6bthetaY TruthuncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))

#rootfile = TFile(outfile+".root","recreate")

openPDF(outfile,c)

for i in range(len(cuts)):
	saveTuplePlot2D(events,"BaduncM","BaduncVZ",nBins,0,0.1,nBins,minVZ,maxVZ,outfile,c,"uncM [GeV]","uncVZ [mm]","Bad "+cuts[i],cuts[i],1)
	saveTuplePlot2D(events,"TruthuncM","TruthuncVZ",nBins,0,0.1,nBins,minVZ,maxVZ,outfile,c,"uncM [GeV]","uncVZ [mm]","Truth "+cuts[i],cuts[i],1)

for j in range(len(plotsvert)):
	plot = getPlotX(plotsvert[j])
	minX = getMin(plotsvert[j])
	maxX = getMax(plotsvert[j])
	plotVert(events,plot,nBins,minX,maxX,nBins,minVZ,maxVZ,outfile,c,plot,plot,cut)

for i in range(len(plotspart)):
	plot = getPlotX(plotspart[i])
	minX = getMin(plotspart[i])
	maxX = getMax(plotspart[i])
	plotPart(events,plot,nBins,minX,maxX,nBins,minVZ,maxVZ,outfile,c,plot,plot,cut)

for i in range(0,len(plots2D)):
	x = getPlotX(plots2D[i])
	y = getPlotY(plots2D[i])
	minX = getMinX(plots2D[i])
	maxX = getMaxX(plots2D[i])
	minY = getMinY(plots2D[i])
	maxY = getMaxY(plots2D[i])
	saveTuplePlot2D(events,x,y,nBins,minX,maxX,nBins,minY,maxY,outfile,c,x,y,y+" vs "+x,cut)

for i in range(len(othercuts)):
	saveTuplePlot2D(events,"BaduncM","BaduncVZ",nBins,0,0.1,nBins,minVZ,maxVZ,outfile,c,"uncM [GeV]","uncVZ [mm]","Bad "+othercuts[i],cut+"&&"+othercuts[i],1)
	saveTuplePlot2D(events,"TruthuncM","TruthuncVZ",nBins,0,0.1,nBins,minVZ,maxVZ,outfile,c,"uncM [GeV]","uncVZ [mm]","Truth "+othercuts[i],cut+"&&"+othercuts[i],1)
	saveTuplePlot2D(events,"otherEleP","BaduncVZ",nBins,0,1.5,nBins,minVZ,maxVZ,outfile,c,"otherEleP [GeV]","uncVZ [mm]","Bad "+othercuts[i],cut+"&&"+othercuts[i],1)
	saveTuplePlot2D(events,"otherEleP","TruthuncVZ",nBins,0,1.5,nBins,minVZ,maxVZ,outfile,c,"otherEleP [GeV]","uncVZ [mm]","Truth "+othercuts[i],cut+"&&"+othercuts[i],1)
	saveTuplePlot2D(events,"othereleTrackP","BaduncVZ",nBins,0,1.5,nBins,minVZ,maxVZ,outfile,c,"othereleTrackP [GeV]","uncVZ [mm]","Bad "+othercuts[i],cut+"&&"+othercuts[i],1)
	saveTuplePlot2D(events,"othereleTrackP","TruthuncVZ",nBins,0,1.5,nBins,minVZ,maxVZ,outfile,c,"othereleTrackP [GeV]","uncVZ [mm]","Truth "+othercuts[i],cut+"&&"+othercuts[i],1)
	saveTuplePlot2D(events,"otherPosP","BaduncVZ",nBins,0,1.5,nBins,minVZ,maxVZ,outfile,c,"otherPosP [GeV]","uncVZ [mm]","Bad "+othercuts[i],cut+"&&"+othercuts[i],1)
	saveTuplePlot2D(events,"otherPosP","TruthuncVZ",nBins,0,1.5,nBins,minVZ,maxVZ,outfile,c,"otherPosP [GeV]","uncVZ [mm]","Truth "+othercuts[i],cut+"&&"+othercuts[i],1)
	saveTuplePlot2D(events,"otherposTrackP","BaduncVZ",nBins,0,1.5,nBins,minVZ,maxVZ,outfile,c,"otherposTrackP [GeV]","uncVZ [mm]","Bad "+othercuts[i],cut+"&&"+othercuts[i],1)
	saveTuplePlot2D(events,"otherposTrackP","TruthuncVZ",nBins,0,1.5,nBins,minVZ,maxVZ,outfile,c,"otherposTrackP [GeV]","uncVZ [mm]","Truth "+othercuts[i],cut+"&&"+othercuts[i],1)
	for j in range(len(otherplots)):
		plot = getPlotX(otherplots[j])
		minX = getMin(otherplots[j])
		maxX = getMax(otherplots[j])
		saveplot(events,plot,nBins,minX,maxX,outfile,c,plot,plot+" "+othercuts[i],cut+"&&"+othercuts[i])

closePDF(outfile,c)
#rootfile.Close()