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
    print '\t-t: is L2L2 (default false)'
    print '\t-z: use zcut (default false)'
    print '\t-p: save PDF (default true)'
    print '\t-d: use Data (default false)'
    print '\t-y: plot labels'
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

def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",cut="",stats=1,logY=0,savePDF=False):
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
L2L2 = False
minVZ = -30
maxVZ = 30
savePDF = True
useZcut = False
useData = False
label = ""

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'lzm:n:py:dth')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-l':
            L1L2 = True
        if opt=='-t':
            L2L2 = True
        if opt=='-z':
            useZcut = True
        if opt=='-m':
            minVZ = float(arg)
        if opt=='-n':
            maxVZ = float(arg)
        if opt=='-y':
            label = str(arg)
        if opt=='-p':
            savePDF = False
        if opt=='-d':
            useData = True
        if opt=='-h':
            print_usage()
            sys.exit(0)

gStyle.SetOptStat(110011)
gStyle.SetPalette(1)
c = TCanvas("c","c",800,600)
c.SetLogz(1)

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
if(useData):
	angle = angleData
	uncTargProjX = -0.139824865412
	uncTargProjXSig = 0.337082294325
	uncTargProjY = -0.0600724148472
	uncTargProjYSig = 0.0971755263948
	uncY =  -0.0743550601346
	uncYSig = 0.102015199636
else:
	angle = angleMC
	uncTargProjX = -0.0995461972579
	uncTargProjXSig = 0.217919555935
	uncTargProjY = -0.0668941015569
	uncTargProjYSig = 0.0831670646584
	uncY =  -0.0772321507928
	uncYSig = 0.0878428842895

zTarg = -4.3

xProj = "(uncVX-(uncVZ-{0})*uncPX/uncPZ)".format(zTarg)
yProj = "(uncVY-(uncVZ-{0})*uncPY/uncPZ)".format(zTarg)
xProj_rot = "{0}*cos({2})-{1}*sin({2})".format(xProj,yProj,-angle)
yProj_rot = "{0}*sin({2})+{1}*cos({2})".format(xProj,yProj,-angle)
nSig = 2

if(L1L2):
	m0 = -0.167438502208
	a0 = 0.016762652862
	a1 = 0.00033162637213
	b0 = 0.0207347770085
	b1 = 0.000331699098944

	eleisoL1 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
	posisoL1 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

	eleisoL2 = "eleMinPositiveIsoL2+1/3.*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
	posisoL2 = "posMinPositiveIsoL2+1/3.*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

	eleiso = "((eleHasL1&&{0})||(!eleHasL1&&{1}))".format(eleisoL1,eleisoL2)
	posiso = "((posHasL1&&{0})||(!posHasL1&&{1}))".format(posisoL1,posisoL2)

	uncTargProjXSig = 1.25 * uncTargProjXSig
	uncTargProjYSig = 1.5 * uncTargProjYSig

elif(L2L2):
	mpos = -0.576619997051
	mneg = -0.0126688170132
	m0 = -0.126973432435
	a0 = 0.0628788048688
	a1 = -0.00317833175061
	b0 = 0.0614724292851
	b1 = -0.00358273636968

	eleisoL2 = "eleMinPositiveIsoL2+1/3.*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
	posisoL2 = "posMinPositiveIsoL2+1/3.*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

	eleiso = eleisoL2
	posiso = posisoL2

	uncTargProjXSig = 1.9 * uncTargProjXSig
	uncTargProjYSig = 2.5 * uncTargProjYSig

else:
	m0 = -0.201776054859
	a0 = 0.0518988558564
	a1 = -0.00230111045957
	b0 = 0.0471576968062
	b1 = -0.00108639651791

	eleiso = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
	posiso = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

isocut = "({0}&&{1})".format(eleiso,posiso)

c0 = 0.0
c1 = 0.0
c2 = 0.0
c3 = 0.0

if(useData):
	c0 = -0.377
	c1 = 13.79
	c2 = -55.84
	c3 = 84.0

dy = uncTargProjY - (-0.0668941015569)
dz = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3".format(c0,c1,c2,c3)

