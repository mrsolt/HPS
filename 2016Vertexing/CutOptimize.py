import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import math
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TLatex, TF1
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input text Data file> <input text MC file> <input text A' files>".format(sys.argv[0])
    print 'Note: Even when not using a data, MC, or Ap file, you must feed a dummy text file'
    print "Arguments: "
    print '\t-z: target position (default -4.3 mm)'
    print '\t-g: minimum uncVZ (default 0 mm)'
    print '\t-i: maximum uncVZ (default 50 mm)'
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
    print '\t-j: use Ap (default False)'
    print '\t-k: do uncChisq (default False)'
    print '\t-m: do V0 Proj (default False)'
    print '\t-n: do IP Cut (default False)'
    print '\t-c: is 80 MeV Ap (default False)'
    print '\t-f: is 100 MeV ap (default False)'
    print '\t-h: this help message'
    print

zTarg = -4.3
ebeam = 2.3
minVZ = 0
maxVZ = 50
nBins = 50
L1L2 = False
useData = False
useAp = False
doUncChisq = False
doV0Proj = False
doIP = False
is80 = False
is100 = False
clusterT = 56
uncTargProjX = 0.
uncTargProjXSig = 9999.
uncTargProjY = 0.
uncTargProjYSig = 9999.
Label = ""

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:g:i:e:q:t:jkmncfo:p:a:b:y:rd')

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
		if opt=='-j':
			useAp = True
		if opt=='-k':
			doUncChisq = True
		if opt=='-m':
			doV0Proj = True
		if opt=='-n':
			doIP = True
		if opt=='-c':
			is80 = True
		if opt=='-f':
			is100 = True
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

