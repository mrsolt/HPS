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
    print '\t-o: uncTargProjX mean (default 0)'
    print '\t-p: uncTargProjX sigma (default 9999)'
    print '\t-a: uncTargProjY mean (default 0)'
    print '\t-b: uncTargProjY sigma (default 9999)'
    print '\t-r: is L1L2 category (default false)'
    print '\t-y: plot label'
    print '\t-d: use data file (default False)'
    print '\t-w: make cutflow plots (default False)'
    print '\t-x: output new root tree (default False)'
    print '\t-h: this help message'
    print

zTarg = -4.3
ebeam = 2.3
minVZ = -60
maxVZ = 80
nBins = 140
useData = False
L1L2 = False
makeCutflow = False
makeNewTree = False
clusterT = 56
uncTargProjX = 0.
uncTargProjXSig = 9999.
uncTargProjY = 0.
uncTargProjYSig = 9999.
Label = ""

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:g:i:e:q:t:o:p:a:b:y:rdwx')

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
			Label=str(arg)
		if opt=='-r':
			L1L2 = True
		if opt=='-d':
			useData = True
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
	color = 1
	for i in range(len(histos2)):
		if(color == 5 or color == 10):
			color = color + 1
		histos2[i].SetLineColor(color)
		color = color + 1
		histos2[i].Scale(1.0)
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

file = TFile(remainder[1])
events = file.Get("ntuple")

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

#cuts.append("isPair1")
#cuts.append("eleMatchChisq<10&&posMatchChisq<10")
#cuts.append("abs(eleClT-posClT)<1.45")
#cuts.append("abs(eleClT-eleTrkT-{0})<4&&abs(posClT-posTrkT-{0})<4".format(clusterT))
#cuts.append("eleP<1.75")
#cuts.append("eleTrkChisq/(2*eleNTrackHits-5)<6&&posTrkChisq/(2*posNTrackHits-5)<6")
#cuts.append("uncChisq<10")
#cuts.append("eleP>0.4&&posP>0.4")
#cuts.append("uncP<2.4")

#label.append("Preprocessing")
#label.append("Pair1 Trigger")
#label.append("Track/Cluster Match Sigma < 10")
#label.append("Cluster Time Diff < 1.45 ns")
#label.append("Track/Cluster Time Diff < 4 ns")
#label.append("e- Momentum < 1.75 GeV")
#label.append("Track Chisq / dof < 6")
#label.append("Unconstrained Vertex Chisq < 10")
#label.append("e- and e+ Momentum > 0.4 GeV")
#label.append("e+ e- Momentum Sum < 2.4 GeV")

label.append("Preselection")

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

if(L1L2):
	a0 = -0.204298550172
	a1 = -0.819203072994
	a2 = 0.0215541584276
	a3 = 0.0769066743212
	b0 = -0.0131964462788
	b1 = -0.356152922206
	b2 = 0.0199952852357
	b3 = 0.0682704240163

	eleisoL1 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
	posisoL1 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

	eleisoL2 = "eleMinPositiveIso+1/3.*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
	posisoL2 = "posMinPositiveIso+1/3.*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

	eleiso = "((eleHasL1&&{0})||(!eleHasL1&&{1}))".format(eleisoL1,eleisoL2)
	posiso = "((posHasL1&&{0})||(!posHasL1&&{1}))".format(posisoL1,posisoL2)

	cuts.append("((!eleHasL1&&posHasL1)||(eleHasL1&&!posHasL1))&&eleHasL2&&posHasL2")
	label.append("Layer Requirement")

	uncTargProjXSig = 1.25 * uncTargProjXSig
	uncTargProjYSig = 1.5 * uncTargProjYSig

else:
	a0 = -0.177913468428
	a1 = -0.932330924205
	a2 = 0.00961915803124
	a3 = 0.228303547556
	b0 = 0.0115212779435
	b1 = -0.651929048499
	b2 = 0.0125216209858
	b3 = 0.217752673675

	eleiso = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
	posiso = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

	#z0cut = "((eleTrkZ0>((-0.177913468428+-0.932330924205*uncM)+(0.00961915803124+0.228303547556*uncM)*(uncVZ+{0}))&&-posTrkZ0>((0.0115212779435+-0.651929048499*uncM)+(0.0125216209858+0.217752673675*uncM)*(uncVZ+{0})))||(posTrkZ0>((-0.177913468428+-0.932330924205*uncM)+(0.00961915803124+0.228303547556*uncM)*uncVZ)&&-eleTrkZ0>((0.0115212779435+-0.651929048499*uncM)+(0.0125216209858+0.217752673675*uncM)*(uncVZ+{0}))))".format(dz) #80%

	cuts.append("eleHasL1&&posHasL1&&eleHasL2&&posHasL2")
	label.append("e+e- Layer Requirement")

isocut = "({0}&&{1})".format(eleiso,posiso)

eleZ0_up = "(eleTrkZ0>{0}+{1}*uncM+{2}*(uncVZ+{4})+{3}*uncM*(uncVZ+{4}))".format(a0,a1,a2,a3,dz)
posZ0_up = "(posTrkZ0>{0}+{1}*uncM+{2}*(uncVZ+{4})+{3}*uncM*(uncVZ+{4}))".format(a0,a1,a2,a3,dz)

eleZ0_down = "(-eleTrkZ0>{0}+{1}*uncM+{2}*(uncVZ+{4})+{3}*uncM*(uncVZ+{4}))".format(b0,b1,b2,b3,dz)
posZ0_down = "(-posTrkZ0>{0}+{1}*uncM+{2}*(uncVZ+{4})+{3}*uncM*(uncVZ+{4}))".format(b0,b1,b2,b3,dz)

z0cut = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up,posZ0_down,posZ0_up,eleZ0_down)

cuts.append("sqrt((abs((uncVX-(uncVZ-{4})*uncPX/uncPZ)-{0})/(2*{1}))^2+(abs((uncVY-(uncVZ-{4})*uncPY/uncPZ)-{2})/(2*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,zTarg))
cuts.append("uncChisq<4")
cuts.append("uncP>2.0")
cuts.append(isocut)
cuts.append(z0cut)

label.append("V0 Projection 2 sigma")
label.append("Unconstrained Vertex Chisq < 4")
label.append("V0 momentum > 2.0 GeV")
label.append("Isolation Cut")
label.append("Impact Parameter Cuts")

cut_all = ""

for i in range(len(cuts)):
	cut = cuts[i]
	if(i == 0):
		cut_all = cut
	else:
		cut_all = cut_all + "&&" + cut

if(makeCutflow):
	outfile = remainder[0]+"_cutflow"
	outfileroot = TFile(remainder[0]+"_cutlfow.root","RECREATE")

	openPDF(outfile,c)

	for i in range(len(plots)):
		plot = getPlot(plots[i])
		minimum = getMin(plots[i])
		maximum = getMax(plots[i])
		plotlabel = plotlabels[i]
		saveCutFlow(events,plot,cuts,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " {0}".format(Label),stats=0,logY=setlog[i])

	histo_cutflow = TH1F("histo_cutflow","histo_cutflow",len(cuts),0,len(cuts))

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

if(makeNewTree):
	print (events.GetEntries())
	print (cut_all)
	outFile = TFile(remainder[0]+".root","RECREATE")
	events_new = events.CopyTree(cut_all)
	print (events_new.GetEntries())
	events_new.Write("ntuple",TTree.kOverwrite)
	gDirectory.ls()
