import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import math
from array import array
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH2F, TLatex, TF1, TH1F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-l: is L1L2 (default false)'
    print '\t-z: use zcut (default false)'
    print '\t-p: save PDF (default true)'
    print '\t-m: minimum uncVZ'
    print '\t-n: maximum uncVZ'
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
	if(len(arr) < 2): return -9999
	else: return float(arr[1])

def getMaxX(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

def getMinX2D(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

def getMaxX2D(string):
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

def getScatter(actsensor,inactsensor):
	scatter = actsensor
	if(scatter < -9998):
		scatter = inactsensor
	return scatter

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def saveTuplePlot(events,inHisto,nBinsX,minX,maxX,outfile,canvas,XaxisTitle="",plotTitle="",cut="",stats=0,logY=0,savePDF=False):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBinsX,minX,maxX),cut)
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.SetStats(stats)
	histo.Draw()
	canvas.SetLogy(logY)
	if(savePDF):
	    canvas.Print(outfile+".pdf")
	histo.Write(plotTitle)
	del histo

def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",cut="",stats=0,logY=0,savePDF=False):
	events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,inHisto1,nBinsX,minX,maxX,nBinsY,minY,maxY),cut)
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw("COLZ")
	canvas.SetLogy(logY)
	if(savePDF):
	    canvas.Print(outfile+".pdf")
	histo.Write(plotTitle)
	del histo

def savehisto2D(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0,savePDF=False):
	c.SetLogz(0)
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw("COLZ")
	canvas.SetLogy(logY)
	if(savePDF):
	    canvas.Print(outfile+".pdf")
	histo.Write(plotTitle)
	del histo

L1L2 = False
minVZ = -30
maxVZ = 30
savePDF = True
useZcut = False

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'lzm:n:ph')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-l':
			L1L2 = True
		if opt=='-z':
			useZcut = True
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-p':
			savePDF = False
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(110011)
gStyle.SetPalette(1)
c = TCanvas("c","c",800,600)
c.SetLogz(1)

cut = ""
if(useZcut):
	cut = "uncVZ>{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(22.23,48.63,-5150,49760,-169900,141700)
	if(L1L2):
		cut = "uncVZ>{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(25.23,47.14,-2987,12370,0,0)

#cut = cut + "&&" + "uncM>0.06&&uncM<0.15"

