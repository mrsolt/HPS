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
	print '\t-o: uncTargProjX mean (default 0)'
	print '\t-p: uncTargProjX sigma (default 9999)'
	print '\t-a: uncTargProjY mean (default 0)'
	print '\t-b: uncTargProjY sigma (default 9999)'
	print '\t-r: is L1L2 category (default false)'
	print '\t-s: is L2L2 category (default false)'
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
L2L2 = False
makeCutflow = False
makeNewTree = False
clusterT = 56
uncTargProjX = 0.
uncTargProjXSig = 9999.
uncTargProjY = 0.
uncTargProjYSig = 9999.
Label = ""

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:g:i:e:q:t:o:p:a:b:y:rsdwx')

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
		if opt=='-s':
			L2L2 = True
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
		if(inHisto == "uncVZ"):
			plotHisto = "{0}+{1}".format(inHisto,dz)
		else:
			plotHisto = inHisto
		events.Draw("{0}>>{1}({2},{3},{4})".format(plotHisto,"histos{0}_{1}".format(i,inHisto),nBins,minX,maxX),cut_tot)
		histos.append(ROOT.gROOT.FindObject("histos{0}_{1}".format(i,inHisto)))
		events.Draw("{0}>>{1}({2},{3},{4})".format(plotHisto,"histo2{0}_{1}".format(i,inHisto),nBins,minX,maxX),cuts_1)
		histos2.append(ROOT.gROOT.FindObject("histo2{0}_{1}".format(i,inHisto)))
		events.Draw("{0}>>{1}({2},{3},{4})".format(plotHisto,"histo3{0}_{1}".format(i,inHisto),nBins,minX,maxX),cuts_1+"&&"+cuts[i])
		histos3.append(ROOT.gROOT.FindObject("histo3{0}_{1}".format(i,inHisto)))
		if(inHisto == "uncVZ"):
			events.Draw("uncVZ:uncM>>{0}({1},{2},{3},{1},{4},{5})".format("histo4{0}_{1}".format(i,inHisto),nBins,0.,0.2,-30,30),cuts_1)
			histos4.append(ROOT.gROOT.FindObject("histo4{0}_{1}".format(i,inHisto)))

	outfileroot.cd()
	if(inHisto == "uncVZ"):
		events.Draw("uncVZ:uncM>>{0}({1},{2},{3},{1},{4},{5})".format("histo_2D",nBins,0.,0.2,-30,30),cut_tot)
		histo_2D = ROOT.gROOT.FindObject("histo_2D")
		canvas.SetLogz(1)
		canvas.SetLogy(0)
		histo_2D.Draw("COLZ")
		histo_2D.SetTitle("Vz vs Mass All Cuts")
		histo_2D.GetXaxis().SetTitle("Mass [GeV]")
		histo_2D.GetYaxis().SetTitle("Reconstructed z [mm]")
		histo_2D.SetStats(stats)
		histo_2D.GetXaxis().SetLabelSize(0.05)
		histo_2D.GetYaxis().SetLabelSize(0.05)
		#histo_2D.GetZaxis().SetLabelSize(0.05)
		histo_2D.GetXaxis().SetTitleOffset(0.8)
		histo_2D.GetXaxis().SetTitleSize(0.06)
		histo_2D.GetYaxis().SetTitleOffset(0.8)
		histo_2D.GetYaxis().SetTitleSize(0.06)
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
		histos4[i].GetXaxis().SetLabelSize(0.05)
		histos4[i].GetYaxis().SetLabelSize(0.05)
		#histos4[i].GetZaxis().SetLabelSize(0.05)
		histos4[i].GetXaxis().SetTitleOffset(0.8)
		histos4[i].GetXaxis().SetTitleSize(0.06)
		histos4[i].GetYaxis().SetTitleOffset(0.8)
		histos4[i].GetYaxis().SetTitleSize(0.06)
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
		histos[i].Sumw2()
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
		histos[0].GetXaxis().SetLabelSize(0.05)
		histos[0].GetYaxis().SetLabelSize(0.05)
		#histos[0].GetZaxis().SetLabelSize(0.05)
		histos[0].GetXaxis().SetTitleOffset(0.8)
		histos[0].GetXaxis().SetTitleSize(0.06)
		histos[0].GetYaxis().SetTitleOffset(0.8)
		histos[0].GetYaxis().SetTitleSize(0.06)
		histos[0].SetStats(stats)
		histos2[i].Sumw2()
		histos2[i].SetLineColor(2)
		histos2[i].Draw("same")
		histos2[i].Write("histo2{0}_{1}".format(i,inHisto))
		histos3[i].Sumw2()
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
		legend3.SetTextSize(0.05)
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
	del histos4

