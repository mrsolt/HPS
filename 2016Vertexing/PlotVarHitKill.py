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
nBins = 30
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
    eff = 1 - effSlopeData.GetBinContent(ibin) #the slope "efficiency" is actually an inefficiency
    if rndm > eff:
        return True
    else:
        return False

def makePlots(events,var,cut,nBins,minX,maxX,label,outfile,canvas,XaxisTitle="",YaxisTitle="",stats=0,logY=0):
	RatioMin = 0.5
	RatioMax = 1.0

	events.Draw("{0}>>{1}({2},{3},{4})".format(var,"histo",nBins,minX,maxX),cut)
	histo = ROOT.gROOT.FindObject("histo")
	histo.Sumw2()

	eventskill = events.CloneTree(0)
	eventskill.SetName("ntuple_kill")

	eleTrkLambda = array.array('d',[0])
	posTrkLambda = array.array('d',[0])

	events.Branch("eleTrkLambda",eleTrkLambda,"eleTrkLambda/D")
	events.Branch("posTrkLambda",posTrkLambda,"posTrkLambda/D")

	nevents = events.GetEntries()

	for entry in xrange(nevents):
		events.GetEntry(entry)
		removehitEle = RemoveHit(events.eleTrkLambda)
		removehitPos = RemoveHit(events.posTrkLambda)
		if(removehitEle or removehitPos):
			continue
		else:
			eventskill.Fill()

	eventskill.Draw("{0}>>{1}({2},{3},{4})".format(var,"histo2",nBins,minX,maxX),cut)
	histo2 = ROOT.gROOT.FindObject("histo2")
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

	legend = TLegend(.75,.65,.97,.90)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histo,"No Hit Killing","LP")
	legend.AddEntry(histo2,"With Hit Killing","LP")
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
cuts.append("uncP>2.0")
cuts.append(isocut)
cuts.append(z0cut)

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

variables = []
variables.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,nSig))
variables.append("uncP")
variables.append("eleTrkZ0")
variables.append("posTrkZ0")

cuttot = []
cuttot.append("{0}&&{1}&&{2}&&{3}".format(cuts[0],cuts[2],cuts[3],cuts[4]))
cuttot.append("{0}&&{1}&&{2}&&{3}".format(cuts[0],cuts[1],cuts[3],cuts[4]))
cuttot.append("{0}&&{1}&&{2}&&{3}".format(cuts[0],cuts[1],cuts[2],cuts[3]))
cuttot.append("{0}&&{1}&&{2}&&{3}".format(cuts[0],cuts[1],cuts[2],cuts[3]))

xaxis = []
xaxis.append("V0 Projection to Target N#sigma")
xaxis.append("V0 Momentum (GeV)")
xaxis.append("Electron Track Z0 (mm)")
xaxis.append("Positron Track Z0 (mm)")

minvar = []
minvar.append(0)
minvar.append(1.0)
minvar.append(-0.5)
minvar.append(-0.5)

maxvar = []
maxvar.append(3)
maxvar.append(2.6)
maxvar.append(0.5)
maxvar.append(0.5)

openPDF(outfile,c)

for i in range(len(variables)):
	makePlots(events,variables[i],cuttot[i],nBins,minvar[i],maxvar[i],label,outfile,c,XaxisTitle=xaxis[i],YaxisTitle="")

closePDF(outfile,c)
outfileroot.Close()