masscut_nsigma = 2.80
if(not L1L2):
	mres = TF1("mres","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(0.01095/1000.,0.04305,0,0,0,0),0.04,0.2)
else:
	mres = TF1("mres","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(0.04906/1000.,0.04606,0,0,0,0),0.04,0.2)

outfile = remainder[0]
events = TChain("ntuple")
for i in range(1,len(remainder)):
    events.Add(remainder[i])

nBins = 100
minX = ""
maxX = ""
minY = ""
maxY = ""
maxTheta = 0.03
minTheta = -maxTheta

angleMC = 0.111025680707
angleData = 0.0386557750132
angle = angleMC
zTarg = -4.3
uncTargProjY = -0.0668941015569
uncTargProjYSig = 0.0831670646584
uncY =  -0.0772321507928
uncYSig = 0.0878428842895

m0 = -0.201776054859
a0 = 0.0518988558564
a1 = -0.00230111045957
b0 = 0.0471576968062
b1 = -0.00108639651791

if(L1L2):
	m0 = -0.167438502208
	a0 = 0.016762652862
	a1 = 0.00033162637213
	b0 = 0.0207347770085
	b1 = 0.000331699098944
	uncTargProjYSig = uncTargProjYSig * 1.5
	uncYSig = uncYSig * 1.5

plots2D = []
plots2D.append("uncM uncVZ 0 0.2 {0} {1}".format(minVZ,maxVZ))

rootfile = TFile(outfile+".root","recreate")
textFileName = outfile+"_table.txt"
textFile = open(textFileName,"w")

minMass = 0.06
maxMass = 0.15
nBack = TH1F("nBack","nBack",nBins,minMass,maxMass)

if(savePDF):
    openPDF(outfile,c)

for j in range(0,len(plots2D)):
	x = getPlotX(plots2D[j])
	y = getPlotY(plots2D[j])
	minX = getMinX2D(plots2D[j])
	maxX = getMaxX2D(plots2D[j])
	minY = getMinY(plots2D[j])
	maxY = getMaxY(plots2D[j])
	saveTuplePlot2D(events,x,y,nBins,minX,maxX,nBins,minY,maxY,outfile,c,x,y,y+" vs "+x+" "+cut,cut,1,savePDF=savePDF)

for i in range(nBins):
	mass = minMass + i * (maxMass - minMass)/nBins
	if(cut == ""):
		masscut = "abs({0}-{1})<{2}/2*{3}".format("uncM",mass,masscut_nsigma,mres.Eval(mass))
	else:
		masscut = cut + "&&abs({0}-{1})<{2}/2*{3}".format("uncM",mass,masscut_nsigma,mres.Eval(mass))
	events.Draw("{0}>>histo({1},{2},{3})".format("uncVZ",nBins,-30,30),masscut)
	histo = ROOT.gROOT.FindObject("histo")
	nbk = histo.GetEntries()
	nBack.SetBinContent(i+1,nbk/3)
	nBack.SetBinError(i+1,math.sqrt(nbk)/3)
	del histo

nBack.Draw()
nBack.SetTitle("Number of Background Events")
nBack.GetXaxis().SetTitle("Mass (GeV)")
nBack.SetStats(0)
nBack.Fit('pol2')
nBack.Write("Background")
c.Print(outfile+".pdf")

def getUnbiased(mass,masswindow,histoback):
    histoclone = histoback.Clone()
    for i in range(histoclone.GetNbinsX()):
        nbin = i + 1
        m = histoback.GetBinCenter(nbin) 
        if(abs(mass - m) < masswindow):
            histoclone.SetBinError(nbin,0)
    fit = TF1("fit","pol2")
    histoclone.Fit('fit')
    backnew = fit.Eval(mass)
    return backnew

nBackunbiased = TH1F("nBackunbiased","nBackunbiased",nBins,minMass,maxMass)

for i in range(nBins):
	mass = minMass + i * (maxMass - minMass)/nBins
	if(cut == ""):
		masscut = "abs({0}-{1})<{2}/2*{3}".format("uncM",mass,masscut_nsigma,mres.Eval(mass))
	else:
		masscut = cut + "&&abs({0}-{1})<{2}/2*{3}".format("uncM",mass,masscut_nsigma,mres.Eval(mass))
	events.Draw("{0}>>histo({1},{2},{3})".format("uncVZ",nBins,-30,30),masscut)
	histo = ROOT.gROOT.FindObject("histo")
	nbknew = getUnbiased(mass,mres.Eval(mass)/2*masscut_nsigma,nBack)
	nbk = nBack.GetBinContent(i+1)
	nBackunbiased.SetBinContent(i+1,nbknew)
	#nBackunbiased.SetBinError(i+1,math.sqrt(nbk))
	del histo

nBack.SetLineColor(1)
nBack.Draw()
nBack.SetTitle("Number of Background Events")
nBack.GetXaxis().SetTitle("Mass (GeV)")
nBack.SetStats(0)
nBackunbiased.SetLineColor(4)
nBackunbiased.Draw("same")
nBackunbiased.SetStats(0)
nBackunbiased.Write("Background Unbiased")
legend = TLegend(.70,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(nBack,"Biased","LP")
legend.AddEntry(nBackunbiased,"Unbiased","LP")
legend.Draw("same")
c.Print(outfile+".pdf")

scatter = TH2F("scatter","scatter",100,0,maxTheta/2,100,0,maxTheta/2)
scatterL1 = TH2F("scatterL1","scatterL1",100,0,maxTheta/2,100,0,maxTheta/2)
scatterL2 = TH2F("scatterL2","scatterL2",100,0,maxTheta/2,100,0,maxTheta/2)
scattermax = TH2F("scattermax","scattermax",100,0,maxTheta/2,100,0,maxTheta/2)

cutevents = events.CopyTree(cut)
neventscut = cutevents.GetEntries()

uncVX = array('d',[0])
uncVY = array('d',[0])
uncVZ = array('d',[0])

uncPX = array('d',[0])
uncPY = array('d',[0])
uncPZ = array('d',[0])
uncP = array('d',[0])

uncM = array('d',[0])
uncChisq = array('d',[0])

eleTrkZ0 = array('d',[0])
posTrkZ0 = array('d',[0])
elePY = array('d',[0])
posPY = array('d',[0])

eleL1tthetaY = array('d',[0])
eleL2tthetaY = array('d',[0])
eleL1bthetaY = array('d',[0])
eleL2bthetaY = array('d',[0])

eleL1tInthetaY = array('d',[0])
eleL2tInthetaY = array('d',[0])
eleL1bInthetaY = array('d',[0])
eleL2bInthetaY = array('d',[0])

posL1tthetaY = array('d',[0])
posL2tthetaY = array('d',[0])
posL1bthetaY = array('d',[0])
posL2bthetaY = array('d',[0])

posL1tInthetaY = array('d',[0])
posL2tInthetaY = array('d',[0])
posL1bInthetaY = array('d',[0])
posL2bInthetaY = array('d',[0])

cutevents.Branch("uncVX",uncVX,"uncVX")
cutevents.Branch("uncVY",uncVY,"uncVY")
cutevents.Branch("uncVZ",uncVZ,"uncVZ")

cutevents.Branch("uncPX",uncPX,"uncPX")
cutevents.Branch("uncPY",uncPY,"uncPY")
cutevents.Branch("uncPZ",uncPZ,"uncPZ")
cutevents.Branch("uncP",uncP,"uncP")

cutevents.Branch("uncM",uncM,"uncM")
cutevents.Branch("uncChisq",uncChisq,"uncChisq")

cutevents.Branch("eleTrkZ0",eleTrkZ0,"eleTrkZ0")
cutevents.Branch("posTrkZ0",posTrkZ0,"posTrkZ0")
cutevents.Branch("elePY",elePY,"elePY")
cutevents.Branch("posPY",posPY,"posPY")

cutevents.Branch("eleL1tthetaY",eleL1tthetaY,"eleL1tthetaY/D")
cutevents.Branch("eleL2tthetaY",eleL2tthetaY,"eleL2tthetaY/D")
cutevents.Branch("eleL1bthetaY",eleL1bthetaY,"eleL1bthetaY/D")
cutevents.Branch("eleL2bthetaY",eleL2bthetaY,"eleL2bthetaY/D")

cutevents.Branch("eleL1tInthetaY",eleL1tInthetaY,"eleL1tInthetaY/D")
cutevents.Branch("eleL2tInthetaY",eleL2tInthetaY,"eleL2tInthetaY/D")
cutevents.Branch("eleL1bInthetaY",eleL1bInthetaY,"eleL1bInthetaY/D")
cutevents.Branch("eleL2bInthetaY",eleL2bInthetaY,"eleL2bInthetaY/D")

cutevents.Branch("posL1tthetaY",posL1tthetaY,"posL1tthetaY/D")
cutevents.Branch("posL2tthetaY",posL2tthetaY,"posL2tthetaY/D")
cutevents.Branch("posL1bthetaY",posL1bthetaY,"posL1bthetaY/D")
cutevents.Branch("posL2bthetaY",posL2bthetaY,"posL2bthetaY/D")

cutevents.Branch("posL1tInthetaY",posL1tInthetaY,"posL1tInthetaY/D")
cutevents.Branch("posL2tInthetaY",posL2tInthetaY,"posL2tInthetaY/D")
cutevents.Branch("posL1bInthetaY",posL1bInthetaY,"posL1bInthetaY/D")
cutevents.Branch("posL2bInthetaY",posL2bInthetaY,"posL2bInthetaY/D")

textFile.write('VZ (mm) & Mass (MeV) & $theta_{1}$ (mrad) & $theta_{2}$ (mrad) & $chi^2_{unc}$ & V0 Proj Y ($n_{\sigma}$) & VY ($n_{\sigma}$) & $\Delta \ e^- \ z0$ (mm) & $\Delta \ e^+ \ z0$ (mm)\n')
for entry in xrange(neventscut):
	cutevents.GetEntry(entry)
	eleL1t = getScatter(cutevents.eleL1tthetaY,cutevents.eleL1tInthetaY)
	eleL2t = getScatter(cutevents.eleL2tthetaY,cutevents.eleL2tInthetaY)
	posL1t = getScatter(cutevents.posL1tthetaY,cutevents.posL1tInthetaY)
	posL2t = getScatter(cutevents.posL2tthetaY,cutevents.posL2tInthetaY)
	eleL1b = getScatter(cutevents.eleL1bthetaY,cutevents.eleL1bInthetaY)
	eleL2b = getScatter(cutevents.eleL2bthetaY,cutevents.eleL2bInthetaY)
	posL1b = getScatter(cutevents.posL1bthetaY,cutevents.posL1bInthetaY)
	posL2b = getScatter(cutevents.posL2bthetaY,cutevents.posL2bInthetaY)

	scatter.Fill(-(eleL1t+eleL2t),(posL1b+posL2b),cutevents.uncVZ)
	scatter.Fill(-(posL1t+posL2t),(eleL1b+eleL2b),cutevents.uncVZ)
	scatterL1.Fill(-(eleL1t),(posL1b),cutevents.uncVZ)
	scatterL1.Fill(-(posL1t),(eleL1b),cutevents.uncVZ)
	scatterL2.Fill(-(eleL2t),(posL2b),cutevents.uncVZ)
	scatterL2.Fill(-(posL2t),(eleL2b),cutevents.uncVZ)
	scattermax.Fill(max(max(-eleL1t,-9998),max(-eleL2t,-9998)),max(posL1b,posL2b),cutevents.uncVZ)
	scattermax.Fill(max(max(-posL1t,-9998),max(-posL2t,-9998)),max(eleL1b,eleL2b),cutevents.uncVZ)

	xProj = (cutevents.uncVX-(cutevents.uncVZ-zTarg)*cutevents.uncPX/cutevents.uncPZ)
	yProj = (cutevents.uncVY-(cutevents.uncVZ-zTarg)*cutevents.uncPY/cutevents.uncPZ)
	yProj_rot = xProj*math.sin(angle)+yProj*math.cos(angle)

	projY = abs(yProj_rot - uncTargProjY) / uncTargProjYSig
	VY = abs(cutevents.uncVY - uncY) / uncYSig

	if(cutevents.elePY > 0):
		eleZ0 = cutevents.eleTrkZ0-m0+a0*cutevents.uncVZ+a1*1/cutevents.uncM*cutevents.uncVZ
		posZ0 = -cutevents.posTrkZ0-m0+b0*cutevents.uncVZ+b1*1/cutevents.uncM*cutevents.uncVZ
		textFile.write('{0:0.2f} & {1:0.2f}$ & {2:0.2f} & {3:0.2f} & {4:0.2f} & {5:0.2f} & {6:0.2f} & {7:0.2f} & {8:0.2f}\n'.format(cutevents.uncVZ,
			cutevents.uncM*1000,max(max(-eleL1t,-9998),max(-eleL2t,-9998))*1000,max(posL1b,posL2b)*1000,cutevents.uncChisq,projY,VY,eleZ0,posZ0))
	else:
		eleZ0 = -cutevents.eleTrkZ0-m0+b0*cutevents.uncVZ+b1*1/cutevents.uncM*cutevents.uncVZ
		posZ0 = cutevents.posTrkZ0-m0+a0*cutevents.uncVZ+a1*1/cutevents.uncM*cutevents.uncVZ
		textFile.write('{0:0.2f} & {1:0.2f}$ & {2:0.2f} & {3:0.2f} & {4:0.2f} & {5:0.2f} & {6:0.2f} & {7:0.2f} & {8:0.2f}\n'.format(cutevents.uncVZ,
			cutevents.uncM*1000,max(max(-posL1t,-9998),max(-posL2t,-9998))*1000,max(eleL1b,eleL2b)*1000,cutevents.uncChisq,projY,VY,eleZ0,posZ0))

savehisto2D(scatter,outfile,c,"#theta_{bot}","#theta_{top}","Top Scatter vs Bottom Scatter L1 + L2",0,savePDF=savePDF)
savehisto2D(scatterL1,outfile,c,"#theta_{bot}","#theta_{top}","Top Scatter vs Bottom Scatter L1",0,savePDF=savePDF)
savehisto2D(scatterL2,outfile,c,"#theta_{bot}","#theta_{top}","Top Scatter vs Bottom Scatter L2",0,savePDF=savePDF)
savehisto2D(scattermax,outfile,c,"#theta_{bot}","#theta_{top}","Top Scatter vs Bottom Scatter Max L1 L2",0,savePDF=savePDF)

textFile.close()
if(savePDF):
    closePDF(outfile,c)
rootfile.Close()