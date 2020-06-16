#!/usr/bin/env python
#Author Matt Solt mrsolt@slac.stanford.edu
import sys
import array, math
import numpy as np
import random
import root_numpy, numpy
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, TH1F, TLegend, TLatex, TGraphErrors, TPad
import getopt

def print_usage():
    print "\nUsage: {0} <output file basename> <input A' file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-e: use this beam energy <default 2.3 GeV>'
    print '\t-t: use this target position <default -4.3 mm>'
    print '\t-n: number of bins in histograms <default 50>'
    print '\t-z: total range in z covered <default 100 mm>'
    print '\t-s: tuple name <default is "ntuple">'
    print '\t-c: cut tracks with shared hits <default is false>'
    print '\t-h: this help message'
    print

#Default Values
eBeam = 2.3
killInTrackSlope = True
targZ = -4.3
nBins = 50
zRange = 100
removeSharedHits = False
tupleName = "ntuple"

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

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:t:n:z:cs:h')

# Parse the command line arguments
for opt, arg in options:
    if opt=='-e':
        eBeam=float(arg)
    if opt=='-t':
        targZ=float(arg)
    if opt=='-n':
        nBins=int(arg)
    if opt=='-z':
        zRange=float(arg)
    if opt=='-c':
        removeSharedHits = True
    if opt=='-s':
        tupleName = str(arg)
    if opt=='-h':
        print_usage()
        sys.exit(0)

if killInTrackSlope:
    #effSlopeFileName = '/home/mrsolt/hps/test/EmGamma-L1HitEfficiencyResults-2016.root'
    effSlopeFileName = 'EmGamma-L1HitEfficiencyResults-2016.root'
    effRatioName = 'p2slopehps_007963.1GamEm_L1HitInefficiency'
    effSlopeFile = ROOT.TFile(effSlopeFileName)      
    effSlopeData = getEffTH1(effSlopeFile,effRatioName)

def RemoveHit(slp):
    rndm = random.random()         
    ibin = effSlopeData.FindBin(slp)
    eff = 1 - effSlopeData.GetBinContent(ibin) #the slope "efficiency" is actually an inefficiency
    if rndm > eff:
        return True
    else:
        return False

def correctSlope(z,slp):
    d = 100
    return (1 - z/d) * slp

def NewEventsL1L1(events,outfile):
    eleTrkLambda = array.array('d',[0])
    posTrkLambda = array.array('d',[0])
    uncVZ = array.array('d',[0])

    file = TFile("dum_{0}.root".format(outfile),"recreate")
    events1 = events.CloneTree(0)
    events2 = events.CloneTree(0)

    events1.SetName("ntuple_new")
    events2.SetName("ntuple_corr")

    events.Branch("eleTrkLambda",eleTrkLambda,"eleTrkLambda/D")
    events.Branch("posTrkLambda",posTrkLambda,"posTrkLambda/D")
    events.Branch("uncVZ",uncVZ,"uncVZ/D")

    nevents = events.GetEntries()

    for entry in xrange(nevents):
        events.GetEntry(entry)
        removehitEle = RemoveHit(events.eleTrkLambda)
        removehitPos = RemoveHit(events.posTrkLambda)
        eleTrkLambdaCorr = correctSlope(events.uncVZ,events.eleTrkLambda)
        posTrkLambdaCorr = correctSlope(events.uncVZ,events.posTrkLambda)
        removehitEleCorr = RemoveHit(eleTrkLambdaCorr)
        removehitPosCorr = RemoveHit(posTrkLambdaCorr)
        if(not removehitEle and not removehitPos):
            events1.Fill()
        if(not removehitEleCorr and not removehitPosCorr):
            events2.Fill()

    events1.AutoSave()
    events2.AutoSave()
    #return events1, events2
    return

def openPDF(outfile,canvas):
    canvas.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
    canvas.Print(outfile+".pdf]")

gROOT.SetBatch(True)
c = TCanvas("c","c",1200,900)
maxZ = targZ + zRange #Define Maximum Z

#Set outfile and grab infile
outfile = remainder[0]
outfileroot = TFile(remainder[0]+"_all.root","RECREATE")
infile = TFile(remainder[1])
events = infile.Get("ntuple")

#Grab values of mass from the truth in the tuple files
events.Draw("triM>>histoMass({0},{1},{2})".format(1000,0,1))
histoMass = ROOT.gROOT.FindObject("histoMass")
mass = histoMass.GetMean()
del histoMass

