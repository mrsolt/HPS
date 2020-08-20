import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TLatex
sys.argv = tmpargv

#List arguments
def print_usage():
	print "\nUsage: {0} <output file base name> <input root file>".format(sys.argv[0])
	print "Arguments: "
	print '\t-z: target position (default -4.3 mm)'
	print '\t-g: minimum uncVZ (default -60 mm)'
	print '\t-i: maximum uncVZ (default 80 mm)'
	print '\t-e: beam energy (default 2.3 GeV)'
	print '\t-q: number of bins (default 140)'
	print '\t-t: cluster time offset (default 56 ns)'
	print '\t-y: plot label'
	print '\t-d: use data file (default False)'
	print '\t-w: make cutflow plots (default False)'
	print '\t-x: output new root tree (default False)'
	print '\t-h: this help message'
	print

zTarg = -4.3
ebeam = 2.3
minVZ = -100
maxVZ = 100
nBins = 200
makeCutflow = False
makeNewTree = False
clusterTdata = 56
clusterTmc = 43
clusterTap = 45
Label = ""

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:g:i:e:q:t:y:wx')

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
		if opt=='-y':
			Label=str(arg)
		if opt=='-w':
			makeCutflow = True
		if opt=='-x':
			makeNewTree = True
		if opt=='-h':
			print_usage()
			sys.exit(0)

