import sys
tmpargv = sys.argv
sys.argv = []
import getopt
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
    print '\t-g: minimum uncVZ (default 0 mm)'
    print '\t-i: maximum uncVZ (default 60 mm)'
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
minVZ = 0
maxVZ = 60
nBins = 30
useData = False
L1L2 = False
clusterT = 56
uncTargProjX = 0.
uncTargProjXSig = 9999.
uncTargProjY = 0.
uncTargProjYSig = 9999.
label = ""

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:g:i:e:q:t:o:p:a:b:y:rd')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-g':
			minVZ = float(arg)
		if opt=='-i':
			maxVZ = float(arg)
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

def SmearZ0(eventscut,nBins,minX,maxX):
	mean = -0.01
	z0smear = 0.05
	m0 = -0.201776054859
	a0 = 0.0518988558564
	a1 = -0.00230111045957
	b0 = 0.0471576968062
	b1 = -0.00108639651791
	histo3 = TH1F("histo3","histo3",nBins,minX,maxX)

	uncM = array.array('d',[0])
	uncVZ = array.array('d',[0])
	eleTrkZ0 = array.array('d',[0])
	posTrkZ0 = array.array('d',[0])

	eventscut.Branch("uncM",uncM,"uncM/D")
	eventscut.Branch("uncVZ",uncVZ,"uncVZ/D")
	eventscut.Branch("eleTrkZ0",eleTrkZ0,"eleTrkZ0/D")
	eventscut.Branch("posTrkZ0",posTrkZ0,"posTrkZ0/D")

	nevents = eventscut.GetEntries()

	for entry in xrange(nevents):
		eventscut.GetEntry(entry)

		eleZ0 = random.gauss(eventscut.eleTrkZ0-mean, z0smear)
		posZ0 = random.gauss(eventscut.posTrkZ0-mean, z0smear)

		eleZ0cut1 = eleZ0 > m0 + a0 * eventscut.uncVZ + a1 *1/eventscut.uncM * eventscut.uncVZ
		eleZ0cut2 = -eleZ0 > m0 + b0 * eventscut.uncVZ + b1 *1/eventscut.uncM * eventscut.uncVZ

		posZ0cut1 = posZ0 > m0 + a0 * eventscut.uncVZ + a1 *1/eventscut.uncM * eventscut.uncVZ
		posZ0cut2 = -posZ0 > m0 + b0 * eventscut.uncVZ + b1 *1/eventscut.uncM * eventscut.uncVZ

		if((eleZ0cut1 and posZ0cut2) or (eleZ0cut2 and posZ0cut1)):
			histo3.Fill(eventscut.uncVZ)

	return histo3

def makePlots(events,z0_cut,cut_tot,nBins,minX,maxX,label,outfile,canvas,XaxisTitle="",YaxisTitle="",stats=0,logY=0):
	RatioMin = 0.9
	RatioMax = 1.1

	cut = "{0}&&{1}".format(cut_tot,z0_cut)
	events.Draw("{0}>>{1}({2},{3},{4})".format("uncVZ","histo",nBins,minX,maxX),cut)
	histo = ROOT.gROOT.FindObject("histo")
	histo.Sumw2()

	eventscut = events.CopyTree(cut_tot)

	histo2 = SmearZ0(eventscut,nBins,minX,maxX)
	histo2.Sumw2()

	canvas.Clear()
	canvas.SetLogy(logY)

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

	histo.SetTitle(label)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)

	histo.Draw()
	histo2.SetLineColor(2)
	histo2.Draw("same")

	legend = TLegend(.60,.66,.82,.90)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histo,"No Smearing","LP")
	legend.AddEntry(histo2,"With Smearing","LP")
	legend.Draw("")

	bot.cd()
	reference = histo.Clone("reference")
	reference.GetYaxis().SetTitle("Ratio")
	reference.GetYaxis().SetTitleSize(0.06)
	reference.GetYaxis().SetLabelSize(0.1)
	reference.GetXaxis().SetTitleSize(0.1)
	reference.GetXaxis().SetLabelSize(0.1)
	reference.GetXaxis().SetTitle(XaxisTitle)
	reference.GetYaxis().SetRangeUser(RatioMin,RatioMax)
	reference.GetYaxis().SetNdivisions(508)
	reference.GetYaxis().SetDecimals(True)
	reference.Draw("axis")
	ratio = histo2.Clone("Ratio"+histo2.GetName())
	ratio.Divide(reference)
	ratio.DrawCopy("pe same")
	ratio.SetStats(1)
	ratio.Fit("pol0")

	canvas.Print(outfile+".pdf")
	canvas.Write()

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

file = TFile(remainder[1])
events = file.Get("ntuple")

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

cuts = []

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

cuts.append("eleHasL1&&posHasL1&&eleHasL2&&posHasL2")
cuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,nSig))
cuts.append("uncP>2.0")
cuts.append(isocut)

cut_all = ""

for i in range(len(cuts)):
	cut = cuts[i]
	if(i == 0):
		cut_all = cut
	else:
		cut_all = cut_all + "&&" + cut

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

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

openPDF(outfile,c)

makePlots(events,z0cut,cut_all,nBins,minVZ,maxVZ,label,outfile,c,XaxisTitle="reconstructed z (mm)",YaxisTitle="")

closePDF(outfile,c)
outfileroot.Close()