if(L2L2):
	m0 = mpos

eleZ0_up = "(eleTrkZ0>{0}+{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,a0,a1,dz,dy)
posZ0_up = "(posTrkZ0>{0}+{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,a0,a1,dz,dy)

if(L2L2):
	m0 = mneg

eleZ0_down = "(-eleTrkZ0>{0}-{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,b0,b1,dz,dy)
posZ0_down = "(-posTrkZ0>{0}-{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,b0,b1,dz,dy)

z0cut = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up,posZ0_down,posZ0_up,eleZ0_down)

cuts = []
if(useZcut):
	if(L1L2):
		if(useData):
			#zcut = TF1("zcut","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-133,8211,-162000,1480000,-6406000,10560000),0.05,0.175) #L1L2 10%
			#cuts.append("(uncVZ>{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5)".format(-133,8211,-162000,1480000,-6406000,10560000))
			zcut = TF1("zcut","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-164.9,1.012e4,-2.087e5,2.039e6,-9.614e6,1.761e7),0.05,0.175) #L1L2 10%
			cuts.append("(uncVZ>{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5)".format(-164.9,1.012e4,-2.087e5,2.039e6,-9.614e6,1.761e7)) #100% Data L1L1
		else:
			#zcut = TF1("zcut","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(25.23,47.14,-2987,12370,0,0),0.05,0.175)
			#cuts.append("(uncVZ>{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5)".format(25.23,47.14,-2987,12370,0,0))
			zcut = TF1("zcut","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(74.12,-2922,7.02e4,-8.567e5,4.936e6,-1.075e7),0.05,0.175)
			cuts.append("(uncVZ>{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5)".format(74.12,-2922,7.02e4,-8.567e5,4.936e6,-1.075e7))
	if(L2L2):
		if(useData):
			#zcut = TF1("zcut","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-133,8211,-162000,1480000,-6406000,10560000),0.05,0.175) #L1L2 10%
			#cuts.append("(uncVZ>{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5)".format(-133,8211,-162000,1480000,-6406000,10560000))
			zcut = TF1("zcut","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-168.1,1.14e4,-2.278e5,2.051e6,-8.728e6,1.438e7),0.05,0.175) #L1L2 10%
			cuts.append("(uncVZ>{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5)".format(-168.1,1.14e4,-2.278e5,2.051e6,-8.728e6,1.438e7)) #100% Data L1L1
		else:
			#zcut = TF1("zcut","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(25.23,47.14,-2987,12370,0,0),0.05,0.175)
			#cuts.append("(uncVZ>{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5)".format(25.23,47.14,-2987,12370,0,0))
			zcut = TF1("zcut","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-816,5.006e4,-1.118e6,1.18e7,-5.97e7,1.169e8),0.05,0.175)
			cuts.append("(uncVZ>{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5)".format(-816,5.006e4,-1.118e6,1.18e7,-5.97e7,1.169e8))
	else:
		if(useData):
			#zcut = TF1("zcut","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-2.308,1227,-29030,285300,-1296000,2229000),0.05,0.175) #L1L1 10%
			#cuts.append("(uncVZ>{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5)".format(-2.308,1227,-29030,285300,-1296000,2229000))
			#zcut = TF1("zcut","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(9,53.04,-2566,-4258,2.345e5,-8.994e5),0.05,0.175) #L1L1 10%
			#cuts.append("(uncVZ>{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5)".format(9,53.04,-2566,-4258,2.345e5,-8.994e5))
			zcut = TF1("zcut","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-0.4738,1551,-3.835e4,3.930e5,-1.865e6,3.373e6),0.05,0.175) #100% Data L1L1
			cuts.append("(uncVZ>{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5)".format(-0.4738,1551,-3.835e4,3.930e5,-1.865e6,3.373e6))
		else:
			#zcut = TF1("zcut","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(22.23,48.63,-5150,49760,-169900,141700),0.05,0.175)
			#cuts.append("(uncVZ>{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5)".format(22.23,48.63,-5150,49760,-169900,141700))
			zcut = TF1("zcut","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(23.55,152.9,-9489,1.091e5,-5.19e5,9.013e5),0.05,0.175)
			cuts.append("(uncVZ>{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5)".format(23.55,152.9,-9489,1.091e5,-5.19e5,9.013e5))

cuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,nSig))
#cuts.append("uncChisq<4")
cuts.append("uncP>1.85")
cuts.append(isocut)
cuts.append(z0cut)
cuts.append("eleHasL2&&posHasL2")
cuts.append("uncM>0.06&&uncM<0.15")

cut = ""
for i in range(len(cuts)):
	if(i == 0):
		cut = cuts[i]
	else:
		cut = cut + "&&" + cuts[i]

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
	saveTuplePlot2D(events,x,y,nBins,minX,maxX,nBins,minY,maxY,outfile,c,"Mass (GeV)","Reconstructed z (mm)","Past zcut".format(label),cut=cut,stats=1,savePDF=savePDF)

for i in range(nBins):
	mass = minMass + i * (maxMass - minMass)/nBins
	if(cut == ""):
		masscut = "abs({0}-{1})<{2}/2*{3}".format("uncM",mass,masscut_nsigma,mres.Eval(mass))
	else:
		masscut = cut + "&&abs({0}-{1})<{2}/2*{3}".format("uncM",mass,masscut_nsigma,mres.Eval(mass))
	events.Draw("{0}>>histo({1},{2},{3})".format("uncVZ",nBins,-30,30),masscut)
	histo = ROOT.gROOT.FindObject("histo")
	nbk = histo.GetEntries()
	nBack.SetBinContent(i+1,nbk)
	nBack.SetBinError(i+1,math.sqrt(nbk))
	del histo

nBack.Draw()
nBack.SetTitle("Number of Background Events Overlapping Bins {0}".format(label))
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
	nbknew = getUnbiased(mass,mres.Eval(mass)/2*masscut_nsigma,nBack)
	#nbk = nBack.GetBinContent(i+1)
	nBackunbiased.SetBinContent(i+1,nbknew)
	#nBackunbiased.SetBinError(i+1,math.sqrt(nbk))

nBack.SetLineColor(1)
nBack.Draw()
nBack.SetTitle("Number of Background Events Overlapping Bins {0}".format(label))
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

massArr = []
mass = minMass
for i in range(nBins):
	massArr.append(mass)
	mass = mass + mres.Eval(mass)/2 * masscut_nsigma
	if(mass > maxMass):
		break

nBackNon = TH1F("nBackNon","nBackNon",len(massArr),massArr[0],massArr[len(massArr)-1])
for i in range(len(massArr)):
	mass = massArr[i]
	if(cut == ""):
		masscut = "abs({0}-{1})<{2}/2*{3}".format("uncM",mass,masscut_nsigma,mres.Eval(mass))
	else:
		masscut = cut + "&&abs({0}-{1})<{2}/2*{3}".format("uncM",mass,masscut_nsigma,mres.Eval(mass))
	events.Draw("{0}>>histo({1},{2},{3})".format("uncVZ",nBins,-30,30),masscut)
	histo = ROOT.gROOT.FindObject("histo")
	nbk = histo.GetEntries()
	nBackNon.SetBinContent(i+1,nbk)
	nBackNon.SetBinError(i+1,math.sqrt(nbk))
	del histo

nBackNon.Draw()
nBackNon.SetTitle("Number of Background Events {0}".format(label))
nBackNon.GetXaxis().SetTitle("Mass (GeV)")
nBackNon.SetStats(0)
nBackNon.Fit('pol2')
nBackNon.Write("Background")
c.Print(outfile+".pdf")

def getUnbiasedNon(mass,nbin,histoback):
    histoclone = histoback.Clone()
    histoclone.SetBinError(nbin,0)
    fit = TF1("fit","pol2")
    histoclone.Fit('fit')
    backnew = fit.Eval(mass)
    return backnew

nBackunbiasedNon = TH1F("nBackunbiasedNon","nBackunbiasedNon",len(massArr),massArr[0],massArr[len(massArr)-1])

for i in range(len(massArr)):
	nbknew = getUnbiasedNon(massArr[i],i+1,nBackNon)
	#nbk = nBack.GetBinContent(i+1)
	nBackunbiasedNon.SetBinContent(i+1,nbknew)
	#nBackunbiased.SetBinError(i+1,math.sqrt(nbk))

nBackNon.SetLineColor(1)
nBackNon.Draw()
nBackNon.SetTitle("Number of Background Events Overlapping Bins {0}".format(label))
nBackNon.GetXaxis().SetTitle("Mass (GeV)")
nBackNon.SetStats(0)
nBackunbiasedNon.SetLineColor(4)
nBackunbiasedNon.Draw("same")
nBackunbiasedNon.SetStats(0)
nBackunbiasedNon.Write("Background Unbiased")
legend.Draw("same")
c.Print(outfile+".pdf")

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

if(useData):
	textFile.write('$\Delta z_{cut}$ & VZ (mm) & Mass (MeV) & Run & Event & $chi^2_{unc}$ & V0 Proj Y ($n_{\sigma}$) & VY ($n_{\sigma}$) & $\Delta \ e^- \ z0$ (mm) & $\Delta \ e^+ \ z0$ (mm)\n')
	for entry in xrange(neventscut):
		#if(dzcut < 0):
		#	continue
		cutevents.GetEntry(entry)
		dzcut = cutevents.uncVZ - zcut.Eval(cutevents.uncM)

		xProj = (cutevents.uncVX-(cutevents.uncVZ-zTarg)*cutevents.uncPX/cutevents.uncPZ)
		yProj = (cutevents.uncVY-(cutevents.uncVZ-zTarg)*cutevents.uncPY/cutevents.uncPZ)
		yProj_rot = xProj*math.sin(angle)+yProj*math.cos(angle)

		projY = abs(yProj_rot - uncTargProjY) / uncTargProjYSig
		VY = abs(cutevents.uncVY - uncY) / uncYSig

		#textFile.write('{0} {1} \n'.format(cutevents.run,cutevents.event))

		if(cutevents.elePY > 0):
			eleZ0 = cutevents.eleTrkZ0-(m0+a0*cutevents.uncVZ+a1*1/cutevents.uncM*cutevents.uncVZ)
			posZ0 = -cutevents.posTrkZ0-(m0+b0*cutevents.uncVZ+b1*1/cutevents.uncM*cutevents.uncVZ)
			textFile.write('{9:0.2f} & {0:0.2f} & {1:0.2f} & {2:0.0f} & {3:0.0f} & {4:0.2f} & {5:0.2f} & {6:0.2f} & {7:0.2f} & {8:0.2f} \\ \n'.format(cutevents.uncVZ,
				cutevents.uncM*1000,cutevents.run,cutevents.event,cutevents.uncChisq,projY,VY,-eleZ0,-posZ0,dzcut))
		else:
			eleZ0 = -cutevents.eleTrkZ0-(m0+b0*cutevents.uncVZ+b1*1/cutevents.uncM*cutevents.uncVZ)
			posZ0 = cutevents.posTrkZ0-(m0+a0*cutevents.uncVZ+a1*1/cutevents.uncM*cutevents.uncVZ)
			textFile.write('{9:0.2f} & {0:0.2f} & {1:0.2f} & {2:0.0f} & {3:0.0f} & {4:0.2f} & {5:0.2f} & {6:0.2f} & {7:0.2f} & {8:0.2f} \\ \n'.format(cutevents.uncVZ,
				cutevents.uncM*1000,cutevents.run,cutevents.event,cutevents.uncChisq,projY,VY,-eleZ0,-posZ0,dzcut))

	textFile.close()
	if(savePDF):
		closePDF(outfile,c)
	rootfile.Close()
	sys.exit(0)

textFile.write('$\Delta z_{cut}$ & VZ (mm) & Mass (MeV) & $theta_{1}$ (mrad) & $theta_{2}$ (mrad) & $chi^2_{unc}$ & V0 Proj Y ($n_{\sigma}$) & VY ($n_{\sigma}$) & $\Delta \ e^- \ z0$ (mm) & $\Delta \ e^+ \ z0$ (mm)\n')

scatter = TH2F("scatter","scatter",100,0,maxTheta/2,100,0,maxTheta/2)
scatterL1 = TH2F("scatterL1","scatterL1",100,0,maxTheta/2,100,0,maxTheta/2)
scatterL2 = TH2F("scatterL2","scatterL2",100,0,maxTheta/2,100,0,maxTheta/2)
scattermax = TH2F("scattermax","scattermax",100,0,maxTheta/2,100,0,maxTheta/2)

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

for entry in xrange(neventscut):
	#if(dzcut < 0):
	#	continue
	cutevents.GetEntry(entry)
	dzcut = cutevents.uncVZ - zcut.Eval(cutevents.uncM)
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
	yProj_rot = xProj*math.sin(-angle)+yProj*math.cos(-angle)

	projY = abs(yProj_rot - uncTargProjY) / uncTargProjYSig
	VY = abs(cutevents.uncVY - uncY) / uncYSig

	if(eleL1t == -9999):
		eleL1t = 0

	if(eleL2t == -9999):
		eleL2t = 0

	if(eleL1b == -9999):
		eleL1b = 0

	if(eleL2b == -9999):
		eleL2b = 0

	if(posL1t == -9999):
		posL1t = 0

	if(posL2t == -9999):
		posL2t = 0

	if(posL1b == -9999):
		posL1b = 0

	if(posL2b == -9999):
		posL2b = 0

	if(cutevents.elePY > 0):
		eleZ0 = cutevents.eleTrkZ0-(m0+a0*cutevents.uncVZ+a1*1/cutevents.uncM*cutevents.uncVZ)
		posZ0 = -cutevents.posTrkZ0-(m0+b0*cutevents.uncVZ+b1*1/cutevents.uncM*cutevents.uncVZ)
		textFile.write('{9:0.2f} & {0:0.2f} & {1:0.2f} & {2:0.2f} & {3:0.2f} & {4:0.2f} & {5:0.2f} & {6:0.2f} & {7:0.2f} & {8:0.2f} \\ \n'.format(cutevents.uncVZ,
			cutevents.uncM*1000,max(-eleL1t,-eleL2t)*1000,max(posL1b,posL2b)*1000,cutevents.uncChisq,projY,VY,-eleZ0,-posZ0,dzcut))
	else:
		eleZ0 = -cutevents.eleTrkZ0-(m0+b0*cutevents.uncVZ+b1*1/cutevents.uncM*cutevents.uncVZ)
		posZ0 = cutevents.posTrkZ0-(m0+a0*cutevents.uncVZ+a1*1/cutevents.uncM*cutevents.uncVZ)
		textFile.write('{9:0.2f} & {0:0.2f} & {1:0.2f} & {2:0.2f} & {3:0.2f} & {4:0.2f} & {5:0.2f} & {6:0.2f} & {7:0.2f} & {8:0.2f} \\ \n'.format(cutevents.uncVZ,
			cutevents.uncM*1000,max(-posL1t,-posL2t)*1000,max(eleL1b,eleL2b)*1000,cutevents.uncChisq,projY,VY,-eleZ0,-posZ0,dzcut))

savehisto2D(scatter,outfile,c,"#theta_{bot}","#theta_{top}","Top Scatter vs Bottom Scatter Sensor1 + Sensor2 {0}".format(label),0,savePDF=savePDF)
savehisto2D(scatterL1,outfile,c,"#theta_{bot}","#theta_{top}","Top Scatter vs Bottom Scatter Sensor1 {0}".format(label),0,savePDF=savePDF)
savehisto2D(scatterL2,outfile,c,"#theta_{bot}","#theta_{top}","Top Scatter vs Bottom Scatter Sensor2 {0}".format(label),0,savePDF=savePDF)
savehisto2D(scattermax,outfile,c,"#theta_{bot}","#theta_{top}","Top Scatter vs Bottom Scatter Max(Sensor1,Sensor2) {0}".format(label),0,savePDF=savePDF)

textFile.close()
if(savePDF):
    closePDF(outfile,c)
rootfile.Close()
