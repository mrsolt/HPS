import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TPad
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input text Data file> <input text MC file> <input text A' files>".format(sys.argv[0])
    print "Arguments: "
    print '\t-z: target position (default -4.3 mm)'
    print '\t-m: minimum uncVZ (default -30 mm)'
    print '\t-n: maximum uncVZ (default 60 mm)'
    print '\t-e: beam energy (default 2.3 GeV)'
    print '\t-b: number of bins (default 100)'
    print '\t-h: this help message'
    print

zTarg = -4.3
ebeam = 2.3
minVZ = -40
maxVZ = 40
nBins = 100


options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:m:n:e:b:')

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
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def saveTuplePlot(eventsmc,eventsdata,inHisto,inHistodata,nBins,minX,maxX,outfile,canvas,cut=""):
	canvas.Clear()
	RatioMin = 0.8
	RatioMax = 1.2
	eventsmc.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBins,minX,maxX),cut)
	histo = ROOT.gROOT.FindObject("histo")
	eventsdata.Draw("{0}>>histo2({1},{2},{3})".format(inHistodata,nBins,minX,maxX),cut)
	histo2 = ROOT.gROOT.FindObject("histo2")

	top = TPad("top","top",0,0.42,1,1)
	#top.SetLogy(logY)
    
	bot = TPad("bot","bot",0,0,1,0.40)
    
	top.Draw()
	top.SetBottomMargin(0)
	#top.SetTopMargin(gStyle.GetPadTopMargin()*topScale)
	bot.Draw()
	bot.SetTopMargin(0)
	bot.SetBottomMargin(0.4)
	top.cd()

	histo.SetTitle("{0}".format(inHisto))
	histo.GetXaxis().SetTitle("{0}".format(inHisto))
	histo.Sumw2()
	histo2.Sumw2()
	histo.Scale(1/histo.Integral())
	histo2.Scale(1/histo2.Integral())
	histo2.SetLineColor(2)
	histo.Draw("")
	histo2.Draw("same")
	legend = TLegend(.65,.66,.97,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histo,"MC","LP")
	legend.AddEntry(histo2,"Data","LP")
	legend.Draw("")

	bot.cd()
	reference = histo.Clone("reference")
	reference.GetYaxis().SetTitle("Ratio")
	reference.GetYaxis().SetTitleSize(0.06)
	reference.GetYaxis().SetLabelSize(0.1)
	reference.GetXaxis().SetTitleSize(0.1)
	reference.GetXaxis().SetLabelSize(0.1)
	reference.GetXaxis().SetTitle("{0}".format(inHisto))
	reference.GetYaxis().SetRangeUser(RatioMin,RatioMax)
	reference.GetYaxis().SetNdivisions(508)
	reference.GetYaxis().SetDecimals(True)
	reference.Draw("axis")
	ratio = histo2.Clone("Ratio"+histo2.GetName())
	ratio.Divide(reference)
	ratio.DrawCopy("pe same")



	canvas.Print(outfile+".pdf")
	del histo
	del histo2

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

def getCut(string):
	arr = string.split(" ")
	if(len(arr) < 4): return ""
	else: return arr[3]

outfile = remainder[0]

filemc = TFile(remainder[1])
eventsmc = filemc.Get("ntuple")

filedata = TFile(remainder[2])
eventsdata = filedata.Get("ntuple")

uncVX = -0.0916034735685
uncVXSig = 0.216732544476 
uncVY = -0.0772321507928
uncVYSig = 0.0878428842895
uncTargProjX = -0.0995461972579
uncTargProjXSig = 0.217919555935
uncTargProjY = -0.0668941015569
uncTargProjYSig = 0.0831670646584

angleMC = 0.111025680707
angleData = 0.0386557750132
angle = angleMC

dz = 0
dy = 0

xProj = "(uncVX-(uncVZ-{0})*uncPX/uncPZ)".format(zTarg)
yProj = "(uncVY-(uncVZ-{0})*uncPY/uncPZ)".format(zTarg)
uncTargProjXrot = "{0}*cos({2})-{1}*sin({2})".format(xProj,yProj,-angle)
uncTargProjYrot = "{0}*sin({2})+{1}*cos({2})".format(xProj,yProj,-angle)