radfracf = TF1("radfracf","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(0.2018,-2.342,12.86,25.88,-405.8,898.6),0.04,0.2)
num_pairsf = TF1("num_pairsf","exp({0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5)".format(4.903,208.3,-1880,-1868,68700,-198000),0.04,0.2)

def saveCutFlow(events,eventstruth,useAp,is80,is100,inHisto,cuts,floatcuts,nBins,minX,maxX,label,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	outfileroot.cd()
	exppol1=TF1("exppol1","exp(pol1(0))",-5,100)
	histos = []
	histos2 = []
	color = 0
	for i in range(len(floatcuts)):
		cutstot = "{0}&&{1}".format(cuts,floatcuts[i])
		events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo{0}".format(i),nBins,minX,maxX),cutstot)
		histos.append(ROOT.gROOT.FindObject("histo{0}".format(i)))
		histos[i].Sumw2()
		if(useAp):
			events.Draw("{0}>>{1}({2},{3},{4})".format("triEndZ","histo2{0}".format(i),nBins,minX,maxX),cutstot)
			histos2.append(ROOT.gROOT.FindObject("histo2{0}".format(i)))
			histos2[i].Sumw2()
	if(useAp):
		eventstruth.Draw("{0}>>{1}({2},{3},{4})".format("triEndZ","histotruth",nBins,minX,maxX))
		histostruth = ROOT.gROOT.FindObject("histotruth")
		histostruth.Sumw2()

	legend = TLegend(.58,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)

	histointegral = TH1F("histointegral","histointegral",len(floatcuts),0,len(floatcuts))

	for i in range(len(histos)):
		color = color + 1
		if(i == 0):
			histos[i].SetLineColor(color)
			histos[i].SetTitle(plotTitle)
			histos[i].GetXaxis().SetTitle(XaxisTitle)
			histos[i].GetYaxis().SetTitle(YaxisTitle)
			histos[i].SetStats(stats)
			histos[i].Draw()
		else:
			if(color == 5 or color == 10):
				color = color + 1
			histos[i].SetLineColor(color)
			histos[i].Draw("same")
		histos[i].Write("histo{0}".format(i))
		legend.AddEntry(histos[i],label[i],"LP")
		if(useAp):
			deltaM = 0.001
			if(is80):
				mass = 0.080
				eps = 3e-9
				num_rad = radfracf.Eval(mass)*num_pairsf.Eval(mass)
				norm = 0.04
			elif(is100):
				mass = 0.100
				eps = 2e-9
				num_rad = radfracf.Eval(mass)*num_pairsf.Eval(mass)
				norm = 0.14
			else:
				num_rad = 0
				mass = -9999
				eps = -9999
				norm = 1.0
			ap_yield= 3*math.pi/(2*(1/137.0))*num_rad*(mass/deltaM)
			hbar_c = 1.973e-13
			gamma = 0.965
			gammact = hbar_c*3.0*2.3*gamma/(mass*mass*(1/137.036)*eps)
			exppol1.SetParameters(zTarg/gammact-math.log(gammact),-1.0/gammact)
			histos2[i].Divide(histostruth)
			histos2[i].Scale(ap_yield*eps/norm)
			for j in range(histos2[i].GetNbinsX()):
				sig_bin = histos2[i].GetBinContent(j+1) * exppol1.Eval(histos2[i].GetBinCenter(j+1))
				histos2[i].SetBinContent(j+1,sig_bin)
			print("{0} Number of Events: {1}".format(label[i],histos2[i].Integral()))
			histointegral.SetBinContent(i+1,histos2[i].Integral())
		else:
			print("{0} Number of Events: {1}".format(label[i],histos[i].Integral()))
			histointegral.SetBinContent(i+1,histos[i].Integral())

	legend.Draw()
	canvas.Print(outfile+".pdf")
	canvas.Write()
	histointegral.SetTitle(Label)
	histointegral.GetXaxis().SetTitle("Cut Number")
	histointegral.Draw()
	canvas.Print(outfile+".pdf")
	histointegral.Write("Integral")

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")


outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

file = TFile(remainder[1])
events = file.Get("ntuple")

file2 = TFile(remainder[2])
eventstruth = file2.Get("ntuple")

plot = "uncVZ"
plotlabel = "Reconstructed z [mm]"

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

dz = "0."
if(useData):
	dz = "((-3.517-13.41*uncM+88.16*uncM^2-173.1*uncM^3)-(-3.14-27.2*uncM+144*uncM^2-257.1*uncM^3))"
dy = uncTargProjY - (-0.0668941015569)

label = []
floatcuts = []
nominal = []
cuts = []

if(L1L2):
	eleisoL1 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3.0*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
	posisoL1 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3.0*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

	eleisoL2 = "eleMinPositiveIso+1/3.*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3.0*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
	posisoL2 = "posMinPositiveIso+1/3.*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3.0*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

	eleiso = "((eleHasL1&&{0})||(!eleHasL1&&{1}))".format(eleisoL1,eleisoL2)
	posiso = "((posHasL1&&{0})||(!posHasL1&&{1}))".format(posisoL1,posisoL2)

	m0_1 = -0.144047348514
	a0_1 = 0.00744446817538
	a1_1 = 0.000733701536088
	b0_1 = 0.00396086083746
	b1_1 = 0.00141551321138

	m0_2 = -0.167438502208
	a0_2 = 0.016762652862
	a1_2 = 0.00033162637213
	b0_2 = 0.0207347770085
	b1_2 = 0.000331699098944

	m0_3 = -0.165901413074
	a0_3 = 0.0224285926089
	a1_3 = 9.77428404087e-05
	b0_3 = 0.0266646866578
	b1_3 = -1.95809258016e-05

	m0_4 = -0.159878338859
	a0_4 = 0.0239443819303
	a1_4 = 0.000252995988727
	b0_4 = 0.0306980650011
	b1_4 = -0.000292916678252

	cuts.append("((!eleHasL1&&posHasL1)||(eleHasL1&&!posHasL1))&&eleHasL2&&posHasL2")
	uncTargProjXSig = 1.25 * uncTargProjXSig
	uncTargProjYSig = 1.5 * uncTargProjYSig

else:
	eleiso = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3.0*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
	posiso = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3.0*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

	m0_1 = -0.220979312259
	a0_1 = 0.0454134504877
	a1_1 = -0.00194343184899
	b0_1 = 0.0448779386535
	b1_1 = -0.000904925763122

	m0_2 = -0.201776054859
	a0_2 = 0.0518988558564
	a1_2 = -0.00230111045957
	b0_2 = 0.0471576968062
	b1_2 = -0.00108639651791

	m0_3 = -0.182785054865
	a0_3 = 0.0548318052232
	a1_3 = -0.00237467958982
	b0_3 = 0.0510079099013
	b1_3 = -0.00139764921133

	m0_4 = -0.170362502498
	a0_4 = 0.0577161789952
	a1_4 = -0.00248138234665
	b0_4 = 0.0544000489688
	b1_4 = -0.00163132278653

	cuts.append("eleHasL1&&posHasL1&&eleHasL2&&posHasL2")

isocut = "({0}&&{1})".format(eleiso,posiso)

eleZ0_up1 = "(eleTrkZ0>{0}+{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_1,a0_1,a1_1,dz,dy)
posZ0_up1 = "(posTrkZ0>{0}+{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_1,a0_1,a1_1,dz,dy)
eleZ0_down1 = "(-eleTrkZ0>{0}-{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_1,b0_1,b1_1,dz,dy)
posZ0_down1 = "(-posTrkZ0>{0}-{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_1,b0_1,b1_1,dz,dy)
z0cut1 = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up1,posZ0_down1,posZ0_up1,eleZ0_down1)

eleZ0_up2 = "(eleTrkZ0>{0}+{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_2,a0_2,a1_2,dz,dy)
posZ0_up2 = "(posTrkZ0>{0}+{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_2,a0_2,a1_2,dz,dy)
eleZ0_down2 = "(-eleTrkZ0>{0}-{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_2,b0_2,b1_2,dz,dy)
posZ0_down2 = "(-posTrkZ0>{0}-{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_2,b0_2,b1_2,dz,dy)
z0cut2 = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up2,posZ0_down2,posZ0_up2,eleZ0_down2)

