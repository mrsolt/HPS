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
	print '\t-s: remove shared hits (default True)'
	print '\t-g: minimum VZ (default -30 mm)'
	print '\t-i: maximum VZ (default 60 mm)'
	print '\t-h: this help message'
	print

ebeam=2.3
cutOutput = False
onlyBest = False
onlyOnly = False
useMC = False
useFullTruth = False
makePlots = False
removeSharedHits = True
minVZ = -30
maxVZ = 60

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:cbomthpsg:i:')
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
		if opt=='-s':
			removeSharedHits = False
		if opt=='-g':
			minVZ = float(arg)
		if opt=='-i':
			maxVZ = float(arg)
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
	"tarPX",
	"tarPY",
	"tarPZ",
	"tarP",
	"tarM",
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
	"eleClE",
	"eleClX",
	"eleClY",
	"eleClZ",
	"posClE",
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
	"eleTrkOmega",
	"posTrkOmega",
	"eleTrkZ0Err",
	"posTrkZ0Err",
	"eleTrkLambdaErr",
	"posTrkLambdaErr",
	"eleTrkOmegaErr",
	"posTrkOmegaErr",
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
	#branchlist.append("triP")
	branchlist.append("triStartP")
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
	branchlist.append("eleStartPX")
	branchlist.append("eleStartPY")
	branchlist.append("eleStartPZ")
	branchlist.append("eleStartP")
	branchlist.append("posStartPX")
	branchlist.append("posStartPY")
	branchlist.append("posStartPZ")
	branchlist.append("posStartP")
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
	branchlist.append("eleL1tInthetaY")
	branchlist.append("eleL2tInthetaY")
	branchlist.append("eleL3tInthetaY")
	branchlist.append("eleL4tInthetaY")
	branchlist.append("eleL1bInthetaY")
	branchlist.append("eleL2bInthetaY")
	branchlist.append("eleL3bInthetaY")
	branchlist.append("eleL4bInthetaY")
	branchlist.append("posL1tInthetaY")
	branchlist.append("posL2tInthetaY")
	branchlist.append("posL3tInthetaY")
	branchlist.append("posL4tInthetaY")
	branchlist.append("posL1bInthetaY")
	branchlist.append("posL2bInthetaY")
	branchlist.append("posL3bInthetaY")
	branchlist.append("posL4bInthetaY")
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

if(not removeSharedHits):
	cut = events["uncP"]>0.0
else:
	cut = numpy.row_stack((events["eleNHitsShared"]<1.0,
		events["posNHitsShared"]<1.0)).all(0)

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
	"tarPX",
	"tarPY",
	"tarPZ",
	"tarP",
	"tarM",
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
	"eleClE",
	"eleClX",
	"eleClY",
	"eleClZ",
	"posClE",
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
	"eleTrkOmega",
	"posTrkOmega",
	"eleTrkZ0Err",
	"posTrkZ0Err",
	"eleTrkLambdaErr",
	"posTrkLambdaErr",
	"eleTrkOmegaErr",
	"posTrkOmegaErr",
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
	#names.append("triP")
	names.append("triStartP")
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
	names.append("eleStartPX")
	names.append("eleStartPY")
	names.append("eleStartPZ")
	names.append("eleStartP")
	names.append("posStartPX")
	names.append("posStartPY")
	names.append("posStartPZ")
	names.append("posStartP")
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
	names.append("eleL1tInthetaY")
	names.append("eleL2tInthetaY")
	names.append("eleL3tInthetaY")
	names.append("eleL4tInthetaY")
	names.append("eleL1bInthetaY")
	names.append("eleL2bInthetaY")
	names.append("eleL3bInthetaY")
	names.append("eleL4bInthetaY")
	names.append("posL1tInthetaY")
	names.append("posL2tInthetaY")
	names.append("posL3tInthetaY")
	names.append("posL4tInthetaY")
	names.append("posL1bInthetaY")
	names.append("posL2bInthetaY")
	names.append("posL3bInthetaY")
	names.append("posL4bInthetaY")
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
sharedhits = 0
sharedhits_duplicates = 0
for i in xrange(0,n):
	if events[i]["event"]!=currentevent:
		candidates.sort(key=lambda x:events[x]["bscChisq"],reverse=False)
		rank=1
		for j in candidates:
			output[j]["nPass"]=len(candidates)
			output[j]["rank"]=rank
			rank+=1
			if(len(candidates)>1):
				duplicates = duplicates + 1
				if(events[i]["eleNHitsShared"]>0.5 or events[i]["posNHitsShared"]>0.5):
					sharedhits_duplicates = sharedhits_duplicates + 1
		del candidates[:]
		currentevent = events[i]["event"]
	if output[i]["cut"]!=0:
		candidates.append(i)
	else:
		sharedhits = sharedhits + 1

if cutOutput:
	output = output[output["cut"]!=0]
if onlyBest:
	output = output[output["rank"]==1]
if onlyOnly:
	output = output[output["nPass"]==1]

print("Total Number of of Shared Hits = {0}".format(sharedhits))
print("Total Number of Duplicate V0s = {0}".format(duplicates))
print("Total Number of Duplicate V0s with Shared Hits = {0}".format(sharedhits_duplicates))
print("Total Number of V0s = {0}".format(n))
print("Total Number of V0s Remaining = {0}".format(output.size))

root_numpy.array2root(output,remainder[0]+".root",mode="recreate",treename="ntuple")

if(makePlots):
	outfileroot = TFile(remainder[0]+"_plots.root","RECREATE")
	gStyle.SetOptStat(0)
	c = TCanvas("c","c",800,600)
	c.Print(remainder[0]+"_plots.pdf[")
	infile = TFile(remainder[1])
	outfile = TFile(remainder[0]+".root")
	events_in = infile.Get("ntuple")
	events_out = outfile.Get("ntuple")
	nBins = 90
	plots = []
	plots.append("uncVZ")
	plots.append("uncM")
	plotlabels = []
	plotlabels.append("Reconstructed Z (mm)")
	plotlabels.append("Mass (GeV)")
	minimums = []
	minimums.append(minVZ)
	minimums.append(0)
	maximums = []
	maximums.append(maxVZ)
	maximums.append(0.1*ebeam)
	for i in range(len(plots)):
		plot = plots[i]
		minX = minimums[i]
		maxX = maximums[i]
		events_in.Draw("{0}>>{1}({2},{3},{4})".format(plot,"histo_in",nBins,minX,maxX))
		histo_in = ROOT.gROOT.FindObject("histo_in")
		events_out.Draw("{0}>>{1}({2},{3},{4})".format(plot,"histo_out",nBins,minX,maxX))
		histo_out = ROOT.gROOT.FindObject("histo_out")
		histo_in.Sumw2()
		histo_out.Sumw2()
		histo_in.Draw()
		histo_in.GetXaxis().SetTitle(plotlabels[i])
		histo_in.SetTitle("Single V0s")
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
		outfileroot.cd()
		histo_in.Write("{0} Before".format(plot))
		histo_out.Write("{0} After".format(plot))
		c.SetLogy(1)
		c.Print(remainder[0]+"_plots.pdf")
		c.Write()
		c.SetLogy(0)
		c.Print(remainder[0]+"_plots.pdf")
	c.Print(remainder[0]+"_plots.pdf]")
	outfileroot.Close()