def saveCuts(events,i,cut_1,nBins,minX,maxX,label,var,outfile,canvas,XaxisTitle="",YaxisTitle="",stats=0,logY=0):
	events.Draw("{0}>>{1}({2},{3},{4})".format(var,"histo5{0}".format(i),nBins,minX,maxX),cut_1)
	histo5 = ROOT.gROOT.FindObject("histo5{0}".format(i))
	canvas.SetLogy(logY)
	histo5.Sumw2()
	histo5.Draw()
	histo5.SetTitle(label + " Exclusive")
	histo5.GetXaxis().SetTitle(XaxisTitle)
	histo5.GetYaxis().SetTitle(YaxisTitle)
	histo5.GetXaxis().SetLabelSize(0.05)
	histo5.GetYaxis().SetLabelSize(0.05)
	#histo5.GetZaxis().SetLabelSize(0.05)
	histo5.GetXaxis().SetTitleOffset(0.8)
	histo5.GetXaxis().SetTitleSize(0.06)
	histo5.GetYaxis().SetTitleOffset(0.8)
	histo5.GetYaxis().SetTitleSize(0.06)
	histo5.SetStats(stats)
	canvas.Print(outfile+".pdf")
	canvas.Write()
	histo5.Write("histo5{0}".format(i))
	del histo5

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

label = []
cuts = []
var = []
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

dy = uncTargProjY - (-0.0668941015569)
dz = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3".format(c0,c1,c2,c3)

if(L2L2):
	mpos = -0.576619997051
	mneg = -0.0126688170132
	m0 = -0.126973432435
	a0 = 0.0628788048688
	a1 = -0.00317833175061
	b0 = 0.0614724292851
	b1 = -0.00358273636968


	#eleisoL1 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
	#posisoL1 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

	eleisoL2 = "eleMinPositiveIsoL2+1/3.*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
	posisoL2 = "posMinPositiveIsoL2+1/3.*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

	eleiso = "({0})".format(eleisoL2)
	posiso = "({0})".format(posisoL2)

	cuts.append("(!eleHasL1&&!posHasL1&&eleHasL2&&posHasL2)")
	var.append("((!eleHasL1*posHasL1)+(eleHasL1*!posHasL1))*eleHasL2*posHasL2 -1 2")
	label.append("Layer Requirement")

	uncTargProjXSig = 1.9 * uncTargProjXSig
	uncTargProjYSig = 2.5 * uncTargProjYSig

elif(L1L2):
	#a0 = -0.204298550172
	#a1 = -0.819203072994
	#a2 = 0.0215541584276
	#a3 = 0.0769066743212
	#b0 = -0.0131964462788
	#b1 = -0.356152922206
	#b2 = 0.0199952852357
	#b3 = 0.0682704240163

	m0 = -0.167438502208
	a0 = 0.016762652862
	a1 = 0.00033162637213
	b0 = 0.0207347770085
	b1 = 0.000331699098944

	eleisoL1 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
	posisoL1 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

	eleisoL2 = "eleMinPositiveIsoL2+1/3.*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
	posisoL2 = "posMinPositiveIsoL2+1/3.*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

	eleiso = "((eleHasL1&&{0})||(!eleHasL1&&{1}))".format(eleisoL1,eleisoL2)
	posiso = "((posHasL1&&{0})||(!posHasL1&&{1}))".format(posisoL1,posisoL2)

	cuts.append("((!eleHasL1&&posHasL1)||(eleHasL1&&!posHasL1))&&eleHasL2&&posHasL2")
	var.append("((!eleHasL1*posHasL1)+(eleHasL1*!posHasL1))*eleHasL2*posHasL2 -1 2")
	label.append("Layer Requirement")

	uncTargProjXSig = 1.25 * uncTargProjXSig
	uncTargProjYSig = 1.5 * uncTargProjYSig

else:
	#a0 = -0.177913468428
	#a1 = -0.932330924205
	#a2 = 0.00961915803124
	#a3 = 0.228303547556
	#b0 = 0.0115212779435
	#b1 = -0.651929048499
	#b2 = 0.0125216209858
	#b3 = 0.217752673675

	m0 = -0.201776054859
	a0 = 0.0518988558564
	a1 = -0.00230111045957
	b0 = 0.0471576968062
	b1 = -0.00108639651791

	eleiso = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
	posiso = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

	#z0cut = "((eleTrkZ0>((-0.177913468428+-0.932330924205*uncM)+(0.00961915803124+0.228303547556*uncM)*(uncVZ+{0}))&&-posTrkZ0>((0.0115212779435+-0.651929048499*uncM)+(0.0125216209858+0.217752673675*uncM)*(uncVZ+{0})))||(posTrkZ0>((-0.177913468428+-0.932330924205*uncM)+(0.00961915803124+0.228303547556*uncM)*uncVZ)&&-eleTrkZ0>((0.0115212779435+-0.651929048499*uncM)+(0.0125216209858+0.217752673675*uncM)*(uncVZ+{0}))))".format(dz) #80%

	cuts.append("eleHasL1&&posHasL1&&eleHasL2&&posHasL2")
	var.append("eleHasL1*posHasL1*eleHasL2*posHasL2 -1 2")
	label.append("e+e- Layer Requirement")

