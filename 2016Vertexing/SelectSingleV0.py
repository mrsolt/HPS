#!/usr/bin/env python
import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import root_numpy, numpy
import ROOT
from ROOT import TLegend, TH1, TH1F, gROOT, gStyle, TFile, TTree, TCanvas
sys.argv = tmpargv

def print_usage():
    print "\nUsage: {0} <output ROOT file name> <input ROOT file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-e: use this beam energy'
    print '\t-c: only write candidates that pass cuts'
    print '\t-b: only keep best candidate'
    print '\t-o: only keep candidate if it\'s the only one'
    print '\t-m: use MC information'
    print '\t-t: use MC full truth information'
    print '\t-p: make Plots'
    print '\t-h: this help message'
    print

ebeam=2.3
cutOutput = False
onlyBest = False
onlyOnly = False
useMC = False
useFullTruth = False
makePlots = False #Todo make plots

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:cbomthp')
# Parse the command line arguments
for opt, arg in options:
        if opt=='-e':
            ebeam=float(arg)
        if opt=='-c':
            cutOutput = True
        if opt=='-b':
            onlyBest = True
        if opt=='-o':
            onlyOnly = True
        if opt=='-m':
            useMC = True
        if opt=='-t':
            useFullTruth = True
        if opt=='-p':
            makePlots = True
        if opt=='-h':
            print_usage()
            sys.exit(0)

if len(remainder)!=2:
    print_usage()
    sys.exit(0)
print remainder[0]
print remainder[1]

branchlist=["event",
    "run",
    "nSVTHits",
    "nSVTHitsL1",
    "nSVTHitsL1b",
    "uncPX",
    "uncPY",
    "uncPZ",
    "uncP",
    "uncM",
    "uncMErr",
    "uncVX",
    "uncVY",
    "uncVZ",
    "uncCovXX",
    "uncCovYY",
    "uncCovZZ",
    "uncChisq",
    "uncTargProjX",
    "uncTargProjY",
    "uncTargProjXErr",
    "uncTargProjYErr",
    "bscChisq",
    "eleP",
    "posP",
    "elePX",
    "posPX",
    "elePY",
    "posPY",
    "elePZ",
    "posPZ",
    "eleMatchChisq",
    "posMatchChisq",
    "eleTrkChisq",
    "posTrkChisq",
    "eleNTrackHits",
    "posNTrackHits",
    "eleNHitsShared",
    "posNHitsShared",
    "eleTrkT",
    "posTrkT",
    "eleClX",
    "eleClY",
    "eleClZ",
    "posClX",
    "posClY",
    "posClZ",
    "eleClT",
    "posClT",
    "eleIsoStereo",
    "eleIsoAxial",
    "posIsoStereo",
    "posIsoAxial",
    "eleMinPositiveIso",
    "posMinPositiveIso",
    "eleIsoStereoL2",
    "eleIsoAxialL2",
    "posIsoStereoL2",
    "posIsoAxialL2",
    "eleMinPositiveIsoL2",
    "posMinPositiveIsoL2",
    "minIso",
    "minPositiveIso",
    "eleTrkZ0",
    "posTrkZ0",
    "eleTrkD0",
    "posTrkD0",
    "eleTrkLambda",
    "posTrkLambda",
    "eleHasL1",
    "posHasL1",
    "eleHasL2",
    "posHasL2",
    "nPos",
    "eleTrkExtrpYSensorAxialTopL1",
    "eleTrkExtrpYSensorStereoTopL1",
    "eleTrkExtrpYSensorAxialBotL1",
    "eleTrkExtrpYSensorStereoBotL1",
    "posTrkExtrpYSensorAxialTopL1",
    "posTrkExtrpYSensorStereoTopL1",
    "posTrkExtrpYSensorAxialBotL1",
    "posTrkExtrpYSensorStereoBotL1"]

if useMC:
    branchlist.append("triP")
#    branchlist.append("triPair1P")
    branchlist.append("triM")
    branchlist.append("triEndZ")

