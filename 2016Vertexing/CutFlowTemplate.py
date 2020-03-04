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
    print '\t-r: is L1L2 category (default false)'
    print '\t-y: plot label'
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
L1L2 = False
clusterT = 56
uncVX = 0.
uncVXSig = 9999.
uncVY = 0.
uncVYSig = 9999.
uncTargProjX = 0.
uncTargProjXSig = 9999.
uncTargProjY = 0.
uncTargProjYSig = 9999.
Label = ""

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:g:i:e:q:t:j:k:m:n:o:p:a:b:y:frdcl')

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
		if opt=='-y':
			Label=str(arg)
		if opt=='-f':
			preproc = True
		if opt=='-r':
			L1L2 = True
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
		events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo2{0}_{1}".format(i,inHisto),nBins,minX,maxX),cuts_1)
		histos2.append(ROOT.gROOT.FindObject("histo2{0}_{1}".format(i,inHisto)))
		events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo3{0}_{1}".format(i,inHisto),nBins,minX,maxX),cuts_1+"&&"+cuts[i])
		histos3.append(ROOT.gROOT.FindObject("histo3{0}_{1}".format(i,inHisto)))
		if(inHisto == "uncVZ"):
			events.Draw("uncVZ:uncM>>{0}({1},{2},{3},{1},{4},{5})".format("histo4{0}_{1}".format(i,inHisto),nBins,0.,0.2,minX,maxX),cuts_1)
			histos4.append(ROOT.gROOT.FindObject("histo4{0}_{1}".format(i,inHisto)))
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
	histos[0].GetYaxis().SetTitle(YaxisTitle)
	histos[0].SetStats(stats)
	color = 1
	for i in range(len(histos4)):
		canvas.SetLogy(0)
		histos4[i].Draw("COLZ")
		histos4[i].SetTitle("Vz vs Mass " + label[i] + " Exclusive")
		histos4[i].GetXaxis().SetTitle("Mass [GeV]")
		histos4[i].GetYaxis().SetTitle("Reconstructed z [mm]")
		histos4[i].SetStats(stats)
		canvas.Print(outfile+".pdf")
		canvas.Write()
		histos4[i].Write("histo4{0}_{1}".format(i,inHisto))
		canvas.SetLogy(logY)

	for i in range(len(histos)):
		if(color == 5 or color == 10):
			color = color + 1
		histos[i].SetLineColor(color)
		color = color + 1
		histos[i].Scale(1.0)
		if(i == 0):
			histos[i].Draw("")
			histos[i].Write("histos{0}_{1}".format(i,inHisto))
		else:
			histos[i].Draw("same")
			histos[i].Write("histos{0}_{1}".format(i,inHisto))
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
	canvas.Write()
	for i in range(len(histos2)):
		histos[0].Scale(1.0)
		histos[0].SetLineColor(1)
		histos[0].Draw()
		histos[0].SetTitle(plotTitle + " " + label[i] + " Exclusive")
		histos[0].GetXaxis().SetTitle(XaxisTitle)
		histos[0].GetYaxis().SetTitle(YaxisTitle)
		histos[0].SetStats(stats)
		#histos[0].Write("histos{0}_{1}".format(i,inHisto))
		histos2[i].Scale(1.0)
		histos2[i].SetLineColor(2)
		histos2[i].Draw("same")
		histos2[i].Write("histo2{0}_{1}".format(i,inHisto))
		histos3[i].Scale(1.0)
		histos3[i].SetLineColor(4)
		histos3[i].Draw("same")
		histos3[i].Write("histo3{0}_{1}".format(i,inHisto))
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
	#histos2[0].Write("histos20")
	color = 1
	for i in range(len(histos2)):
		if(color == 5 or color == 10):
			color = color + 1
		histos2[i].SetLineColor(color)
		color = color + 1
		histos2[i].Scale(1.0)
		if(i == 0):
			histos2[i].Draw("")
			#histos2[i].Write("histos2{0}_{1}".format(i,inHisto))
			maximum = histos2[0].GetMaximum()
		else:
			histos2[i].Draw("same")
			#histos2[i].Write("histos2{0}_{1}".format(i,inHisto))
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
	del histos4


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

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

file = TFile(remainder[1])
events = file.Get("ntuple")

#if(useData):
#	datafile = open(remainder[1],"r")
#	dataFiles = []

#	for line in (raw.strip().split() for raw in datafile):
#		dataFiles.append(line[0])
#	dataevents = TChain("ntuple")
#	for i in range(len(dataFiles)):
#		dataevents.Add(dataFiles[i])

