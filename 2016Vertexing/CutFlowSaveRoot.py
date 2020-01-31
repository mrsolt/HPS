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
    print '\t-g: minimum uncVZ (default -60 mm)'
    print '\t-i: maximum uncVZ (default 80 mm)'
    print '\t-e: beam energy (default 2.3 GeV)'
    print '\t-q: number of bins (default 140)'
    print '\t-t: cluster time offset (default 56 ns)'
    print '\t-j: uncVX mean (default 0)'
    print '\t-k: uncVX sigma (default 9999)'
    print '\t-m: uncVY mean (default 0)'
    print '\t-n: uncVY sigma (default 9999)'
    print '\t-o: uncTargProjX mean (default 0)'
    print '\t-p: uncTargProjX sigma (default 9999)'
    print '\t-a: uncTargProjY mean (default 0)'
    print '\t-b: uncTargProjY sigma (default 9999)'
    print '\t-f: use preprocessing cuts and labels (default false)'
    print '\t-d: use data file (default False)'
    print '\t-c: use MC file (default False)'
    print '\t-l: use Ap file (default False)'
    print '\t-h: this help message'
    print

zTarg = -4.3
ebeam = 2.3
minVZ = -60
maxVZ = 80
nBins = 140
useData = False
useMC = False
useAp = False
preproc = False
clusterT = 56
uncVX = 0.
uncVXSig = 9999.
uncVY = 0.
uncVYSig = 9999.
uncTargProjX = 0.
uncTargProjXSig = 9999.
uncTargProjY = 0.
uncTargProjYSig = 9999.

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:g:i:e:q:t:j:k:m:n:o:p:a:b:fdcl')

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
		if opt=='-f':
			preproc = True
		if opt=='-d':
			useData = True
		if opt=='-c':
			useMC = True
		if opt=='-l':
			useAp = True
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def saveCutFlow(events,inHisto,cuts,nBins,minX,maxX,labels,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	histos = []
	histos2 = []
	histos3 = []
	cut_tot = ""
	for i in range(len(cuts)):
		cut = cuts[i]
		if(i == 0):
			cut_tot = cut
			cuts_1 = cut
		else:
			cut_tot = cut_tot + "&&" + cut
			cuts_1 = ""
			for j in range(len(cuts)):
				if(j != i):
					if(cuts_1 != ""):
						cuts_1 = cuts_1 + "&&" + cuts[j]
					else:
						cuts_1 = cuts[j]
		events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo{0}".format(i),nBins,minX,maxX),cut_tot)
		histos.append(ROOT.gROOT.FindObject("histo{0}".format(i)))
		events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo2{0}".format(i),nBins,minX,maxX),cuts_1)
		histos2.append(ROOT.gROOT.FindObject("histo2{0}".format(i)))
		events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo3{0}".format(i),nBins,minX,maxX),cuts_1+"&&"+cuts[i])
		histos3.append(ROOT.gROOT.FindObject("histo3{0}".format(i)))
	histos[0].SetTitle(plotTitle + " Inclusive")
	histos[0].GetXaxis().SetTitle(XaxisTitle)
	histos[0].GetYaxis().SetTitle(YaxisTitle)
	histos[0].SetStats(stats)
	color = 1
	for i in range(len(histos)):
		if(color == 5 or color == 10):
			color = color + 1
		histos[i].SetLineColor(color)
		color = color + 1
		histos[i].Sumw2()
		if(i == 0):
			histos[i].Draw("")
		else:
			histos[i].Draw("same")
	legend = TLegend(.08,.46,.42,.87)
	if(inHisto == "uncM"):
		legend = TLegend(.58,.46,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	for i in range(len(labels)):
		legend.AddEntry(histos[i],labels[i],"LP")
	legend.Draw("")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	outfileroot.cd()
	canvas.Write()
	for i in range(len(histos2)):
		#histos[0].Sumw2()
		histos[0].SetLineColor(1)
		histos[0].Draw()
		histos[0].SetTitle(plotTitle + " " + label[i] + " Exclusive")
		histos[0].GetXaxis().SetTitle(XaxisTitle)
		histos[0].GetYaxis().SetTitle(YaxisTitle)
		histos[0].SetStats(stats)
		histos2[i].Sumw2()
		histos2[i].SetLineColor(2)
		histos2[i].Draw("same")
		histos3[i].Sumw2()
		histos3[i].SetLineColor(4)
		histos3[i].Draw("same")
		legend3 = TLegend(.08,.66,.42,.87)
		if(inHisto == "uncM"):
			legend3 = TLegend(.58,.66,.92,.87)
		legend3.SetBorderSize(0)
		legend3.SetFillColor(0)
		legend3.SetFillStyle(0)
		legend3.SetTextFont(42)
		legend3.SetTextSize(0.035)
		legend3.AddEntry(histos[0],labels[0],"LP")
		legend3.AddEntry(histos2[i],"Without " + labels[i],"LP")
		legend3.AddEntry(histos3[i],"With " + labels[i],"LP")
		legend3.Draw("same")
		canvas.Print(outfile+".pdf")
		canvas.Write()
	histos2[0].SetTitle(plotTitle + " Exclusive")
	histos2[0].GetXaxis().SetTitle(XaxisTitle)
	histos2[0].GetYaxis().SetTitle(YaxisTitle)
	histos2[0].SetStats(stats)
	color = 1
	for i in range(len(histos2)):
		if(color == 5 or color == 10):
			color = color + 1
		histos2[i].SetLineColor(color)
		color = color + 1
		#histos2[i].Sumw2()
		if(i == 0):
			histos2[i].Draw("")
			maximum = histos2[0].GetMaximum()
		else:
			histos2[i].Draw("same")
			if(histos2[i].GetMaximum() > maximum):
				maximum = histos2[i].GetMaximum()
	histos2[0].GetYaxis().SetRangeUser(0.1,1.2*maximum)
	legend2 = TLegend(.08,.46,.42,.87)
	if(inHisto == "uncM"):
		legend2 = TLegend(.58,.46,.92,.87)
	legend2.SetBorderSize(0)
	legend2.SetFillColor(0)
	legend2.SetFillStyle(0)
	legend2.SetTextFont(42)
	legend2.SetTextSize(0.035)
	for i in range(len(labels)):
		legend2.AddEntry(histos2[i],labels[i],"LP")
	legend2.Draw("")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	canvas.Write()
	del histos
	del histos2
	del histos3

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

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

if(useData):
	datafile = open(remainder[1],"r")
	dataFiles = []

	for line in (raw.strip().split() for raw in datafile):
		dataFiles.append(line[0])
	dataevents = TChain("ntuple")
	for i in range(len(dataFiles)):
		dataevents.Add(dataFiles[i])

if(useMC):
	mcfile = open(remainder[1],"r")
	mcFiles = []

	for line in (raw.strip().split() for raw in mcfile):
		mcFiles.append(line[0])
	mcevents = TChain("ntuple")
	for i in range(len(mcFiles)):
		mcevents.Add(mcFiles[i])

if(useAp):
	apfile = open(remainder[1],"r")
	apfiles = []
	events = []
	mass = []

	for line in (raw.strip().split() for raw in apfile):
		apfiles.append(TFile(line[0]))

	for i in range(len(apfiles)):
		events.append(apfiles[i].Get("ntuple"))
		events[i].Draw("triM>>dummy({0},{1},{2})".format(1000,0,1))
		dummy = ROOT.gROOT.FindObject("dummy")
		mass.append(dummy.GetMean())
		del dummy

plots = []
plots.append("uncVZ {0} {1}".format(minVZ,maxVZ))
plots.append("uncM {0} {1}".format(0.0,0.1*ebeam))
plots.append("uncP {0} {1}".format(0,1.2*ebeam))

plotlabels = []
plotlabels.append("Reconstructed z [mm]")
plotlabels.append("Reconstructed Mass [GeV]")
plotlabels.append("V0 Momentum [GeV]")

setlog = []
setlog.append(1)
setlog.append(1)
setlog.append(0)

label = []
cuts = []
cuts.append("uncP<9999")
if(preproc):
	cuts.append("isPair1")
	#cuts.append("eleHasL1&&posHasL1")
	#cuts.append("eleHasL2&&posHasL2")
	cuts.append("eleMatchChisq<10&&posMatchChisq<10")
	cuts.append("abs(eleClT-posClT)<1.45")
	cuts.append("abs(eleClT-eleTrkT-{0})<4&&abs(posClT-posTrkT-{0})<4".format(clusterT))
	cuts.append("eleP<1.75")
	cuts.append("eleTrkChisq/(2*eleNTrackHits-5)<6&&posTrkChisq/(2*posNTrackHits-5)<6")
	cuts.append("uncChisq<10")
	cuts.append("eleP>0.4&&posP>0.4")
	cuts.append("uncP<2.4")

	label.append("Preprocessing")
	label.append("Pair1 Trigger")
	#label.append("e+e- L1 Hit")
	#label.append("e+e- L2 Hit")
	label.append("Track/Cluster Match Chisq < 10")
	label.append("Cluster Time Diff < 1.45 ns")
	label.append("Track/Cluster Time Diff < 4 ns")
	label.append("e- Momentum < 1.75 GeV")
	label.append("Track Chisq / dof < 6")
	label.append("Unconstrained Vertex Chisq < 10")
	label.append("e- and e+ Momentum > 0.4 GeV")
	label.append("e+ e- Momentum Sum < 2.4 GeV")

else:
	cuts.append("uncP< 1.15*2.3")
	cuts.append("uncChisq<4")
	cuts.append("abs(uncVX-{0})<3*{1}".format(uncVX,uncVXSig))
	cuts.append("abs(uncVY-{0})<3*{1}".format(uncVY,uncVYSig))
	cuts.append("abs(uncTargProjX-{0})<3*{1}".format(uncTargProjX,uncTargProjXSig))
	cuts.append("abs(uncTargProjY-{0})<3*{1}".format(uncTargProjY,uncTargProjYSig))
	cuts.append("uncP>0.8*2.3")
	cuts.append("min(eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY))>0".format(zTarg))

	label.append("Preselection")
	label.append("V0 momentum < 1.15 E")
	label.append("Unconstrained Vertex Chisq < 4")
	label.append("V0 X 3 sigma")
	label.append("V0 Y 3 sigma")
	label.append("V0 Projection X 3 sigma")
	label.append("V0 Projection Y 3 sigma")
	label.append("V0 momentum > 0.8 E")
	label.append("Nominal Isolation Cut")

openPDF(outfile,c)

for i in range(len(plots)):
	plot = getPlot(plots[i])
	minimum = getMin(plots[i])
	maximum = getMax(plots[i])
	plotlabel = plotlabels[i]
	if(useData):
		saveCutFlow(dataevents,plot,cuts,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " Data",stats=0,logY=setlog[i])
	if(useMC):
		saveCutFlow(mcevents,plot,cuts,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " MC",stats=0,logY=setlog[i])
	if(useAp):
		for j in range(len(mass)):
			saveCutFlow(events[j],plot,cuts,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ ' Ap {0:.0f} MeV'.format(mass[j]*1000),stats=0,logY=setlog[i])

closePDF(outfile,c)
outfileroot.Close()