if useFullTruth:
    branchlist.append("elepdgid")
    branchlist.append("eleparentID")
    branchlist.append("eleHasTruthMatch")
    branchlist.append("elePurity")
    branchlist.append("pospdgid")
    branchlist.append("posparentID")
    branchlist.append("posHasTruthMatch")
    branchlist.append("posPurity")
    branchlist.append("eleL1tthetaY")
    branchlist.append("eleL2tthetaY")
    branchlist.append("eleL3tthetaY")
    branchlist.append("eleL4tthetaY")
    branchlist.append("eleL1bthetaY")
    branchlist.append("eleL2bthetaY")
    branchlist.append("eleL3bthetaY")
    branchlist.append("eleL4bthetaY")
    branchlist.append("posL1tthetaY")
    branchlist.append("posL2tthetaY")
    branchlist.append("posL3tthetaY")
    branchlist.append("posL4tthetaY")
    branchlist.append("posL1bthetaY")
    branchlist.append("posL2bthetaY")
    branchlist.append("posL3bthetaY")
    branchlist.append("posL4bthetaY")
    branchlist.append("eleL1tIsGoodTruthHit")
    branchlist.append("eleL2tIsGoodTruthHit")
    branchlist.append("eleL3tIsGoodTruthHit")
    branchlist.append("eleL4tIsGoodTruthHit")
    branchlist.append("eleL1bIsGoodTruthHit")
    branchlist.append("eleL2bIsGoodTruthHit")
    branchlist.append("eleL3bIsGoodTruthHit")
    branchlist.append("eleL4bIsGoodTruthHit")
    branchlist.append("posL1tIsGoodTruthHit")
    branchlist.append("posL2tIsGoodTruthHit")
    branchlist.append("posL3tIsGoodTruthHit")
    branchlist.append("posL4tIsGoodTruthHit")
    branchlist.append("posL1bIsGoodTruthHit")
    branchlist.append("posL2bIsGoodTruthHit")
    branchlist.append("posL3bIsGoodTruthHit")
    branchlist.append("posL4bIsGoodTruthHit")
events = root_numpy.root2array(remainder[1],branches=branchlist,treename="ntuple")

n = events.size

cut = events["uncP"]>0.0
    #cut = numpy.row_stack((#events["isPair1"]==1,
        #events["uncP"]>0.8*ebeam)).all(0)

names = ["event",
    "run",
    "nSVTHits",
    "nSVTHitsL1",
    "nSVTHitsL1b",
    "uncPX",
    "uncPY",
    "uncPZ",
    "uncP",
    "uncM",
    "uncMErr",
    "uncVX",
    "uncVY",
    "uncVZ",
    "uncCovXX",
    "uncCovYY",
    "uncCovZZ",
    "uncChisq",
    "uncTargProjX",
    "uncTargProjY",
    "uncTargProjXErr",
    "uncTargProjYErr",
    "bscChisq",
    "eleP",
    "posP",
    "elePX",
    "posPX",
    "elePY",
    "posPY",
    "elePZ",
    "posPZ",
    "eleMatchChisq",
    "posMatchChisq",
    "eleTrkChisq",
    "posTrkChisq",
    "eleNTrackHits",
    "posNTrackHits",
    "eleNHitsShared",
    "posNHitsShared",
    "eleTrkT",
    "posTrkT",
    "eleClX",
    "eleClY",
    "eleClZ",
    "posClX",
    "posClY",
    "posClZ",
    "eleClT",
    "posClT",
    "eleIsoStereo",
    "eleIsoAxial",
    "posIsoStereo",
    "posIsoAxial",
    "eleMinPositiveIso",
    "posMinPositiveIso",
    "eleIsoStereoL2",
    "eleIsoAxialL2",
    "posIsoStereoL2",
    "posIsoAxialL2",
    "eleMinPositiveIsoL2",
    "posMinPositiveIsoL2",
    "minIso",
    "minPositiveIso",
    "eleTrkZ0",
    "posTrkZ0",
    "eleTrkD0",
    "posTrkD0",
    "eleTrkLambda",
    "posTrkLambda",
    "eleHasL1",
    "posHasL1",
    "eleHasL2",
    "posHasL2",
    "nPos",
    "eleTrkExtrpYSensorAxialTopL1",
    "eleTrkExtrpYSensorStereoTopL1",
    "eleTrkExtrpYSensorAxialBotL1",
    "eleTrkExtrpYSensorStereoBotL1",
    "posTrkExtrpYSensorAxialTopL1",
    "posTrkExtrpYSensorStereoTopL1",
    "posTrkExtrpYSensorAxialBotL1",
    "posTrkExtrpYSensorStereoBotL1"]

if useMC:
    names.append("triP")
#    names.append("triPair1P")
    names.append("triM")
    names.append("triEndZ")