#if(useMC):
#	mcfile = open(remainder[1],"r")
#	mcFiles = []

#	for line in (raw.strip().split() for raw in mcfile):
#		mcFiles.append(line[0])
#	mcevents = TChain("ntuple")
#	for i in range(len(mcFiles)):
#		mcevents.Add(mcFiles[i])

#if(useAp):
#	apfile = open(remainder[1],"r")
#	apfiles = []
#	events = []
#	mass = []

#	for line in (raw.strip().split() for raw in apfile):
#		apfiles.append(TFile(line[0]))

#	for i in range(len(apfiles)):
#		events.append(apfiles[i].Get("ntuple"))
#		events[i].Draw("triM>>dummy({0},{1},{2})".format(1000,0,1))
#		dummy = ROOT.gROOT.FindObject("dummy")
#		mass.append(dummy.GetMean())
#		del dummy

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
	label.append("Track/Cluster Match Chisq < 10")
	label.append("Cluster Time Diff < 1.45 ns")
	label.append("Track/Cluster Time Diff < 4 ns")
	label.append("e- Momentum < 1.75 GeV")
	label.append("Track Chisq / dof < 6")
	label.append("Unconstrained Vertex Chisq < 10")
	label.append("e- and e+ Momentum > 0.4 GeV")
	label.append("e+ e- Momentum Sum < 2.4 GeV")

