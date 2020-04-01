import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TLatex
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

def saveCutFlow(events,inHisto,i,cuts_1,cut1,cut2,cut3,nBins,minX,maxX,label,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=1):
	events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histos{0}".format(i),nBins,minX,maxX),cuts_1)
	histo = ROOT.gROOT.FindObject("histos{0}".format(i))
	events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo2{0}".format(i),nBins,minX,maxX),cuts_1+"&&"+cut1)
	histo2 = ROOT.gROOT.FindObject("histo2{0}".format(i))
	events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo3{0}".format(i),nBins,minX,maxX),cuts_1+"&&"+cut2)
	histo3 = ROOT.gROOT.FindObject("histo3{0}".format(i))
	events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo4{0}".format(i),nBins,minX,maxX),cuts_1+"&&"+cut3)
	histo4 = ROOT.gROOT.FindObject("histo4{0}".format(i))
	events.Draw("uncVZ:uncM>>{0}({1},{2},{3},{1},{4},{5})".format("histo5{0}".format(i),nBins,0.,0.2,minX,maxX),cuts_1)
	histo5 = ROOT.gROOT.FindObject("histo5{0}".format(i))
	events.Draw("uncVZ:uncM>>{0}({1},{2},{3},{1},{4},{5})".format("histo6{0}".format(i),nBins,0.,0.2,minX,maxX),cuts_1+"&&"+cut1)
	histo6 = ROOT.gROOT.FindObject("histo6{0}".format(i))
	events.Draw("uncVZ:uncM>>{0}({1},{2},{3},{1},{4},{5})".format("histo7{0}".format(i),nBins,0.,0.2,minX,maxX),cuts_1+"&&"+cut2)
	histo7 = ROOT.gROOT.FindObject("histo7{0}".format(i))
	events.Draw("uncVZ:uncM>>{0}({1},{2},{3},{1},{4},{5})".format("histo8{0}".format(i),nBins,0.,0.2,minX,maxX),cuts_1+"&&"+cut3)
	histo8 = ROOT.gROOT.FindObject("histo8{0}".format(i))
	outfileroot.cd()

	label1 = label[3*i+2]
	label2 = label[3*i+3]
	label3 = label[3*i+4]

	canvas.SetLogy(1)
	canvas.SetLogz(1)
	histo.SetLineColor(1)
	histo.Draw()
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Write("histos{0}".format(i))
	histo2.SetLineColor(2)
	histo2.Draw("same")
	histo2.Write("histo2{0}".format(i))
	histo3.SetLineColor(4)
	histo3.Draw("same")
	histo3.Write("histo3{0}".format(i))
	histo4.SetLineColor(6)
	histo4.Draw("same")
	histo4.Write("histo4{0}".format(i))
	legend = TLegend(.08,.66,.42,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histo,"Without " + label1,"LP")
	legend.AddEntry(histo2,"{0}".format(label1),"LP")
	legend.AddEntry(histo3,"{0}".format(label2),"LP")
	legend.AddEntry(histo4,"{0}".format(label3),"LP")
	legend.Draw("same")
	canvas.Print(outfile+".pdf")
	canvas.Write()

	canvas.SetLogy(0)
	histo5.Draw("COLZ")
	histo5.SetTitle("Vz vs Mass " + label1 + " Exclusive")
	histo5.GetXaxis().SetTitle("Mass [GeV]")
	histo5.GetYaxis().SetTitle("Reconstructed z [mm]")
	histo5.SetStats(stats)
	canvas.Print(outfile+".pdf")
	canvas.Write()
	histo5.Write("histo5{0}".format(i))

	histo6.Draw("COLZ")
	histo6.SetTitle("Vz vs Mass " + label1)
	histo6.GetXaxis().SetTitle("Mass [GeV]")
	histo6.GetYaxis().SetTitle("Reconstructed z [mm]")
	histo6.SetStats(stats)
	canvas.Print(outfile+".pdf")
	canvas.Write()
	histo6.Write("histo6{0}".format(i))

	histo7.Draw("COLZ")
	histo7.SetTitle("Vz vs Mass " + label2)
	histo7.GetXaxis().SetTitle("Mass [GeV]")
	histo7.GetYaxis().SetTitle("Reconstructed z [mm]")
	histo7.SetStats(stats)
	canvas.Print(outfile+".pdf")
	canvas.Write()
	histo7.Write("histo7{0}".format(i))

	histo8.Draw("COLZ")
	histo8.SetTitle("Vz vs Mass " + label3)
	histo8.GetXaxis().SetTitle("Mass [GeV]")
	histo8.GetYaxis().SetTitle("Reconstructed z [mm]")
	histo8.SetStats(stats)
	canvas.Print(outfile+".pdf")
	canvas.Write()
	histo8.Write("histo8{0}".format(i))

	canvas.SetLogy(logY)

	del histo
	del histo2
	del histo3
	del histo4
	del histo5
	del histo6
	del histo7
	del histo8