#Function to fit for normalization
exppol4=TF1("exppol4","exp(pol4(0))",-5,100)

angleMC = 0.111025680707
angleData = 0.0386557750132
angle = angleMC
xProj = "(uncVX-(uncVZ-{0})*uncPX/uncPZ)".format(targZ)
yProj = "(uncVY-(uncVZ-{0})*uncPY/uncPZ)".format(targZ)
xProj_rot = "({0}*cos({2})-{1}*sin({2}))".format(xProj,yProj,-angle)
yProj_rot = "({0}*sin({2})+{1}*cos({2}))".format(xProj,yProj,-angle)

uncTargProjX = -0.0995461972579 
uncTargProjXSig = 0.217919555935 
uncTargProjY = -0.0668941015569 
uncTargProjYSig = 0.0831670646584
nSig = 2

eleiso = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(targZ)
posiso = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(targZ)

isocut = "({0}&&{1})".format(eleiso,posiso)

m0 = -0.201776054859
a0 = 0.0518988558564
a1 = -0.00230111045957
b0 = 0.0471576968062
b1 = -0.00108639651791
dz = 0.

eleZ0_up = "(eleTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,a0,a1,dz)
posZ0_up = "(posTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,a0,a1,dz)
eleZ0_down = "(-eleTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,b0,b1,dz)
posZ0_down = "(-posTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,b0,b1,dz)

z0cut = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up,posZ0_down,posZ0_up,eleZ0_down)

cutsL1L1 = []
cutsL1L1.append("eleHasL1&&posHasL1")
cutsL1L1.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,nSig))
cutsL1L1.append(isocut)
cutsL1L1.append(z0cut)
if(removeSharedHits):
    cutsL1L1.append("eleNHitsShared<0.5&&posNHitsShared<0.5")

zcutL1L1 = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(-0.4738,1551,-3.835e4,3.930e5,-1.865e6,3.373e6) #100% Data L1L1
cutsL1L1.append("uncVZ>{0}".format(zcutL1L1))

cutL1L1 = cutsL1L1[0]
for i in range(1,len(cutsL1L1)):
    cutL1L1 = cutL1L1 + "&&" + cutsL1L1[i]

NewEventsL1L1(events,outfile)

newfile = TFile("dum_{0}.root".format(outfile))
eventsnew = newfile.Get("ntuple_new")
eventscorr = newfile.Get("ntuple_corr")

eventsnew.Draw("triEndZ>>histo({0},{1},{2})".format(nBins,targZ,maxZ))
histo = ROOT.gROOT.FindObject("histo")

eventscorr.Draw("triEndZ>>histocorr({0},{1},{2})".format(nBins,targZ,maxZ))
histocorr = ROOT.gROOT.FindObject("histocorr")

outfileroot.cd()

histo.Sumw2()
histocorr.Sumw2()

outfileroot.cd()

c.Clear()

RatioMin = 0.7
RatioMax = 1.1

top = TPad("top","top",0,0.42,1,1)
top.SetLogy(0)
   
bot = TPad("bot","bot",0,0,1,0.38)
    
top.Draw()
top.SetBottomMargin(0)
#top.SetTopMargin(gStyle.GetPadTopMargin()*topScale)
bot.Draw()
bot.SetTopMargin(0)
bot.SetBottomMargin(0.4)
top.cd()

histo.SetStats(0)
histocorr.SetStats(0)
histo.Draw("")
histo.GetXaxis().SetTitle("Reconstructed z (mm)")
histo.SetTitle("Comparison of Hit Killing Methods {0:0.1f} MeV A'".format(mass*1000))
histocorr.SetLineColor(2)
histocorr.Draw("same")
legend = TLegend(.68,.70,.92,.90)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(histo,"Nominal Hit Killing","LP")
legend.AddEntry(histocorr,"Corrected Hit Killing","LP")
legend.Draw("same")
bot.cd()
reference = histo.Clone("reference")
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
ratio = histocorr.Clone("Ratio"+histocorr.GetName())
ratio.Divide(reference)
ratio.SetLineColor(1)
ratio.DrawCopy("pe same")

openPDF(outfile,c)
c.Print(outfile+".pdf")
c.Write()
closePDF(outfile,c)

outfileroot.Close()