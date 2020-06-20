import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import numpy as np
import array
import random
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TLatex, TPad
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input root file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-z: target position (default -4.3 mm)'
    print '\t-e: beam energy (default 2.3 GeV)'
    print '\t-q: number of bins (default 140)'
    print '\t-t: cluster time offset (default 56 ns)'
    print '\t-o: uncTargProjX mean (default 0)'
    print '\t-p: uncTargProjX sigma (default 9999)'
    print '\t-a: uncTargProjY mean (default 0)'
    print '\t-b: uncTargProjY sigma (default 9999)'
    print '\t-r: is L1L2 category (default false)'
    print '\t-y: plot label'
    print '\t-d: use data file (default False)'
    print '\t-h: this help message'
    print

zTarg = -4.3
ebeam = 2.3
nBins = 100
useData = False
L1L2 = False
clusterT = 56
uncTargProjX = 0.
uncTargProjXSig = 9999.
uncTargProjY = 0.
uncTargProjYSig = 9999.
label = ""

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:e:q:t:o:p:a:b:y:rd')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-e':
			ebeam = float(arg)
		if opt=='-q':
			nBins = float(arg)
		if opt=='-t':
			clusterT = float(arg)
		if opt=='-o':
			uncTargProjX=float(arg)
		if opt=='-p':
			uncTargProjXSig=float(arg)
		if opt=='-a':
			uncTargProjY=float(arg)
		if opt=='-b':
			uncTargProjYSig=float(arg)
		if opt=='-y':
			label=str(arg)
		if opt=='-r':
			L1L2 = True
		if opt=='-d':
			useData = True
		if opt=='-h':
			print_usage()
			sys.exit(0)

def getEffTH1(hfile, hname):
    print 'Getting Efficiency Graph...converting to TH1'
    effGraph=hfile.Get(hname)
    effGraph.Print("v")
    xmin=effGraph.GetXaxis().GetXmin()
    xmax=effGraph.GetXaxis().GetXmax()
    xsize=effGraph.GetErrorXhigh(0)*2
    nbins=effGraph.GetN()
    nbinsHist=(int)((xmax-xmin)/xsize)
    x=ROOT.Double(0.0)
    y=ROOT.Double(0.0)
    effHist=ROOT.TH1D(effGraph.GetName(),effGraph.GetTitle(),nbinsHist,xmin,xmax)
    for i in range(0,nbins) :
        effGraph.GetPoint(i,x,y)
        histBin=effHist.FindBin(x)
        #print str(x)+' ' +str(y) + ' '+str(i)+ '  '+str(histBin)
        effHist.SetBinContent(histBin,y)   
    return effHist

effSlopeFileName = 'EmGamma-L1HitEfficiencyResults-2016.root'
effRatioName = 'p2slopehps_007963.1GamEm_L1HitInefficiency'
effSlopeFile = ROOT.TFile(effSlopeFileName)      
effSlopeData = getEffTH1(effSlopeFile,effRatioName)
effSlopeData.Print("v")

def RemoveHit(slp):
    rndm = random.random()         
    ibin = effSlopeData.FindBin(slp)
    eff = 1 - 3*effSlopeData.GetBinContent(ibin) #the slope "efficiency" is actually an inefficiency
    if rndm > eff:
        return True
    else:
        return False