def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")


outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

file = TFile(remainder[1])
events = file.Get("ntuple")

plot = "uncVZ"
plotlabel = "Reconstructed z [mm]"

dz = "0."
if(useData):
	dz = "((-3.517-13.41*uncM+88.16*uncM^2-173.1*uncM^3)-(-3.14-27.2*uncM+144*uncM^2-257.1*uncM^3))"


label = []
floatcuts = []
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
	label.append("Track/Cluster Match #chi{^2} < 10")
	label.append("Cluster Time Diff < 1.45 ns")
	label.append("Track/Cluster Time Diff < 4 ns")
	label.append("e- Momentum < 1.75 GeV")
	label.append("Track Chisq / dof < 6")
	label.append("Unconstrained Vertex #chi{^2} < 10")
	label.append("e- and e+ Momentum > 0.4 GeV")
	label.append("e+ e- Momentum Sum < 2.4 GeV")

else:
	label.append("Preselection")

	if(L1L2):
		x0_cut1_pos_x0 = -0.3187
		x1_cut1_pos_x0 = -0.9498

		x0_cut1_neg_x0 = -0.09418
		x1_cut1_neg_x0 = -0.7761

		x0_cut1_pos_x1 = 0.02095
		x1_cut1_pos_x1 = 0.05914

		x0_cut1_neg_x1 = 0.02016
		x1_cut1_neg_x1 = 0.05854

		eleisoL1_1 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-2.5*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
		posisoL1_1 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-2.5*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)
		eleisoL1_2 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
		posisoL1_2 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)
		eleisoL1_3 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3.5*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
		posisoL1_3 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3.5*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

		eleisoL2_1 = "eleMinPositiveIso+1/3.*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-2.5*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
		posisoL2_1 = "posMinPositiveIso+1/3.*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-2.5*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)
		eleisoL2_2 = "eleMinPositiveIso+1/3.*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
		posisoL2_2 = "posMinPositiveIso+1/3.*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)
		eleisoL2_3 = "eleMinPositiveIso+1/3.*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3.5*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
		posisoL2_3 = "posMinPositiveIso+1/3.*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3.5*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

		eleiso_1 = "((eleHasL1&&{0})||(!eleHasL1&&{1}))".format(eleisoL1_1,eleisoL2_1)
		posiso_1 = "((posHasL1&&{0})||(!posHasL1&&{1}))".format(posisoL1_1,posisoL2_1)
		eleiso_2 = "((eleHasL1&&{0})||(!eleHasL1&&{1}))".format(eleisoL1_2,eleisoL2_2)
		posiso_2 = "((posHasL1&&{0})||(!posHasL1&&{1}))".format(posisoL1_2,posisoL2_2)
		eleiso_3 = "((eleHasL1&&{0})||(!eleHasL1&&{1}))".format(eleisoL1_3,eleisoL2_3)
		posiso_3 = "((posHasL1&&{0})||(!posHasL1&&{1}))".format(posisoL1_3,posisoL2_3)

		z0cut2 = "((eleTrkZ0>((-0.204298550172+-0.819203072994*uncM)+(0.0215541584276+0.0769066743212*uncM)*(uncVZ+{0}))&&-posTrkZ0>((-0.0131964462788+-0.356152922206*uncM)+(0.0199952852357+0.0682704240163*uncM)*(uncVZ+{0})))||(posTrkZ0>((-0.204298550172+-0.819203072994*uncM)+(0.0215541584276+0.0769066743212*uncM)*(uncVZ+{0}))&&-eleTrkZ0>((-0.0131964462788+-0.356152922206*uncM)+(0.0199952852357+0.0682704240163*uncM)*(uncVZ+{0}))))".format(dz) #80%
		z0cut3 = "((eleTrkZ0>((-0.160212840296+-0.711401031858*uncM)+(0.0235892675119+0.0868362671156*uncM)*(uncVZ+{0}))&&-posTrkZ0>((0.0074583976511+-0.335278819542*uncM)+(0.0213379480119+0.0830900617137*uncM)*(uncVZ+{0})))||(posTrkZ0>((-0.160212840296+-0.711401031858*uncM)+(0.0235892675119+0.0868362671156*uncM)*(uncVZ+{0}))&&-eleTrkZ0>((0.0074583976511+-0.335278819542*uncM)+(0.0213379480119+0.0830900617137*uncM)*(uncVZ+{0}))))".format(dz) #70%

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

		eleiso_1 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-2.5*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
		posiso_1 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-2.5*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)
		eleiso_2 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
		posiso_2 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)
		eleiso_3 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3.5*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
		posiso_3 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3.5*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

		#z0cut2 = "((eleTrkZ0>{0}&&-posTrkZ0>{1})||(posTrkZ0>{0}&&-eleTrkZ0>{1}))".format(cut1_pos_2,cut1_neg_2)
		#z0cut3 = "((eleTrkZ0>{0}&&-posTrkZ0>{1})||(posTrkZ0>{0}&&-eleTrkZ0>{1}))".format(cut1_pos_3,cut1_neg_3)
		z0cut2 = "((eleTrkZ0>((-0.177913468428+-0.932330924205*uncM)+(0.00961915803124+0.228303547556*uncM)*(uncVZ+{0}))&&-posTrkZ0>((0.0115212779435+-0.651929048499*uncM)+(0.0125216209858+0.217752673675*uncM)*(uncVZ+{0})))||(posTrkZ0>((-0.177913468428+-0.932330924205*uncM)+(0.00961915803124+0.228303547556*uncM)*uncVZ)&&-eleTrkZ0>((0.0115212779435+-0.651929048499*uncM)+(0.0125216209858+0.217752673675*uncM)*(uncVZ+{0}))))".format(dz) #80%
		z0cut3 = "((eleTrkZ0>((-0.168325129572+-0.764572061732*uncM)+(0.0117844556696+0.238831014837*uncM)*(uncVZ+{0}))&&-posTrkZ0>((0.0144335686792+-0.576408853332*uncM)+(0.0158057745213+0.223434276362*uncM)*(uncVZ+{0})))||(posTrkZ0>((-0.168325129572+-0.764572061732*uncM)+(0.0117844556696+0.238831014837*uncM)*uncVZ)&&-eleTrkZ0>((0.0144335686792+-0.576408853332*uncM)+(0.0158057745213+0.223434276362*uncM)*(uncVZ+{0}))))".format(dz) #70%

		cuts.append("eleHasL1&&posHasL1&&eleHasL2&&posHasL2")
		label.append("e+e- L1 & L2")

	x0_cut1_pos = "({0}+{1}*uncM)".format(x0_cut1_pos_x0,x1_cut1_pos_x0)
	x1_cut1_pos = "({0}+{1}*uncM)".format(x0_cut1_pos_x1,x1_cut1_pos_x1)
	cut1_pos = "({0}+{1}*(uncVZ+{2}))".format(x0_cut1_pos,x1_cut1_pos,dz)

	x0_cut1_neg = "({0}+{1}*uncM)".format(x0_cut1_neg_x0,x1_cut1_neg_x0)
	x1_cut1_neg = "({0}+{1}*uncM)".format(x0_cut1_neg_x1,x1_cut1_neg_x1)
	cut1_neg = "({0}+{1}*(uncVZ+{2}))".format(x0_cut1_neg,x1_cut1_neg,dz)

	z0cut = "((eleTrkZ0>{0}&&-posTrkZ0>{1})||(posTrkZ0>{0}&&-eleTrkZ0>{1}))".format(cut1_pos,cut1_neg)
	isocut1 = "({0}&&{1})".format(eleiso_1,posiso_1)
	isocut2 = "({0}&&{1})".format(eleiso_2,posiso_2)
	isocut3 = "({0}&&{1})".format(eleiso_3,posiso_3)

	cuts.append("sqrt((abs((uncVX-(uncVZ-{4})*uncPX/uncPZ)-{0})/(2*{1}))^2+(abs((uncVY-(uncVZ-{4})*uncPY/uncPZ)-{2})/(2*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,zTarg))
	cuts.append("uncChisq<4")
	cuts.append("uncP>2.0")
	cuts.append(isocut2)
	cuts.append(z0cut2)

	label.append("V0 Projection 2#sigma")
	label.append("V0 Projection 1.5#sigma")
	label.append("V0 Projection 2.5#sigma")
	label.append("Unconstrained Vertex #chi{^2} < 4")
	label.append("Unconstrained Vertex #chi{^2} < 3")
	label.append("Unconstrained Vertex #chi{^2} < 5")
	label.append("V0 momentum > 2.0 GeV")
	label.append("V0 momentum > 1.9 GeV")
	label.append("V0 momentum > 2.1 GeV")
	label.append("Isolation Cut 3#sigma")
	label.append("Isolation Cut 2.5#sigma")
	label.append("Isolation Cut 3.5#sigma")
	label.append("Impact Parameter Cuts #alpha = 10%")
	label.append("Impact Parameter Cuts #alpha = 5%")
	label.append("Impact Parameter Cuts #alpha = 20%")

	#cut1_pos_2 = "({0}+{1}*(uncVZ+{2}))+0.1".format(x0_cut1_pos,x1_cut1_pos,dz)
	#cut1_neg_2 = "({0}+{1}*(uncVZ+{2}))+0.1".format(x0_cut1_neg,x1_cut1_neg,dz)
	#cut1_pos_3 = "({0}+{1}*(uncVZ+{2}))+0.2".format(x0_cut1_pos,x1_cut1_pos,dz)
	#cut1_neg_3 = "({0}+{1}*(uncVZ+{2}))+0.2".format(x0_cut1_neg,x1_cut1_neg,dz)

	floatcuts.append("sqrt((abs((uncVX-(uncVZ-{4})*uncPX/uncPZ)-{0})/(1.5*{1}))^2+(abs((uncVY-(uncVZ-{4})*uncPY/uncPZ)-{2})/(1.5*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,zTarg))
	floatcuts.append("sqrt((abs((uncVX-(uncVZ-{4})*uncPX/uncPZ)-{0})/(2.5*{1}))^2+(abs((uncVY-(uncVZ-{4})*uncPY/uncPZ)-{2})/(2.5*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,zTarg))
	floatcuts.append("uncChisq<3")
	floatcuts.append("uncChisq<5")
	floatcuts.append("uncP>1.9")
	floatcuts.append("uncP>2.1")
	floatcuts.append(isocut1)
	floatcuts.append(isocut3)
	floatcuts.append(z0cut)
	floatcuts.append(z0cut3)

cuts_1_arr = []
for i in range(len(cuts)):
	cut = cuts[i]
	if(i == 0):
		cuts_1 = cut
	else:
		cuts_1 = ""
		for j in range(len(cuts)):
			if(j != i):
				if(cuts_1 != ""):
					cuts_1 = cuts_1 + "&&" + cuts[j]
				else:
					cuts_1 = cuts[j]
		cuts_1_arr.append(cuts_1)

openPDF(outfile,c)

for i in range(len(cuts)-2):
	cuts_1 = cuts_1_arr[i+1]
	cut1 = cuts[i+2]
	cut2 = floatcuts[2*i]
	cut3 = floatcuts[2*i+1]
	saveCutFlow(events,plot,i,cuts_1,cut1,cut2,cut3,nBins,minVZ,maxVZ,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " {0}".format(Label),stats=0)

closePDF(outfile,c)
outfileroot.Close()

print(z0cut)