eleZ0_up3 = "(eleTrkZ0>{0}+{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_3,a0_3,a1_3,dz,dy)
posZ0_up3 = "(posTrkZ0>{0}+{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_3,a0_3,a1_3,dz,dy)
eleZ0_down3 = "(-eleTrkZ0>{0}-{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_3,b0_3,b1_3,dz,dy)
posZ0_down3 = "(-posTrkZ0>{0}-{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_3,b0_3,b1_3,dz,dy)
z0cut3 = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up3,posZ0_down3,posZ0_up3,eleZ0_down3)

eleZ0_up4 = "(eleTrkZ0>{0}+{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_4,a0_4,a1_4,dz,dy)
posZ0_up4 = "(posTrkZ0>{0}+{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_4,a0_4,a1_4,dz,dy)
eleZ0_down4 = "(-eleTrkZ0>{0}-{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_4,b0_4,b1_4,dz,dy)
posZ0_down4 = "(-posTrkZ0>{0}-{4}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_4,b0_4,b1_4,dz,dy)
z0cut4 = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up4,posZ0_down4,posZ0_up4,eleZ0_down4)

#cuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,nSig))
cuts.append("uncP>1.85")
cuts.append(isocut)

label2 = ""
if(is80):
	cuts.append("uncM<0.090&&uncM>0.070")
	label2 = " 70 < mass < 90 MeV"
if(is100):
	cuts.append("uncM<0.110&&uncM>0.090")
	label2 = " 90 < mass < 110 MeV"

floatcuts.append("uncP<9999")

if(doUncChisq):
	cuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,2.0))
	cuts.append(z0cut2)
	label.append("unc #chi^{2} < 10")
	label.append("unc #chi^{2} < 6")
	label.append("unc #chi^{2} < 5")
	label.append("unc #chi^{2} < 4")
	label.append("unc #chi^{2} < 3")
	floatcuts.append("uncChisq<6")
	floatcuts.append("uncChisq<5")
	floatcuts.append("uncChisq<4")
	floatcuts.append("uncChisq<3")

if(doV0Proj):
	cuts.append(z0cut2)
	#cuts.append("uncChisq<4")
	label.append("No V0 Proj Cut")
	label.append("V0 Proj 3#sigma")
	label.append("V0 Proj 2.5#sigma")
	label.append("V0 Proj 2#sigma")
	label.append("V0 Proj 1.5#sigma")
	floatcuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,3.0))
	floatcuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,2.5))
	floatcuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,2.0))
	floatcuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,1.5))

if(doIP):
	#cuts.append("uncChisq<4")
	cuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,2.0))
	label.append("No IP Cut")
	label.append("IP Cut #alpha = 10%")
	label.append("IP Cut #alpha = 15%")
	label.append("IP Cut #alpha = 20%")
	label.append("IP Cut #alpha = 25%")
	floatcuts.append(z0cut1)
	floatcuts.append(z0cut2)
	floatcuts.append(z0cut3)
	floatcuts.append(z0cut4)


nomcut = ""
for i in range(len(cuts)):
	if(i == 0):
		nomcut = cuts[i]
	else:
		nomcut = "{0}&&{1}".format(nomcut,cuts[i])

openPDF(outfile,c)

saveCutFlow(events,eventstruth,useAp,is80,is100,plot,nomcut,floatcuts,nBins,minVZ,maxVZ,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle="Events Past Zcut {0}{1}".format(Label,label2))

closePDF(outfile,c)
outfileroot.Close()