def makePlots(e,cut,nBins,label,outfile,canvas,XaxisTitle="",YaxisTitle="",stats=0,logY=0):
	events = e.CopyTree(cut)
	eventskill = events.CloneTree(0)

	eleisocut = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
	posisocut = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

	isocut = "({0}&&{1})".format(eleisocut,posisocut)

	eleTrkLambda = array.array('d',[0])
	posTrkLambda = array.array('d',[0])
	eleTrkZ0 = array.array('d',[0])
	posTrkZ0 = array.array('d',[0])
	elePY = array.array('d',[0])
	posPY = array.array('d',[0])
	eleP = array.array('d',[0])
	posP = array.array('d',[0])
	eleTrkZ0Err = array.array('d',[0])
	posTrkZ0Err = array.array('d',[0])
	eleTrkLambdaErr = array.array('d',[0])
	posTrkLambdaErr = array.array('d',[0])
	eleTrkOmega = array.array('d',[0])
	posTrkOmega = array.array('d',[0])
	eleTrkOmegaErr = array.array('d',[0])
	posTrkOmegaErr = array.array('d',[0])
	eleMinPositiveIso = array.array('d',[0])
	posMinPositiveIso = array.array('d',[0])

	events.Branch("eleTrkLambda",eleTrkLambda,"eleTrkLambda/D")
	events.Branch("posTrkLambda",posTrkLambda,"posTrkLambda/D")
	events.Branch("eleTrkZ0",eleTrkZ0,"eleTrkZ0/D")
	events.Branch("posTrkZ0",posTrkZ0,"posTrkZ0/D")
	events.Branch("elePY",elePY,"elePY/D")
	events.Branch("posPY",posPY,"posPY/D")
	events.Branch("eleP",eleP,"eleP/D")
	events.Branch("posP",posP,"posP/D")
	events.Branch("eleTrkZ0Err",eleTrkZ0Err,"eleTrkZ0Err/D")
	events.Branch("posTrkZ0Err",posTrkZ0Err,"posTrkZ0Err/D")
	events.Branch("eleTrkLambdaErr",eleTrkLambdaErr,"eleTrkLambdaErr/D")
	events.Branch("posTrkLambdaErr",posTrkLambdaErr,"posTrkLambdaErr/D")
	events.Branch("eleTrkOmega",eleTrkOmega,"eleTrkOmega/D")
	events.Branch("posTrkOmega",posTrkOmega,"posTrkOmega/D")
	events.Branch("eleTrkOmegaErr",eleTrkOmegaErr,"eleTrkOmegaErr/D")
	events.Branch("posTrkOmegaErr",posTrkOmegaErr,"posTrkOmegaErr/D")
	events.Branch("eleMinPositiveIso",eleMinPositiveIso,"eleMinPositiveIso/D")
	events.Branch("posMinPositiveIso",posMinPositiveIso,"posMinPositiveIso/D")

	nevents = events.GetEntries()

	for entry in xrange(nevents):
		events.GetEntry(entry)
		eleiso = events.eleMinPositiveIso+0.5*((events.eleTrkZ0+zTarg*events.elePY/events.eleP)*np.sign(events.elePY)-3*(events.eleTrkZ0Err+abs(zTarg*events.eleTrkLambdaErr)+abs(2*zTarg*events.eleTrkLambda*events.eleTrkOmegaErr/events.eleTrkOmega)))
		posiso = events.posMinPositiveIso+0.5*((events.posTrkZ0+zTarg*events.posPY/events.posP)*np.sign(events.posPY)-3*(events.posTrkZ0Err+abs(zTarg*events.posTrkLambdaErr)+abs(2*zTarg*events.posTrkLambda*events.posTrkOmegaErr/events.posTrkOmega)))

		removehitEle = RemoveHit(events.eleTrkLambda)
		removehitPos = RemoveHit(events.posTrkLambda)
		if(eleiso > 0 and posiso > 0):
			eventskill.Fill()
		elif((eleiso < 0 and not removehitEle) or (posiso < 0 and not removehitPos)):
			continue
		else:
			eventskill.Fill()
	outfileroot.cd()
	eventskill.Draw("{0}:uncM>>{1}({2},{3},{4},{5},{6},{7})".format("uncVZ","histo",nBins,0,0.2,nBins,-30,30))
	histo = ROOT.gROOT.FindObject("histo")

	histo.GetXaxis().SetTitle("Reconstructed e+e- Mass (GeV)")
	histo.GetYaxis().SetTitle("Reconstructed z (mm)")
	histo.SetTitle("tritrig-wab-beam L1L1 Hit Killing {0}".format(label))
	histo.Draw("COLZ")

	#canvas.Print(outfile+".pdf")
	#canvas.Write()
	histo.Write("tritrig-wab-beam L1L1 Hit Killing {0}".format(label))

	events.Draw("{0}:uncM>>{1}({2},{3},{4},{5},{6},{7})".format("uncVZ","histo2",nBins,0,0.2,nBins,-30,30),isocut)
	histo2 = ROOT.gROOT.FindObject("histo2")

	histo2.GetXaxis().SetTitle("Reconstructed e+e- Mass (GeV)")
	histo2.GetYaxis().SetTitle("Reconstructed z (mm)")
	histo2.SetTitle("tritrig-wab-beam L1L1 {0}".format(label))
	histo2.Draw("COLZ")

	#canvas.Print(outfile+".pdf")
	#canvas.Write()
	histo2.Write("tritrig-wab-beam L1L1 {0}".format(label))

	eventskill.Draw("{0}>>{1}({2},{3},{4})".format("uncVZ","histo3",nBins,-30,30))
	histo3 = ROOT.gROOT.FindObject("histo3")
	events.Draw("{0}>>{1}({2},{3},{4})".format("uncVZ","histo4",nBins,-30,30),isocut)
	histo4 = ROOT.gROOT.FindObject("histo4")
	histo3.Sumw2()
	histo4.Sumw2()
	histo3.Write("tritrig-wab-beam L1L1 Hit Killing 1D {0}".format(label))
	histo4.Write("tritrig-wab-beam L1L1 1D {0}".format(label))

	canvas.Clear()
	canvas.SetLogy(1)

	RatioMin = 0.7
	RatioMax = 1.3

	top = TPad("top","top",0,0.42,1,1)
	top.SetLogy(logY)
    
	bot = TPad("bot","bot",0,0,1,0.40)
    
	top.Draw()
	top.SetBottomMargin(0)
	#top.SetTopMargin(gStyle.GetPadTopMargin()*topScale)
	bot.Draw()
	bot.SetTopMargin(0)
	bot.SetBottomMargin(0.4)
	top.cd()

	histo3.GetXaxis().SetTitle("Reconstructed z (mm)")
	histo3.SetTitle("tritrig-wab-beam L1L1 {0}".format(label))
	histo3.Draw("")
	histo3.SetStats(0)

	histo4.GetXaxis().SetTitle("Reconstructed z (mm)")
	histo4.SetTitle("tritrig-wab-beam L1L1 {0}".format(label))
	histo4.SetLineColor(2)
	histo4.Draw("same")
	histo4.SetStats(0)

	legend = TLegend(.75,.65,.97,.90)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histo3,"With Hit Killing","LP")
	legend.AddEntry(histo4,"No Hit Killing","LP")
	legend.Draw("")

	bot.cd()
	reference = histo4.Clone("reference")
	reference.GetYaxis().SetTitle("Ratio")
	reference.GetYaxis().SetTitleSize(0.06)
	reference.GetYaxis().SetLabelSize(0.1)
	reference.GetXaxis().SetTitleSize(0.1)
	reference.GetXaxis().SetLabelSize(0.1)
	reference.GetXaxis().SetTitle("Reconstructed z (mm)")
	reference.GetYaxis().SetRangeUser(RatioMin,RatioMax)
	reference.GetYaxis().SetNdivisions(508)
	reference.GetYaxis().SetDecimals(True)
	reference.Draw("axis")
	ratio = histo3.Clone("Ratio"+histo3.GetName())
	ratio.Divide(reference)
	ratio.DrawCopy("pe same")

	#canvas.Print(outfile+".pdf")
	#canvas.Write()

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