isocut = "({0}&&{1})".format(eleiso,posiso)

#eleZ0_up = "(eleTrkZ0>{0}+{1}*uncM+{2}*(uncVZ+{4})+{3}*uncM*(uncVZ+{4}))".format(a0,a1,a2,a3,dz)
#posZ0_up = "(posTrkZ0>{0}+{1}*uncM+{2}*(uncVZ+{4})+{3}*uncM*(uncVZ+{4}))".format(a0,a1,a2,a3,dz)

#eleZ0_down = "(-eleTrkZ0>{0}+{1}*uncM+{2}*(uncVZ+{4})+{3}*uncM*(uncVZ+{4}))".format(b0,b1,b2,b3,dz)
#posZ0_down = "(-posTrkZ0>{0}+{1}*uncM+{2}*(uncVZ+{4})+{3}*uncM*(uncVZ+{4}))".format(b0,b1,b2,b3,dz)

if(L2L2):
	m0 = mpos

eleZ0_up = "(eleTrkZ0>{0}+{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,a0,a1,dz,dy)
posZ0_up = "(posTrkZ0>{0}+{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,a0,a1,dz,dy)

if(L2L2):
	m0 = mneg

eleZ0_down = "(-eleTrkZ0>{0}-{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,b0,b1,dz,dy)
posZ0_down = "(-posTrkZ0>{0}-{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,b0,b1,dz,dy)

z0cut = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up,posZ0_down,posZ0_up,eleZ0_down)

#cuts.append("sqrt((abs((uncVX-(uncVZ-{4})*uncPX/uncPZ)-{0})/(2*{1}))^2+(abs((uncVY-(uncVZ-{4})*uncPY/uncPZ)-{2})/(2*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,zTarg))
cuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,nSig))
#cuts.append("uncChisq<4")
cuts.append("uncP<9999")
cuts.append("uncP>1.85")
cuts.append(isocut)
cuts.append(z0cut)

label.append("V0 Projection 2#sigma")
label.append("Unconstrained Vertex #chi^{2} < 4")
label.append("V0 momentum > 1.85 GeV")
label.append("Isolation Cut")
label.append("Impact Parameter Cuts")

#var.append("sqrt((abs((uncVX-(uncVZ-{4})*uncPX/uncPZ)-{0})/(2*{1}))^2+(abs((uncVY-(uncVZ-{4})*uncPY/uncPZ)-{2})/(2*{3}))^2) 0 2".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,zTarg))
var.append("sqrt((({4}-{0})/({1}))^2+(({5}-{2})/({3}))^2) 0 2".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot))
var.append("uncChisq 0 10")
var.append("uncP 0 2.4")
var.append("eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega))) -3 7".format(zTarg))
var.append("posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega))) -3 7".format(zTarg))
var.append("eleTrkZ0 -3 3")
var.append("posTrkZ0 -3 3")

xlabel = []
xlabel.append("Passes Layer Requirement")
xlabel.append("V0 Projection to Target N#sigma")
xlabel.append("Unconstrainced #chi^{2}")
xlabel.append("V0 Momentum (GeV)")
xlabel.append("Electron Isolation Cut Value (mm)")
xlabel.append("Positron Isolation Cut Value (mm)")
xlabel.append("Electron Track Z0 (mm)")
xlabel.append("Positron Track Z0 (mm)")

index = []
index.append(1)
index.append(2)
index.append(3)
index.append(4)
index.append(5)
index.append(5)
index.append(6)
index.append(6)

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
		saveCutFlow(events,plot,cuts,nBins,minimum,maximum,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " {0}".format(Label),stats=0,logY=setlog[i])

	for i in range(len(var)):
		plot = getPlot(var[i])
		minimum = getMin(var[i])
		maximum = getMax(var[i])
		cut_1 = ""
		cut = cuts[index[i]]
		for j in range(len(cuts)):
			if(j != index[i]):
				if(cut_1 != ""):
					cut_1 = cut_1 + "&&" + cuts[j]
				else:
					cut_1 = cuts[j]
		saveCuts(events,i,cut_1,nBins,minimum,maximum,label[index[i]],plot,outfile,c,XaxisTitle=xlabel[i],logY=1)

	histo_cutflow = TH1F("histo_cutflow","histo_cutflow",len(cuts),0,len(cuts))

	for i in range(len(cuts)):
		if(i == 0):
			cut_tot = cuts[i]
		else:
			cut_tot = cut_tot + "&&" + cuts[i]
		n = getNEvents(events,cut_tot,i)
		print("Cut {0}: Entries {1}".format(label[i],n))
		histo_cutflow.SetBinContent(i+1,n)

	histo_cutflow.Sumw2()
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
