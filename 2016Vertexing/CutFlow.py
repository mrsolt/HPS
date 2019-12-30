import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input text Data file> <input text MC file> <input text A' files>".format(sys.argv[0])
    print 'Note: Even when not using a data, MC, or Ap file, you must feed a dummy text file'
    print "Arguments: "
    print '\t-z: target position (default -4.3 mm)'
    print '\t-m: minimum uncVZ (default -60 mm)'
    print '\t-n: maximum uncVZ (default 60 mm)'
    print '\t-e: beam energy (default 2.3 GeV)'
    print '\t-b: number of bins (default 50)'
    print '\t-d: do not use data file (default use)'
    print '\t-c: do not use MC file (default use)'
    print '\t-a: do not use Ap file (default use)'
    print '\t-h: this help message'
    print

zTarg = -4.3
ebeam = 2.3
minVZ = -60
maxVZ = 60
nBins = 50
useData = True
useMC = True
useAp = True
clusterT = 56

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:m:n:e:b:dca')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-e':
			ebeam = float(arg)
		if opt=='-b':
			nBins = float(arg)
		if opt=='-d':
			useData = False
		if opt=='-c':
			useMC = False
		if opt=='-a':
			useAp = False
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def comparePlot(events0,events1,events2,inHisto,nBins,minX,maxX,outfile,canvas,title0,title1,title2,XaxisTitle="",YaxisTitle="",plotTitle="",cut="",stats=0,logY=0):
	events0.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo0",nBins,minX,maxX),cut)
	events1.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo1",nBins,minX,maxX),cut)
	events2.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo2",nBins,minX,maxX),cut)
	histo0 = ROOT.gROOT.FindObject("histo0")
	histo1 = ROOT.gROOT.FindObject("histo1")
	histo2 = ROOT.gROOT.FindObject("histo2")
	if(histo0.GetEntries() != 0):
		histo0.Scale(1./histo0.GetEntries())
	if(histo1.GetEntries() != 0):
		histo1.Scale(1./histo1.GetEntries())
	if(histo2.GetEntries() != 0):
		histo2.Scale(1./histo2.GetEntries())
	maximum = histo0.GetMaximum()
	if(histo1.GetMaximum() > maximum):
		maximum = histo1.GetMaximum()
	if(histo2.GetMaximum() > maximum):
		maximum = histo2.GetMaximum()
	histo0.GetYaxis().SetRangeUser(0,1.2*maximum)
	histo0.Draw()
	histo0.SetTitle(plotTitle)
	histo0.GetXaxis().SetTitle(XaxisTitle)
	histo0.GetYaxis().SetTitle(YaxisTitle)
	histo0.SetStats(stats)
	histo1.SetLineColor(2)
	histo1.Draw("same")
	histo2.SetLineColor(6)
	histo2.Draw("same")
	legend = TLegend(.58,.46,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histo0,title0,"LP")
	legend.AddEntry(histo1,title1,"LP")
	legend.AddEntry(histo2,title2,"LP")
	legend.Draw("same")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	del histo0
	del histo1
	del histo2