if(not makeCutflow and not makeNewTree):
	print("Both makeCutflow and makeNewTree are false.")
	print("Choose option w and/or option x, otherwise this code does nothing.")
	print_usage()
	sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def saveCutFlow(events,inHisto,cuts,nBins,minX,maxX,labels,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	histos = []
	histos2 = []
	histos3 = []
	histos4 = []
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
		events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histos{0}_{1}".format(i,inHisto),nBins,minX,maxX),cut_tot)
		histos.append(ROOT.gROOT.FindObject("histos{0}_{1}".format(i,inHisto)))

	outfileroot.cd()
	if(inHisto == "uncVZ"):
		events.Draw("uncVZ:uncM>>{0}({1},{2},{3},{1},{4},{5})".format("histo_2D",nBins,0.,0.2,minX,maxX),cut_tot)
		histo_2D = ROOT.gROOT.FindObject("histo_2D")
		canvas.SetLogz(1)
		canvas.SetLogy(0)
		histo_2D.Draw("COLZ")
		histo_2D.SetTitle("Vz vs Mass All Cuts")
		histo_2D.GetXaxis().SetTitle("Mass [GeV]")
		histo_2D.GetYaxis().SetTitle("Reconstructed z [mm]")
		histo_2D.SetStats(stats)
		canvas.Print(outfile+".pdf")
		canvas.Write()
		histo_2D.Write("histo_2D")
	histos[0].SetTitle(plotTitle + " Inclusive")
	histos[0].GetXaxis().SetTitle(XaxisTitle)
	histos[0].GetYaxis().SetTitle("dN")
	histos[0].GetXaxis().SetLabelSize(0.05)
	histos[0].GetYaxis().SetLabelSize(0.05)
	#histos[0].GetZaxis().SetLabelSize(0.05)
	histos[0].GetXaxis().SetTitleOffset(0.8)
	histos[0].GetXaxis().SetTitleSize(0.06)
	histos[0].GetYaxis().SetTitleOffset(0.8)
	histos[0].GetYaxis().SetTitleSize(0.06)
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
			histos[i].Write("histos{0}_{1}".format(i,inHisto))
		else:
			histos[i].Draw("same")
			histos[i].Write("histos{0}_{1}".format(i,inHisto))
	legend = TLegend(.1,.46,.42,.87)
	if(inHisto == "uncM"):
		legend = TLegend(.5,.46,.84,.87)
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
	canvas.Write()

	del histos

def saveCuts(dataevents,mcevents,apevents1,apevents2,i,lineval,nBins,minX,maxX,label,var,varmc,varap,outfile,canvas,legendpos,XaxisTitle="",YaxisTitle="",stats=0,logY=0):
	dataevents.Draw("{0}>>{1}({2},{3},{4})".format(var,"histo5{0}data".format(i),nBins,minX,maxX))
	histo5data = ROOT.gROOT.FindObject("histo5{0}data".format(i))
	mcevents.Draw("{0}>>{1}({2},{3},{4})".format(varmc,"histo5{0}mc".format(i),nBins,minX,maxX))
	histo5mc = ROOT.gROOT.FindObject("histo5{0}mc".format(i))
	apevents1.Draw("{0}>>{1}({2},{3},{4})".format(varap,"histo5{0}ap1".format(i),nBins,minX,maxX))
	histo5ap1 = ROOT.gROOT.FindObject("histo5{0}ap1".format(i))
	apevents2.Draw("{0}>>{1}({2},{3},{4})".format(varap,"histo5{0}ap2".format(i),nBins,minX,maxX))
	histo5ap2 = ROOT.gROOT.FindObject("histo5{0}ap2".format(i))

	canvas.SetLogy(logY)
	histo5data.Sumw2()
	histo5mc.Sumw2()
	histo5ap1.Sumw2()
	histo5ap2.Sumw2()
	if(histo5data.Integral() != 0):
		histo5data.Scale(1./histo5data.Integral())
	if(histo5mc.Integral() != 0):
		histo5mc.Scale(1./histo5mc.Integral())
	if(histo5ap1.Integral() != 0):
		histo5ap1.Scale(1./histo5ap1.Integral())
	if(histo5ap2.Integral() != 0):
		histo5ap2.Scale(1./histo5ap2.Integral())
	lineval1 = float(getPlot(lineval))
	lineval2 = getMin(lineval)
	maximum = histo5data.GetMaximum()
	if(histo5mc.GetMaximum() > maximum):
		maximum = histo5mc.GetMaximum()
	if(histo5ap1.GetMaximum() > maximum):
		maximum = histo5ap1.GetMaximum()
	if(histo5ap2.GetMaximum() > maximum):
		maximum = histo5ap2.GetMaximum()
	minimum = histo5data.GetMinimum(0)
	if(histo5mc.GetMinimum(0) < minimum):
		minimum = histo5mc.GetMinimum(0)
	if(histo5ap1.GetMinimum(0) < minimum):
		minimum = histo5ap1.GetMinimum(0)
	if(histo5ap2.GetMinimum(0) < minimum):
		minimum = histo5ap2.GetMinimum(0)
	histo5data.Draw()
	histo5data.SetTitle(label)
	histo5data.GetXaxis().SetTitle(XaxisTitle)
	histo5data.GetYaxis().SetTitle("dN")
	histo5data.GetXaxis().SetLabelSize(0.05)
	histo5data.GetYaxis().SetLabelSize(0.05)
	#histo5data.GetZaxis().SetLabelSize(0.05)
	histo5data.GetXaxis().SetTitleOffset(0.8)
	histo5data.GetXaxis().SetTitleSize(0.06)
	histo5data.GetYaxis().SetTitleOffset(0.8)
	histo5data.GetYaxis().SetTitleSize(0.06)
	if(logY == 0):
		histo5data.GetYaxis().SetRangeUser(0,maximum*1.3)
	else:
		histo5data.GetYaxis().SetRangeUser(minimum/2,maximum*10)
	histo5data.SetStats(stats)
	histo5mc.SetLineColor(2)
	histo5mc.Draw("same")
	histo5ap1.SetLineColor(1)
	histo5ap1.Draw("same")
	histo5ap2.SetLineColor(8)
	histo5ap2.Draw("same")
	if(logY == 0):
		line1 = TLine(lineval1,0,lineval1,maximum*1.3)
	else:
		line1 = TLine(lineval1,0,lineval1,maximum*10)
	line1.SetLineColor(2)
	line1.SetLineWidth(3)
	line1.Draw("")
	if(lineval2 != ""):
		if(logY == 0):
			line2 = TLine(lineval2,0,lineval2,maximum)
		else:
			line2 = TLine(lineval2,0,lineval2,maximum*10)
		line2.SetLineColor(2)
		line2.SetLineWidth(3)
		line2.Draw("")
	if(legendpos == 0):
		legend = TLegend(.1,.66,.42,.87)
	else:
		legend = TLegend(.65,.66,.97,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.05)
	legend.AddEntry(histo5data,"Run 7800","LP")
	legend.AddEntry(histo5mc,"MC","LP")
	legend.AddEntry(histo5ap1,"80 MeV A'","LP")
	legend.AddEntry(histo5ap2,"100 MeV A'","LP")
	legend.Draw("")
	canvas.Print(outfile+".pdf")
	canvas.Write()
	histo5data.Write("histo5{0}data".format(i))
	histo5mc.Write("histo5{0}mc".format(i))
	histo5ap1.Write("histo5{0}ap1".format(i))
	histo5ap2.Write("histo5{0}ap2".format(i))
	del histo5data
	del histo5mc
	del histo5ap1
	del histo5ap2

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

def getNEvents(events,cut_tot,i):
	events.Draw("{0}>>{1}({2},{3},{4})".format("uncVZ","histo0",100,-9999,9999),cut_tot)
	histo0 = ROOT.gROOT.FindObject("histo0")
	entries = histo0.GetEntries()
	del histo0
	return entries

datafile = open(remainder[1],"r")
dataFiles = []
for line in (raw.strip().split() for raw in datafile):
	dataFiles.append(line[0])
dataevents = TChain("ntuple")
for i in range(len(dataFiles)):
	dataevents.Add(dataFiles[i])

mcfile = open(remainder[2],"r")
mcFiles = []
for line in (raw.strip().split() for raw in mcfile):
	mcFiles.append(line[0])
mcevents = TChain("ntuple")
for i in range(len(mcFiles)):
	mcevents.Add(mcFiles[i])

apfile1 = open(remainder[3],"r")
apFiles1 = []
for line in (raw.strip().split() for raw in apfile1):
	apFiles1.append(line[0])
apevents1 = TChain("ntuple")
for i in range(len(apFiles1)):
	apevents1.Add(apFiles1[i])

apfile2 = open(remainder[4],"r")
apFiles2 = []
for line in (raw.strip().split() for raw in apfile2):
	apFiles2.append(line[0])
apevents2 = TChain("ntuple")
for i in range(len(apFiles2)):
	apevents2.Add(apFiles2[i])

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
var = []
cuts.append("uncP<9999")

cuts.append("isPair1")
cuts.append("eleMatchChisq<10&&posMatchChisq<10")
cuts.append("abs(eleClT-posClT)<1.45")
cuts.append("abs(eleClT-eleTrkT-{0})<4&&abs(posClT-posTrkT-{0})<4".format(clusterTdata))
cuts.append("eleP<1.75")
cuts.append("eleTrkChisq/(2*eleNTrackHits-5)<6&&posTrkChisq/(2*posNTrackHits-5)<6")
cuts.append("uncChisq<10")
cuts.append("eleP>0.4&&posP>0.4")
cuts.append("uncP<2.4")

cutsmc = []
for i in range(len(cuts)):
	if(i == 4):
		cutsmc.append("abs(eleClT-eleTrkT-{0})<4&&abs(posClT-posTrkT-{0})<4".format(clusterTmc))
	else:
		cutsmc.append(cuts[i])

cutsap = []
for i in range(len(cuts)):
	if(i == 4):
		cutsap.append("abs(eleClT-eleTrkT-{0})<4&&abs(posClT-posTrkT-{0})<4".format(clusterTap))
	else:
		cutsap.append(cuts[i])

label.append("Preprocessing")
label.append("Pair1 Trigger")
label.append("Track/Cluster Match N#sigma < 10")
label.append("Cluster Time Diff < 1.45 ns")
label.append("Cluster-Track Time Diff < 4 ns")
label.append("0.4 GeV < e- Momentum < 1.75 GeV")
label.append("Track #chi^{2} / dof < 6")
label.append("Unconstrained Vertex #chi^{2} < 10")
label.append("e+ Momentum > 0.4 GeV")
label.append("V0 Momentum < 2.4 GeV")

var.append("isPair1 -1 2")
var.append("eleMatchChisq 0 15")
var.append("posMatchChisq 0 15")
var.append("eleClT-posClT -6 6")
var.append("eleClT-eleTrkT-{0} -10 10".format(clusterTdata))
var.append("posClT-posTrkT-{0} -10 10".format(clusterTdata))
var.append("eleP 0 2.5")
var.append("eleTrkChisq/(2*eleNTrackHits-5) 0 12")
var.append("posTrkChisq/(2*posNTrackHits-5) 0 12")
var.append("uncChisq 0 20")
var.append("posP 0 2.5")
var.append("uncP 0 2.8")

setlog2 = []
setlog2.append(1)
setlog2.append(1)
setlog2.append(1)
setlog2.append(1)
setlog2.append(1)
setlog2.append(1)
setlog2.append(0)
setlog2.append(1)
setlog2.append(1)
setlog2.append(1)
setlog2.append(0)
setlog2.append(0)

varmc = []
for i in range(len(var)):
	if(i == 4):
		varmc.append("eleClT-eleTrkT-{0} -10 10".format(clusterTmc))
	elif(i == 5):
		varmc.append("posClT-posTrkT-{0} -10 10".format(clusterTmc))
	else:
		varmc.append(var[i])

varap = []
for i in range(len(var)):
	if(i == 4):
		varap.append("eleClT-eleTrkT-{0} -10 10".format(clusterTap))
	elif(i == 5):
		varap.append("posClT-posTrkT-{0} -10 10".format(clusterTap))
	else:
		varap.append(var[i])

xlabel = []
xlabel.append("Passes Trigger Requirement")
xlabel.append("Electron Match N#sigma")
xlabel.append("Positron Match N#sigma")
xlabel.append("Electron - Positron Cluster Time Difference (ns)")
xlabel.append("Electron Cluster - Track Time Difference (ns)")
xlabel.append("Positron Cluster - Track Time Difference (ns)")
xlabel.append("Electron Momentum (GeV) ")
xlabel.append("Electron Track #chi^{2}/dof")
xlabel.append("Positron Track #chi^{2}/dof")
xlabel.append("Unconstrained #chi^{2}")
xlabel.append("Positron Momentum (GeV) ")
xlabel.append("V0 Momentum (GeV)")

legendpos = []
legendpos.append(0)
legendpos.append(1)
legendpos.append(1)
legendpos.append(0)
legendpos.append(0)
legendpos.append(0)
legendpos.append(1)
legendpos.append(1)
legendpos.append(1)
legendpos.append(1)
legendpos.append(1)
legendpos.append(0)

lines = []
lines.append("0.5")
lines.append("10")
lines.append("10")
lines.append("-1.45 1.45")
lines.append("-4 4")
lines.append("-4 4")
lines.append("0.4 1.75")
lines.append("6")
lines.append("6")
lines.append("10")
lines.append("0.4")
lines.append("2.4")

index = []
index.append(1)
index.append(2)
index.append(2)
index.append(3)
index.append(4)
index.append(4)
index.append(5)
index.append(6)
index.append(6)
index.append(7)
index.append(8)
index.append(9)

cut_all = ""

for i in range(len(cuts)):
	cut = cuts[i]
	if(i == 0):
		cut_all = cut
	else:
		cut_all = cut_all + "&&" + cut

if(makeCutflow):
	outfile = remainder[0]+"_cutflow"
	outfileroot = TFile(remainder[0]+"_cutflow.root","RECREATE")

	openPDF(outfile,c)

	for i in range(len(plots)):
		plot = getPlot(plots[i])
		minimum = getMin(plots[i])
		maximum = getMax(plots[i])
		plotlabel = plotlabels[i]
		saveCutFlow(dataevents,plot,cuts,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " {0} {1}".format(Label,'Run 7800'),stats=0,logY=setlog[i])
		saveCutFlow(mcevents,plot,cutsmc,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " {0} {1}".format(Label,'MC'),stats=0,logY=setlog[i])
		saveCutFlow(apevents1,plot,cutsap,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " {0} {1}".format(Label,"80 MeV A'"),stats=0,logY=setlog[i])
		saveCutFlow(apevents2,plot,cutsap,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " {0} {1}".format(Label,"100 MeV A'"),stats=0,logY=setlog[i])

	for i in range(len(var)):
		plot = getPlot(var[i])
		plotmc = getPlot(varmc[i])
		plotap = getPlot(varap[i])
		minimum = getMin(var[i])
		maximum = getMax(var[i])
		saveCuts(dataevents,mcevents,apevents1,apevents2,i,lines[i],nBins,minimum,maximum,label[index[i]],plot,plotmc,plotap,outfile,c,legendpos[i],XaxisTitle=xlabel[i],logY=setlog2[i])

	histo_cutflow_data = TH1F("histo_cutflow_data","histo_cutflow_data",len(cuts),0,len(cuts))
	histo_cutflow_mc = TH1F("histo_cutflow_mc","histo_cutflow_mc",len(cuts),0,len(cuts))
	histo_cutflow_ap1 = TH1F("histo_cutflow_ap1","histo_cutflow_ap1",len(cuts),0,len(cuts))
	histo_cutflow_ap2 = TH1F("histo_cutflow_ap2","histo_cutflow_ap2",len(cuts),0,len(cuts))

	for i in range(len(cuts)):
		if(i == 0):
			cut_tot = cuts[i]
			cut_totmc = cuts[i]
			cut_totap = cuts[i]
		else:
			cut_tot = cut_tot + "&&" + cuts[i]
			cut_totmc = cut_totmc + "&&" + cutsmc[i]
			cut_totap = cut_totap + "&&" + cutsap[i]
		n_data = getNEvents(dataevents,cut_tot,i)
		n_mc = getNEvents(mcevents,cut_totmc,i)
		n_ap1 = getNEvents(apevents1,cut_totap,i)
		n_ap2 = getNEvents(apevents2,cut_totap,i)
		print("Cut {0}: Data Entries {1},  MC Entries {2},  80 MeV A' Entries {3},  100 MeV A' Entries {4}".format(label[i],n_data,n_mc,n_ap1,n_ap2))
		print("Fractional Cut {0}: Data Entries {1},  MC Entries {2},  80 MeV A' Entries {3},  100 MeV A' Entries {4}".format(label[i],n_data/getNEvents(dataevents,"",i),n_mc/getNEvents(mcevents,"",i),n_ap1/getNEvents(apevents1,"",i),n_ap2/getNEvents(apevents2,"",i)))
		histo_cutflow_data.SetBinContent(i+1,n_data)
		histo_cutflow_mc.SetBinContent(i+1,n_mc)
		histo_cutflow_ap1.SetBinContent(i+1,n_ap1)
		histo_cutflow_ap2.SetBinContent(i+1,n_ap2)

	histo_cutflow_data.Sumw2()
	histo_cutflow_mc.Sumw2()
	histo_cutflow_ap1.Sumw2()
	histo_cutflow_ap2.Sumw2()
	#histo_cutflow_data.Scale(1./histo_cutflow_data.Integral())
	#histo_cutflow_mc.Scale(1./histo_cutflow_mc.Integral())
	#histo_cutflow_ap1.Scale(1./histo_cutflow_ap1.Integral())
	#histo_cutflow_ap2.Scale(1./histo_cutflow_ap2.Integral())
	maximum = histo_cutflow_data.GetMaximum()
	if(histo_cutflow_mc.GetMaximum() > maximum):
		maximum = histo_cutflow_mc.GetMaximum()
	if(histo_cutflow_ap1.GetMaximum() > maximum):
		maximum = histo_cutflow_ap1.GetMaximum()
	if(histo_cutflow_ap2.GetMaximum() > maximum):
		maximum = histo_cutflow_ap2.GetMaximum()

	histo_cutflow_data.GetYaxis().SetRangeUser(0.9,maximum*1.3)
	histo_cutflow_data.Draw()
	histo_cutflow_data.SetTitle("Cut Flow")
	histo_cutflow_data.GetXaxis().SetTitle("Cut")

	histo_cutflow_mc.SetLineColor(2)
	histo_cutflow_mc.Draw("same")
	histo_cutflow_ap1.SetLineColor(1)
	histo_cutflow_ap1.Draw("same")
	histo_cutflow_ap2.SetLineColor(8)
	histo_cutflow_ap2.Draw("same")

	legend = TLegend(.65,.66,.97,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histo_cutflow_data,"Run 7800","LP")
	legend.AddEntry(histo_cutflow_mc,"MC","LP")
	legend.AddEntry(histo_cutflow_ap1,"80 MeV A'","LP")
	legend.AddEntry(histo_cutflow_ap2,"100 MeV A'","LP")
	legend.Draw()

	c.Print(outfile+".pdf")
	c.Write()
	histo_cutflow_data.Write("histo_cutflow_data")
	histo_cutflow_mc.Write("histo_cutflow_mc")
	histo_cutflow_ap1.Write("histo_cutflow_ap1")
	histo_cutflow_ap2.Write("histo_cutflow_ap2")

	closePDF(outfile,c)
	outfileroot.Close()

if(makeNewTree):
	print (events.GetEntries())
	print (cut_all)
	outFile = TFile(remainder[0]+".root","RECREATE")
	events_new = events.CopyTree(cut_all)
	print (events_new.GetEntries())
	events_new.Write("ntuple",TTree.kOverwrite)
	gDirectory.ls()