#file = TFile(remainder[1])
#e = file.Get("ntuple")

e = TChain("ntuple")
for i in remainder[1:]:
	e.Add(i,0)

uncTargProjX = -0.0995461972579 
uncTargProjXSig = 0.217919555935 
uncTargProjY = -0.0668941015569 
uncTargProjYSig = 0.0831670646584
angleMC = 0.111025680707
angleData = 0.0386557750132
if(useData):
	angle = angleData
else:
	angle = angleMC
xProj = "(uncVX-(uncVZ-{0})*uncPX/uncPZ)".format(zTarg)
yProj = "(uncVY-(uncVZ-{0})*uncPY/uncPZ)".format(zTarg)
xProj_rot = "{0}*cos({2})-{1}*sin({2})".format(xProj,yProj,-angle)
yProj_rot = "{0}*sin({2})+{1}*cos({2})".format(xProj,yProj,-angle)
nSig = 2

c0 = 0.0
c1 = 0.0
c2 = 0.0
c3 = 0.0

if(useData):
	c0 = -0.377
	c1 = 13.79
	c2 = -55.84
	c3 = 84.0

dz = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3".format(c0,c1,c2,c3)

eleiso = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
posiso = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

isocut = "({0}&&{1})".format(eleiso,posiso)

m0 = -0.201776054859
a0 = 0.0518988558564
a1 = -0.00230111045957
b0 = 0.0471576968062
b1 = -0.00108639651791

eleZ0_up = "(eleTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0+0.00,a0,a1,dz)
posZ0_up = "(posTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0+0.00,a0,a1,dz)
eleZ0_down = "(-eleTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0+0.00,b0,b1,dz)
posZ0_down = "(-posTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0+0.00,b0,b1,dz)

z0cut = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up,posZ0_down,posZ0_up,eleZ0_down)

cuts = []
cuts.append("eleHasL1&&posHasL1&&eleHasL2&&posHasL2")
cuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,nSig))
cuts.append("uncP>1.85")
#cuts.append(isocut)
cuts.append(z0cut)
cuts.append("eleNHitsShared<0.5&&posNHitsShared<0.5")

outfile = remainder[0]
outfileroot2 = TFile(remainder[0]+"_tuple.root","RECREATE")
outfileroot = TFile(remainder[0]+".root","RECREATE")

cuttot = "{0}&&{1}&&{2}&&{3}&&{4}".format(cuts[0],cuts[1],cuts[2],cuts[3],cuts[4])

#openPDF(outfile,c)

outfileroot2.cd()
makePlots(e,cuttot,nBins,label,outfile,c)

#closePDF(outfile,c)
outfileroot.Close()
