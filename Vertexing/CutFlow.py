import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input Data file> <input MC file> <input A' files> <input truth A' files>".format(sys.argv[0])
    print "Arguments: "
    print '\t-z: target position (default 0.5 mm)'
    print '\t-e : ebeam'
    print '\t-h: this help message'
    print

zTarg = 0.5
ebeam = 1.05

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:e:')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-e':
			ebeam = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def tupleToHisto(events,inHisto,histo,nBins,minX,maxX,cut=""):
	events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,histo,nBins,minX,maxX),cut)
	histo = ROOT.gROOT.FindObject(histo)
	return histo

def saveTuplePlot(inHisto,nBins,minX,maxX,outfile,canvas,cut="",logY=0):
	events.Draw("{0}>>({1},{2},{3})".format(inHisto,nBins,minX,maxX),cut)
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")

def drawHisto(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	histo.Draw("")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)

def saveHisto(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",logY=0,stats=0):
	drawHisto(histo,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")

def saveHisto2(histo1,histo2,canvas,outfile,legend,XaxisTitle="",YaxisTitle="",plotTitle="",logY=0,stats=0):
	drawHisto(histo1,XaxisTitle,YaxisTitle,plotTitle,stats)
	#maximum = histo1.GetMaximum()
	#if(histo2.GetMaximum() > maximum): maximum = histo2.GetMaximum()
	#histo1.GetYaxis().SetRangeUser(0,maximum*1.2)
	histo2.SetLineColor(2)
	histo2.Draw("same")
	legend.Draw("same")
	canvas.SetLogy(logY)
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

def drawHisto(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	histo.Draw("")
	#histo.GetXaxis().SetRangeUser(-5,150)
	#histo.GetYaxis().SetRangeUser(0,1.1)
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)

def getPlot(string):
	arr = string.split(" ")
	return arr[0]

def getCut(string):
	arr = string.split(" ")
	if(len(arr) < 2): return ""
	else: return arr[1]

def getLimit(string):
	arr = string.split(" ")
	if(len(arr) < 3): return ""
	else: return float(arr[2])

nBins = 50
minM = 0
maxM = 0.1
minVZ = -50
maxVZ = 70
maxZ = maxVZ
clusterT = 43

outfile = remainder[0]

datafile = open(remainder[1],"r")
dataFiles = []

for line in (raw.strip().split() for raw in datafile):
	dataFiles.append(line[0])
dataevents = TChain("ntuple")
for i in range(len(dataFiles)):
    dataevents.Add(dataFiles[i])

mcfile = open(remainder[2],"r")
mcFiles = []

for line in (raw.strip().split() for raw in mcfile):
	mcFiles.append(line[0])
mcevents = TChain("ntuple")
for i in range(len(mcFiles)):
    mcevents.Add(mcFiles[i])

apfile = open(remainder[3],"r")
apfiles = []
events = []
mass = []

for line in (raw.strip().split() for raw in apfile):
	apfiles.append(TFile(line[0]))

for i in range(len(apfiles)):
	events.append(apfiles[i].Get("ntuple"))
	events[i].Draw("triM>>dummy({0},{1},{2})".format(1000,0,1))
	dummy = ROOT.gROOT.FindObject("dummy")
	mass.append(dummy.GetMean())
	del dummy

truthapfile = open(remainder[4],"r")
truthapfiles = []
truthevents = []

for line in (raw.strip().split() for raw in truthapfile):
	truthapfiles.append(TFile(line[0]))

for i in range(len(truthapfiles)):
	truthevents.append(truthapfiles[i].Get("ntuple"))

cuts = []
#cuts.append("isPair1 0.5 1")
#cuts.append("eleHasL1&&posHasL1 0.5 1")
cuts.append("eleClY*posClY 0 0")
cuts.append("max(eleMatchChisq,posMatchChisq) 10 0")
cuts.append("abs(eleClT-posClT) 2 0")
cuts.append("max(abs(eleClT-eleTrkT-{0}),abs(posClT-posTrkT-{0})) 4 0".format(clusterT))
cuts.append("bscChisq 10 0")
cuts.append("bscChisq-uncChisq 5 0")
cuts.append("max(eleTrkChisq/eleNTrackHits,posTrkChisq/posNTrackHits) 5 0")
cuts.append("abs(eleP-posP)/(eleP+posP) 0.5 0")
cuts.append("eleP 0.788 0")
cuts.append("uncP 1.21 0")
cuts.append("min(eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY)) 0 1".format(zTarg))
cuts.append("uncP 0.84 1")
#cuts.append("sqrt((bscVX-(bscVZ-{0})*bscPX/bscPZ)**2/0.25+(bscVY-(bscVZ-{0})*bscPY/bscPZ)**2/0.125) 1 0".format(zTarg))
#cuts.append("sqrt((uncVX-(uncVZ-{0})*uncPX/uncPZ)**2+(uncVY-(uncVZ-{0})*uncPY/uncPZ)**2/0.25) 1 0".format(zTarg))

cut = "uncP<9999"
datahistos = []
mchistos = []

openPDF(outfile,c)

effmasscuthistos = []
for i in range(len(cuts)):
	plot = getPlot(cuts[i])
	cutval = getCut(cuts[i])
	lim = getLimit(cuts[i])
	newcut = plot+">"+str(cutval)
	if(lim == 0):
		newcut = plot+"<"+str(cutval)
	cut = cut + "&&" + newcut
	datahistos.append(tupleToHisto(dataevents,"uncVZ","datahisto"+str(i),nBins,minVZ,maxVZ,cut))
	mchistos.append(tupleToHisto(mcevents,"uncVZ","mchisto"+str(i),nBins,minVZ,maxVZ,cut))
	saveTuplePlot2D(dataevents,"uncM","uncVZ",nBins,minM,maxM,nBins,minVZ,maxVZ,outfile,c,"uncM","uncVZ"," Data " + newcut,cut)
	saveTuplePlot2D(mcevents,"uncM","uncVZ",nBins,minM,maxM,nBins,minVZ,maxVZ,outfile,c,"uncM","uncVZ"," MC " + newcut,cut)
	effhistos = []
	for j in range(len(events)):
		events[j].Draw("triEndZ>>histoRecon({0},{1},{2})".format(nBins,zTarg,maxZ),cut)
		histoRecon = ROOT.gROOT.FindObject("histoRecon")
		truthevents[j].Draw("triEndZ>>histoTruth({0},{1},{2})".format(nBins,zTarg,maxZ))
		histoTruth = ROOT.gROOT.FindObject("histoTruth")
		effhisto = TH1F("effhisto","effhisto",nBins,zTarg,maxZ)
		for k in range(nBins):
			if (histoTruth.GetBinContent(k+1) == 0):
				effhisto.SetBinContent(k+1,0)
			else:
				effhisto.SetBinContent(k+1,histoRecon.GetBinContent(k+1)/histoTruth.GetBinContent(k+1))
		saveHisto(effhisto,outfile,c,"z [mm]","eff","Efficiency A' {0}".format(str(mass[j])))
		effhistos.append(effhisto)
		saveTuplePlot2D(events[j],"uncM","uncVZ",nBins,minM,maxM,nBins,minVZ,maxVZ,outfile,c,"uncM","uncVZ",str(mass[j]) + " GeV A' " + newcut,cut)
		del histoRecon
		del histoTruth
		del effhisto
	effmasscuthistos.append(effhistos)
	del effhistos

dum1 = datahistos[0]
dum2 = mchistos[0]

legend = TLegend(.68,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(dum1,"Data","LP")
legend.AddEntry(dum2,"MC","LP")

for i in range(len(datahistos)):
	saveHisto2(datahistos[i],mchistos[i],c,outfile,legend,"uncVZ","","uncVZ " + getPlot(cuts[i]),1,1)

legend2 = TLegend(.68,.36,.92,.87)
legend2.SetBorderSize(0)
legend2.SetFillColor(0)
legend2.SetFillStyle(0)
legend2.SetTextFont(42)
legend2.SetTextSize(0.025)

for i in range(len(datahistos)):
	color = i + 1
	if(i > 8):
		color = i + 2
	if(i == 0):
		datahistos[i].Draw()
	else:
		datahistos[i].Draw("same")
	datahistos[i].SetLineColor(color)
	legend2.AddEntry(datahistos[i],cuts[i],"LP")

datahistos[0].SetTitle("Data Cut Flow")
datahistos[0].GetXaxis().SetTitle("uncVZ")
legend2.Draw("same")
c.SetLogy(1)
c.Print(outfile+".pdf")

for i in range(len(mchistos)):
	color = i + 1
	if(i > 8):
		color = i + 2
	if(i == 0):
		mchistos[i].Draw()
	else:
		mchistos[i].Draw("same")
	mchistos[i].SetLineColor(color)

mchistos[0].SetTitle("MC Cut Flow")
mchistos[0].GetXaxis().SetTitle("uncVZ")
legend2.Draw("same")
c.Print(outfile+".pdf")

c.SetLogy(0)

for i in range(len(events)):
	for j in range(len(cuts)):
		color = j + 1
		if(j > 8):
			color = j + 2
		if(j == 0):
			effmasscuthistos[j][i].Draw()
		else:
			effmasscuthistos[j][i].Draw("same")
		effmasscuthistos[j][i].SetLineColor(color)
	effmasscuthistos[j][0].SetTitle("Efficiency Cut Flow A' {0} GeV".format(mass[i]))
	effmasscuthistos[j][0].GetXaxis().SetTitle("uncVZ")
	effmasscuthistos[j][0].GetXaxis().SetTitle("efficiency")
	legend2.Draw("same")
	c.Print(outfile+".pdf")

	

closePDF(outfile,c)