else:
	label.append("Preselection")

	dz = "0."
	if(useData):
		dz = "((-3.517-13.41*uncM+88.16*uncM^2-173.1*uncM^3)-(-3.14-27.2*uncM+144*uncM^2-257.1*uncM^3))"

	if(L1L2):
		x0_cut1_pos_x0 = -0.3187
		x1_cut1_pos_x0 = -0.9498

		x0_cut1_neg_x0 = -0.09418
		x1_cut1_neg_x0 = -0.7761

		x0_cut1_pos_x1 = 0.02095
		x1_cut1_pos_x1 = 0.05914

		x0_cut1_neg_x1 = 0.02016
		x1_cut1_neg_x1 = 0.05854

		eleisoL1 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
		posisoL1 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

		eleisoL2 = "eleMinPositiveIso+1/3.*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
		posisoL2 = "posMinPositiveIso+1/3.*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

		eleiso = "((eleHasL1&&{0})||(!eleHasL1&&{1}))".format(eleisoL1,eleisoL2)
		posiso = "((posHasL1&&{0})||(!posHasL1&&{1}))".format(posisoL1,posisoL2)

		z0cut = "((eleTrkZ0>((-0.204298550172+-0.819203072994*uncM)+(0.0215541584276+0.0769066743212*uncM)*(uncVZ+{0}))&&-posTrkZ0>((-0.0131964462788+-0.356152922206*uncM)+(0.0199952852357+0.0682704240163*uncM)*(uncVZ+{0})))||(posTrkZ0>((-0.204298550172+-0.819203072994*uncM)+(0.0215541584276+0.0769066743212*uncM)*(uncVZ+{0}))&&-eleTrkZ0>((-0.0131964462788+-0.356152922206*uncM)+(0.0199952852357+0.0682704240163*uncM)*(uncVZ+{0}))))".format(dz) #80%

		cuts.append("((!eleHasL1&&posHasL1)||(eleHasL1&&!posHasL1))&&eleHasL2&&posHasL2")
		label.append("e- (!L1 & L2) or e+ (!L1 & L2)")
		uncVXSig = 1.25 * uncVXSig
		uncVYSig = 1.5 * uncVYSig
		uncTargProjXSig = 1.25 * uncTargProjXSig
		uncTargProjYSig = 1.5 * uncTargProjYSig

	else:
		x0_cut1_pos_x0 = -0.2289
		x1_cut1_pos_x0 = -1.09

		x0_cut1_neg_x0 = -0.0009241
		x1_cut1_neg_x0 = -1.612

		x0_cut1_pos_x1 = 0.009205
		x1_cut1_pos_x1 = 0.2069

		x0_cut1_neg_x1 = 0.0091
		x1_cut1_neg_x1 = 0.2341

		eleiso = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
		posiso = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

		z0cut = "((eleTrkZ0>((-0.177913468428+-0.932330924205*uncM)+(0.00961915803124+0.228303547556*uncM)*(uncVZ+{0}))&&-posTrkZ0>((0.0115212779435+-0.651929048499*uncM)+(0.0125216209858+0.217752673675*uncM)*(uncVZ+{0})))||(posTrkZ0>((-0.177913468428+-0.932330924205*uncM)+(0.00961915803124+0.228303547556*uncM)*uncVZ)&&-eleTrkZ0>((0.0115212779435+-0.651929048499*uncM)+(0.0125216209858+0.217752673675*uncM)*(uncVZ+{0}))))".format(dz) #80%

		cuts.append("eleHasL1&&posHasL1&&eleHasL2&&posHasL2")
		label.append("e+e- L1 & L2")

	x0_cut1_pos = "({0}+{1}*uncM)".format(x0_cut1_pos_x0,x1_cut1_pos_x0)
	x1_cut1_pos = "({0}+{1}*uncM)".format(x0_cut1_pos_x1,x1_cut1_pos_x1)
	cut1_pos = "({0}+{1}*(uncVZ+{2}))".format(x0_cut1_pos,x1_cut1_pos,dz)

	x0_cut1_neg = "({0}+{1}*uncM)".format(x0_cut1_neg_x0,x1_cut1_neg_x0)
	x1_cut1_neg = "({0}+{1}*uncM)".format(x0_cut1_neg_x1,x1_cut1_neg_x1)
	cut1_neg = "({0}+{1}*(uncVZ+{2}))".format(x0_cut1_neg,x1_cut1_neg,dz)

	#z0cut = "((eleTrkZ0>{0}&&-posTrkZ0>{1})||(posTrkZ0>{0}&&-eleTrkZ0>{1}))".format(cut1_pos,cut1_neg)
	isocut = "({0}&&{1})".format(eleiso,posiso)

	cuts.append("sqrt((abs(uncVX-{0})/(3*{1}))^2+(abs(uncVY-{2})/(3*{3}))^2)<1".format(uncVX,uncVXSig,uncVY,uncVYSig))
	cuts.append("sqrt((abs((uncVX-(uncVZ-{4})*uncPX/uncPZ)-{0})/(2*{1}))^2+(abs((uncVY-(uncVZ-{4})*uncPY/uncPZ)-{2})/(2*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,zTarg))
	cuts.append("uncChisq<4")
	cuts.append("uncP>2.0")
	cuts.append(isocut)
	cuts.append(z0cut)

	label.append("V0 3 sigma")
	label.append("V0 Projection 2 sigma")
	label.append("Unconstrained Vertex Chisq < 4")
	label.append("V0 momentum > 2.0 GeV")
	label.append("Isolation Cut")
	label.append("Impact Parameter Cuts")

cut_all = ""


openPDF(outfile,c)

for i in range(len(plots)):
	plot = getPlot(plots[i])
	minimum = getMin(plots[i])
	maximum = getMax(plots[i])
	plotlabel = plotlabels[i]
	saveCutFlow(events,plot,cuts,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " {0}".format(Label),stats=0,logY=setlog[i])
	#if(useData):
	#	saveCutFlow(events,plot,cuts,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " Data",stats=0,logY=setlog[i])
	#if(useMC):
	#	saveCutFlow(events,plot,cuts,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " MC",stats=0,logY=setlog[i])
	#if(useAp):
		#for j in range(len(mass)):
			#saveCutFlow(events[j],plot,cuts,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ ' Ap {0:.0f} MeV'.format(mass[j]*1000),stats=0,logY=setlog[i])
	#	saveCutFlow(event,plot,cuts,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ ' Ap',stats=0,logY=setlog[i])

histo_cutflow = TH1F("histo_cutflow","histo_cutflow",len(cuts),0,len(cuts))

cut_all = ""

for i in range(len(cuts)):
	cut = cuts[i]
	if(i == 0):
		cut_all = cut
	else:
		cut_all = cut_all + "&&" + cut

for i in range(len(cuts)):
	if(i == 0):
		cut_tot = cuts[i]
	else:
		cut_tot = cut_tot + "&&" + cuts[i]
	n = getNEvents(events,cut_tot,i)
	print("Cut {0}: Entries {1}".format(label[i],n))
	histo_cutflow.SetBinContent(i+1,n)

histo_cutflow.Draw()
histo_cutflow.SetTitle("Cut Flow")
histo_cutflow.GetXaxis().SetTitle("Cut")
c.Print(outfile+".pdf")
histo_cutflow.Write("histo_cutflow")

closePDF(outfile,c)
outfileroot.Close()