if useFullTruth:
    names.append("elepdgid")
    names.append("eleparentID")
    names.append("eleHasTruthMatch")
    names.append("elePurity")
    names.append("pospdgid")
    names.append("posparentID")
    names.append("posHasTruthMatch")
    names.append("posPurity")
    names.append("eleL1tthetaY")
    names.append("eleL2tthetaY")
    names.append("eleL3tthetaY")
    names.append("eleL4tthetaY")
    names.append("eleL1bthetaY")
    names.append("eleL2bthetaY")
    names.append("eleL3bthetaY")
    names.append("eleL4bthetaY")
    names.append("posL1tthetaY")
    names.append("posL2tthetaY")
    names.append("posL3tthetaY")
    names.append("posL4tthetaY")
    names.append("posL1bthetaY")
    names.append("posL2bthetaY")
    names.append("posL3bthetaY")
    names.append("posL4bthetaY")
    names.append("eleL1tIsGoodTruthHit")
    names.append("eleL2tIsGoodTruthHit")
    names.append("eleL3tIsGoodTruthHit")
    names.append("eleL4tIsGoodTruthHit")
    names.append("eleL1bIsGoodTruthHit")
    names.append("eleL2bIsGoodTruthHit")
    names.append("eleL3bIsGoodTruthHit")
    names.append("eleL4bIsGoodTruthHit")
    names.append("posL1tIsGoodTruthHit")
    names.append("posL2tIsGoodTruthHit")
    names.append("posL3tIsGoodTruthHit")
    names.append("posL4tIsGoodTruthHit")
    names.append("posL1bIsGoodTruthHit")
    names.append("posL2bIsGoodTruthHit")
    names.append("posL3bIsGoodTruthHit")
    names.append("posL4bIsGoodTruthHit")

stuff = [[events[i],(i,events.dtype[i])] for i in names]
stuff.append([cut,("cut",numpy.int8)])
stuff.append([numpy.zeros(n),("nPass",numpy.int8)])
stuff.append([numpy.zeros(n),("rank",numpy.int8)])

dataarray = [i[0] for i in stuff]
typearray = [i[1] for i in stuff]
output = numpy.core.records.fromarrays(dataarray,dtype=typearray)
currentevent = 0
candidates = []
mccandidates = []

duplicates = 0
for i in xrange(0,n):
    if events[i]["event"]!=currentevent:
        candidates.sort(key=lambda x:events[x]["bscChisq"],reverse=False)
        rank=1
        for j in candidates:
            output[j]["nPass"]=len(candidates)
            output[j]["rank"]=rank
            rank+=1
            if(rank>2):
                duplicates = duplicates + 1
        del candidates[:]
        currentevent = events[i]["event"]
    if output[i]["cut"]!=0:
        candidates.append(i)

if cutOutput:
    output = output[output["cut"]!=0]
if onlyBest:
    output = output[output["rank"]==1]
if onlyOnly:
    output = output[output["nPass"]==1]

print("Number of events with a duplicate V0 = {0}".format(duplicates))
print("Total Number of V0s = {0}".format(n))
root_numpy.array2root(output,remainder[0],mode="recreate",treename="ntuple")

if(makePlots):
    gStyle.SetOptStat(0)
    c = TCanvas("c","c",800,600)
    c.Print(remainder[0]+".pdf[")
    infile = TFile(remainder[1])
    outfile = TFile(remainder[0])
    events_in = infile.Get("ntuple")
    events_out = outfile.Get("ntuple")
    nBins = 50
    plots = []
    plots.append("uncVZ")
    plots.append("uncM")
    minimums = []
    minimums.append(-60)
    minimums.append(0)
    maximums = []
    maximums.append(60)
    maximums.append(0.1*ebeam)
    for i in range(len(plots)):
        plot = plots[i]
        minX = minimums[i]
        maxX = maximums[i]
        events_in.Draw("{0}>>{1}({2},{3},{4})".format(plot,"histo_in",nBins,minX,maxX))
        histo_in = ROOT.gROOT.FindObject("histo_in")
        events_out.Draw("{0}>>{1}({2},{3},{4})".format(plot,"histo_out",nBins,minX,maxX))
        histo_out = ROOT.gROOT.FindObject("histo_out")
        histo_in.Draw()
        histo_in.GetXaxis().SetTitle(plot)
        histo_in.SetTitle(plot)
        histo_out.SetLineColor(2)
        histo_out.Draw("same")
        legend = TLegend(.68,.66,.92,.87)
        legend.SetBorderSize(0)
        legend.SetFillColor(0)
        legend.SetFillStyle(0)
        legend.SetTextFont(42)
        legend.SetTextSize(0.035)
        legend.AddEntry(histo_in,"Before Single V0s","LP")
        legend.AddEntry(histo_out,"Single V0s","LP")
        legend.Draw("same")
        c.SetLogy(1)
        c.Print(remainder[0]+".pdf")
    c.Print(remainder[0]+".pdf]")