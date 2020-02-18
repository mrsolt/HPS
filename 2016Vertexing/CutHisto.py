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
    print '\t-e: beam energy (default 2.3 GeV)'
    print '\t-t: cluster time offset (default 56 ns)'
    print '\t-j: uncVX mean (default 0)'
    print '\t-k: uncVX sigma (default 9999)'
    print '\t-m: uncVY mean (default 0)'
    print '\t-n: uncVY sigma (default 9999)'
    print '\t-o: uncTargProjX mean (default 0)'
    print '\t-p: uncTargProjX sigma (default 9999)'
    print '\t-a: uncTargProjY mean (default 0)'
    print '\t-b: uncTargProjY sigma (default 9999)'
    print '\t-h: this help message'
    print

zTarg = -4.3
ebeam = 2.3
clusterT = 56
uncVX = 0.
uncVXSig = 9999.
uncVY = 0.
uncVYSig = 9999.
uncTargProjX = 0.
uncTargProjXSig = 9999.
uncTargProjY = 0.
uncTargProjYSig = 9999.

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:e:t:j:k:m:n:o:p:a:b:')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-e':
			ebeam = float(arg)
		if opt=='-t':
			clusterT = float(arg)
		if opt=='-j':
			uncVX=float(arg)
		if opt=='-k':
			uncVXSig=float(arg)
		if opt=='-m':
			uncVY=float(arg)
		if opt=='-n':
			uncVYSig=float(arg)
		if opt=='-o':
			uncTargProjX=float(arg)
		if opt=='-p':
			uncTargProjXSig=float(arg)
		if opt=='-a':
			uncTargProjY=float(arg)
		if opt=='-b':
			uncTargProjYSig=float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

outfile = remainder[0]

file = open(remainder[1],"r")
Files = []

for line in (raw.strip().split() for raw in file):
	Files.append(line[0])
events = TChain("ntuple")
for i in range(len(Files)):
	events.Add(Files[i])

cuts = []
cuts.append("uncP<9999")
#cuts.append("isPair1")
cuts.append("eleHasL1&&posHasL1")
cuts.append("eleHasL2&&posHasL2")
#cuts.append("eleMatchChisq<10")
#cuts.append("posMatchChisq<10")
#cuts.append("abs(eleClT-posClT)<1.45")
#cuts.append("abs(eleClT-eleTrkT-{0})<4".format(clusterT))
#cuts.append("abs(posClT-posTrkT-{0})<4".format(clusterT))
#cuts.append("eleP<1.75")
#cuts.append("eleTrkChisq/(2*eleNTrackHits-5)<6")
#cuts.append("posTrkChisq/(2*posNTrackHits-5)<6")
#cuts.append("uncChisq<10")
#cuts.append("eleP>0.4")
#cuts.append("posP>0.4")
#cuts.append("uncP<2.4")
cuts.append("uncChisq<4")
cuts.append("uncP>1.55")
#cuts.append("uncP< 1.15*2.3")
cuts.append("abs(uncVX-{0})<3*{1}".format(uncVX,uncVXSig))
cuts.append("abs(uncVY-{0})<3*{1}".format(uncVY,uncVYSig))
cuts.append("abs(uncVX-(uncVZ-{2})*uncPX/uncPZ-{0})<3*{1}".format(uncTargProjX,uncTargProjXSig,zTarg))
cuts.append("abs(uncVY-(uncVZ-{2})*uncPY/uncPZ-{0})<3*{1}".format(uncTargProjY,uncTargProjYSig,zTarg))
cuts.append("min(eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega))),posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega))))".format(zTarg))

label = []
#label.append("Preprocessing")
label.append("Preselection")
#label.append("Pairs1")
label.append("e+e- L1 Hit")
label.append("e+e- L2 Hit")
#label.append("e- Track/Cluster Match Chisq < 10")
#label.append("e+ Track/Cluster Match Chisq < 10")
#label.append("Cluster Time Diff < 2 ns")
#label.append("e- Track/Cluster Time Diff < 4 ns")
#label.append("e+ Track/Cluster Time Diff < 4 ns")
#label.append("e- Momentum < 1.75 GeV")
#label.append("e- Track Chisq / dof < 6")
#label.append("e+ Track Chisq / dof < 6")
#label.append("Unconstrained Vertex Chisq < 10")
#label.append("V0 momentum < 2.4 GeV")
#label.append("e- momentum > 0.4 GeV")
#label.append("e+ momentum > 0.4 GeV")
label.append("Unconstrained Vertex Chisq < 4")
label.append("V0 momentum > 1.55 GeV")
#label.append("V0 momentum < 1.15 E")
label.append("V0 X 3 sigma")
label.append("V0 Y 3 sigma")
label.append("V0 Projection X 3 sigma")
label.append("V0 Projection Y 3 sigma")
label.append("Isolation Cut")

def getNEvents(events,cut_tot,i):
	events.Draw("{0}>>{1}({2},{3},{4})".format("uncVZ","histo0",100,-9999,9999),cut_tot)
	histo0 = ROOT.gROOT.FindObject("histo0")
	entries = histo0.GetEntries()
	del histo0
	return entries

outfile = TFile(remainder[0]+".root","RECREATE")
outfile.cd()

histo = TH1F("histo","histo",len(cuts),0,len(cuts))

cut_tot = ""
for i in range(len(cuts)):
	if(i == 0):
		cut_tot = cuts[i]
	else:
		cut_tot = cut_tot + "&&" + cuts[i]
	n = getNEvents(events,cut_tot,i)
	print("Cut {0}: Entries {1}".format(label[i],n))
	histo.SetBinContent(i+1,n)

histo.Draw()
histo.SetTitle("Cut Flow")
histo.GetXaxis().SetTitle("Cut")
outfile.Write()
outfile.Close()
