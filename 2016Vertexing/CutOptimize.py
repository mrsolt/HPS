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
    print '\t-h: this help message'
    print

zTarg = -4.3
ebeam = 2.3
minVZ = 0
maxVZ = 50
nBins = 50
L1L2 = False
useData = False
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

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:g:i:e:q:t:j:k:m:n:o:p:a:b:y:rd')

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
		if opt=='-r':
			L1L2 = True
		if opt=='-d':
			useData = True
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def saveCutFlow(events,inHisto,cuts,floatcuts,nBins,minX,maxX,label,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	outfileroot.cd()
	histos = []
	color = 0
	for i in range(len(floatcuts)):
		cutstot = "{0}&&{1}".format(cuts,floatcuts[i])
		events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo{0}".format(i),nBins,minX,maxX),cutstot)
		histos.append(ROOT.gROOT.FindObject("histo{0}".format(i)))
		histos[i].Sumw2()

	legend = TLegend(.58,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)

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

	legend.Draw()
	canvas.Print(outfile+".pdf")
	canvas.Write()

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
	uncVXSig = 1.25 * uncVXSig
	uncVYSig = 1.5 * uncVYSig
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

eleZ0_up1 = "(eleTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0_1,a0_1,a1_1)
posZ0_up1 = "(posTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0_1,a0_1,a1_1)
eleZ0_down1 = "(-eleTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0_1,b0_1,b1_1)
posZ0_down1 = "(-posTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0_1,b0_1,b1_1)
z0cut1 = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up1,posZ0_down1,posZ0_up1,eleZ0_down1)

eleZ0_up2 = "(eleTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0_2,a0_2,a1_2)
posZ0_up2 = "(posTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0_2,a0_2,a1_2)
eleZ0_down2 = "(-eleTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0_2,b0_2,b1_2)
posZ0_down2 = "(-posTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0_2,b0_2,b1_2)
z0cut2 = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up2,posZ0_down2,posZ0_up2,eleZ0_down2)

eleZ0_up3 = "(eleTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0_3,a0_3,a1_3)
posZ0_up3 = "(posTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0_3,a0_3,a1_3)
eleZ0_down3 = "(-eleTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0_3,b0_3,b1_3)
posZ0_down3 = "(-posTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0_3,b0_3,b1_3)
z0cut3 = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up3,posZ0_down3,posZ0_up3,eleZ0_down3)

eleZ0_up4 = "(eleTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0_4,a0_4,a1_4)
posZ0_up4 = "(posTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0_4,a0_4,a1_4)
eleZ0_down4 = "(-eleTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0_4,b0_4,b1_4)
posZ0_down4 = "(-posTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0_4,b0_4,b1_4)
z0cut4 = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up4,posZ0_down4,posZ0_up4,eleZ0_down4)

#cuts.append("sqrt((abs((uncVX-(uncVZ-{4})*uncPX/uncPZ)-{0})/(2*{1}))^2+(abs((uncVY-(uncVZ-{4})*uncPY/uncPZ)-{2})/(2*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,zTarg))
#cuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,nSig))
cuts.append("uncChisq<4")
cuts.append("uncP>2.0")
cuts.append(isocut)
cuts.append(z0cut2)

nomcut = ""
for i in range(len(cuts)):
	if(i == 0):
		nomcut = cuts[i]
	else:
		nomcut = "{0}&&{1}".format(nomcut,cuts[i])

label.append("No V0 Proj Cut")
label.append("V0 Proj 1.5#sigma")
label.append("V0 Proj 2#sigma")
label.append("V0 Proj 2.5#sigma")
label.append("V0 Proj 3#sigma")

#label.append("No IP Cut")
#label.append("IP Cut #alpha = 10%")
#label.append("IP Cut #alpha = 15%")
#label.append("IP Cut #alpha = 20%")
#label.append("IP Cut #alpha = 25%")

floatcuts.append("uncP<9999")

floatcuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,1.5))
floatcuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,2.0))
floatcuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,2.5))
floatcuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,3.0))

#floatcuts.append(z0cut1)
#floatcuts.append(z0cut2)
#floatcuts.append(z0cut3)
#floatcuts.append(z0cut4)

openPDF(outfile,c)

saveCutFlow(events,plot,nomcut,floatcuts,nBins,minVZ,maxVZ,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle="Events Past Zcut {0}".format(Label))

closePDF(outfile,c)
outfileroot.Close()