def saveCutFlow(events,inHisto,cuts,nBins,minX,maxX,labels,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	histos = []
	histos2 = []
	cut_tot = ""
	for i in range(len(cuts)):
		cut = cuts[i]
		cuts_1 = ""
		if(i == 0):
			cut_tot = cut
		else:
			cut_tot = cut_tot + "&&" + cut
		for j in range(len(cuts)):
			if(j != i):
				if(cuts_1 != ""):
					cuts_1 = cuts_1 + "&&" + cuts[j]
				else:
					cuts_1 = cuts[j]
		events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo{0}".format(i),nBins,minX,maxX),cut_tot)
		histos.append(ROOT.gROOT.FindObject("histo{0}".format(i)))
		events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo2{0}".format(i),nBins,minX,maxX),cuts_1)
		histos2.append(ROOT.gROOT.FindObject("histo2{0}".format(i)))
	histos[0].SetTitle(plotTitle + " Inclusive")
	histos[0].GetXaxis().SetTitle(XaxisTitle)
	histos[0].GetYaxis().SetTitle(YaxisTitle)
	histos[0].SetStats(stats)
	color = 1
	for i in range(len(histos)):
		if(color == 5 or color == 10):
			color = color + 1
		histos[i].SetLineColor(color)
		color = color + 1
		histos[i].Scale(1.0)
		if(i == 0):
			histos[i].Draw("")
		else:
			histos[i].Draw("same")
	legend = TLegend(.58,.46,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	for i in range(len(labels)):
		legend.AddEntry(histos[i],labels[i],"LP")
	legend.Draw("")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	histos2[0].SetTitle(plotTitle + " Exclusive")
	histos2[0].GetXaxis().SetTitle(XaxisTitle)
	histos2[0].GetYaxis().SetTitle(YaxisTitle)
	histos2[0].SetStats(stats)
	color = 1
	for i in range(len(histos2)):
		if(color == 5 or color == 10):
			color = color + 1
		histos2[i].SetLineColor(color)
		color = color + 1
		histos2[i].Scale(1.0)
		if(i == 0):
			histos2[i].Draw("")
		else:
			histos2[i].Draw("same")
	legend2 = TLegend(.58,.46,.92,.87)
	legend2.SetBorderSize(0)
	legend2.SetFillColor(0)
	legend2.SetFillStyle(0)
	legend2.SetTextFont(42)
	legend2.SetTextSize(0.035)
	for i in range(len(labels)):
		legend2.AddEntry(histos2[i],labels[i],"LP")
	legend2.Draw("")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	del histos
	del histos2

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

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

if(useAp):
	for i in range(len(apfiles)):
		events.append(apfiles[i].Get("ntuple"))
		events[i].Draw("triM>>dummy({0},{1},{2})".format(1000,0,1))
		dummy = ROOT.gROOT.FindObject("dummy")
		mass.append(dummy.GetMean())
		del dummy

plots = []
plots.append("uncVZ {0} {1}".format(minVZ,maxVZ))
plots.append("uncM {0} {1}".format(0.0,0.1*ebeam))
plots.append("uncP {0} {1}".format(0,1.2*ebeam))

plotlabels = []
plotlabels.append("Reconstructed z [mm]")
plotlabels.append("Reconstructed Mass [GeV]")
plotlabels.append("V0 Momentum [GeV]")

cuts = []
cuts.append("uncP<9999")
cuts.append("eleHasL1&&posHasL1")
cuts.append("eleHasL2&&posHasL2")
cuts.append("eleMatchChisq<10&&posMatchChisq<10")
cuts.append("abs(eleClT-posClT)<2")
cuts.append("abs(eleClT-eleTrkT-{0})<2".format(clusterT))
cuts.append("abs(posClT-posTrkT-{0})<2".format(clusterT))
cuts.append("eleTrkChisq/(2*eleNTrackHits-5)<6")
cuts.append("posTrkChisq/(2*posNTrackHits-5)<6")
cuts.append("uncChisq<10")


#cuts.append("eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY)>-1.0".format(zTarg))
#cuts.append("posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY)>-1.0".format(zTarg))
#cuts.append("eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY)>-0.8".format(zTarg))
#cuts.append("posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY)>-0.8".format(zTarg))
#cuts.append("eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY)>-0.6".format(zTarg))
#cuts.append("posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY)>-0.6".format(zTarg))
#cuts.append("eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY)>-0.4".format(zTarg))
#cuts.append("posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY)>-0.4".format(zTarg))
#cuts.append("eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY)>-0.2".format(zTarg))
#cuts.append("posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY)>-0.2".format(zTarg))
#cuts.append("eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY)>0.0".format(zTarg))
#cuts.append("posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY)>0.0".format(zTarg))
#cuts.append("eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY)>0.2".format(zTarg))
#cuts.append("posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY)>0.2".format(zTarg))
#cuts.append("eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY)>0.4".format(zTarg))
#cuts.append("posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY)>0.4".format(zTarg))
#cuts.append("eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY)>0.6".format(zTarg))
#cuts.append("posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY)>0.6".format(zTarg))
#cuts.append("eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY)>0.8".format(zTarg))
#cuts.append("posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY)>0.8".format(zTarg))
#cuts.append("eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY)>1.0".format(zTarg))
#cuts.append("posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY)>1.0".format(zTarg))

label = []
label.append("Preprossessing")
for i in range(1,len(cuts)):
	label.append(cuts[i])

openPDF(outfile,c)

for i in range(len(plots)):
	plot = getPlot(plots[i])
	minimum = getMin(plots[i])
	maximum = getMax(plots[i])
	plotlabel = plotlabels[i]
	if(useData):
		saveCutFlow(dataevents,plot,cuts,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " Data",stats=0,logY=0)
	if(useMC):
		saveCutFlow(mcevents,plot,cuts,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " MC",stats=0,logY=0)
	if(useAp):
		for j in range(len(mass)):
			saveCutFlow(events[j],plot,cuts,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ ' Ap {0:.0f} MeV'.format(mass[j]*1000),stats=0,logY=0)

if(useData and useMC and useAp):
	for i in range(len(plots)):
		plot = getPlot(plots[i])
		minimum = getMin(plots[i])
		maximum = getMax(plots[i])
		plotlabel = plotlabels[i]
		cut_tot = ""
		mass_range = 0.005
		for j in range(len(cuts)):
			cut = cuts[j]
			cuts_1 = ""
			if(j == 0):
				cut_tot = cut
			else:
				cut_tot = cut_tot + "&&" + cut
			for k in range(len(cuts)):
				if(j != k):
					if(cuts_1 != ""):
						cuts_1 = cuts_1 + "&&" + cuts[k]
					else:
						cuts_1 = cuts[k]
			for k in range(len(mass)):
				masscut = "uncM>{0}&&uncM<{1}".format(mass[k]-mass_range,mass[k]+mass_range)
				cut1 = cut_tot + "&&" + masscut
				cut2 = cuts_1 + "&&" + masscut
				comparePlot(events[k],mcevents,dataevents,plot,nBins,minimum,maximum,outfile,c,'Ap {0:.0f} MeV'.format(mass[k]*1000),"MC","Data",XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel + " Inclusive {0}".format(label[j]),cut=cut1,stats=0,logY=0)
				comparePlot(events[k],mcevents,dataevents,plot,nBins,minimum,maximum,outfile,c,'Ap {0:.0f} MeV'.format(mass[k]*1000),"MC","Data",XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel + " Exclusive {0}".format(label[j]),cut=cut2,stats=0,logY=0)

closePDF(outfile,c)