plots = []
plots.append("uncVX-{2} {0} {1}".format(-1,1,uncVX))
plots.append("uncVY-{2} {0} {1}".format(-0.5,0.5,uncVY))
plots.append("(uncVX-{2})/{3} {0} {1}".format(-4,4,uncVX,uncVXSig))
plots.append("(uncVY-{2})/{3} {0} {1}".format(-4,4,uncVY,uncVYSig))
plots.append("uncVZ+{2} {0} {1}".format(-30,30,dz))
plots.append("sqrt(uncCovZZ) {0} {1}".format(0,5))
plots.append("(uncVZ+{2}+4.3)/sqrt(uncCovZZ) {0} {1}".format(-10,10,dz))
plots.append("uncP {0} {1}".format(0,2.4))
#Smear P
plots.append("eleP {0} {1}".format(0,2.4))
plots.append("posP {0} {1}".format(0,2.4))
plots.append("eleTrkLambda {0} {1}".format(-0.1,0.1))
plots.append("posTrkLambda {0} {1}".format(-0.1,0.1))
plots.append("eleTrkZ0-{2}+(-4.3)*eleTrkLambda {0} {1}".format(-0.5,0.5,dy))
plots.append("posTrkZ0-{2}+(-4.3)*posTrkLambda {0} {1}".format(-0.5,0.5,dy))
plots.append("{2}-{3} {0} {1}".format(-1,1,uncTargProjXrot,uncTargProjX))
plots.append("{2}-{3} {0} {1}".format(-0.5,0.5,uncTargProjYrot,uncTargProjY))
plots.append("({2}-{3})/{4} {0} {1}".format(-4,4,uncTargProjXrot,uncTargProjX,uncTargProjXSig))
plots.append("({2}-{3})/{4} {0} {1}".format(-4,4,uncTargProjYrot,uncTargProjY,uncTargProjYSig))

angle = angleData
uncVX = -0.132067895667
uncVXSig = 0.33663731855
uncVY = -0.0743550601346
uncVYSig = 0.102015199636
uncTargProjX = -0.139824865412
uncTargProjXSig = 0.337082294325
uncTargProjY = -0.0600724148472
uncTargProjYSig = 0.0971755263948
uncTargProjXrot = "{0}*cos({2})-{1}*sin({2})".format(xProj,yProj,-angle)
uncTargProjYrot = "{0}*sin({2})+{1}*cos({2})".format(xProj,yProj,-angle)
c0 = -0.377
c1 = 13.79
c2 = -55.84
c3 = 84.0
dy = uncTargProjY - (-0.0668941015569)
dz = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3".format(c0,c1,c2,c3)

plotsdata = []
plotsdata.append("uncVX-{2} {0} {1}".format(-1,1,uncVX))
plotsdata.append("uncVY-{2} {0} {1}".format(-0.5,0.5,uncVY))
plotsdata.append("(uncVX-{2})/{3} {0} {1}".format(-4,4,uncVX,uncVXSig))
plotsdata.append("(uncVY-{2})/{3} {0} {1}".format(-4,4,uncVY,uncVYSig))
plotsdata.append("uncVZ+{2} {0} {1}".format(-30,30,dz))
plotsdata.append("sqrt(uncCovZZ) {0} {1}".format(0,5))
plotsdata.append("(uncVZ+{2}+4.3)/sqrt(uncCovZZ) {0} {1}".format(-10,10,dz))
plotsdata.append("uncP {0} {1}".format(0,2.4))
#Smear P
plotsdata.append("eleP {0} {1}".format(0,2.4))
plotsdata.append("posP {0} {1}".format(0,2.4))
plotsdata.append("eleTrkLambda {0} {1}".format(-0.1,0.1))
plotsdata.append("posTrkLambda {0} {1}".format(-0.1,0.1))
plotsdata.append("eleTrkZ0-{2}+(-4.3)*eleTrkLambda {0} {1}".format(-0.5,0.5,dy))
plotsdata.append("posTrkZ0-{2}+(-4.3)*posTrkLambda {0} {1}".format(-0.5,0.5,dy))
plotsdata.append("{2}-{3} {0} {1}".format(-1,1,uncTargProjXrot,uncTargProjX))
plotsdata.append("{2}-{3} {0} {1}".format(-0.5,0.5,uncTargProjYrot,uncTargProjY))
plotsdata.append("({2}-{3})/{4} {0} {1}".format(-4,4,uncTargProjXrot,uncTargProjX,uncTargProjXSig))
plotsdata.append("({2}-{3})/{4} {0} {1}".format(-4,4,uncTargProjYrot,uncTargProjY,uncTargProjYSig))

openPDF(outfile,c)

for i in range(len(plots)):
	plot = getPlot(plots[i])
	plotdata = getPlot(plotsdata[i])
	minimum = getMin(plots[i])
	maximum = getMax(plots[i])
	#cut = getCut(plots[i])
	saveTuplePlot(eventsmc,eventsdata,plot,plotdata,nBins,minimum,maximum,outfile,c)

closePDF(outfile,c)