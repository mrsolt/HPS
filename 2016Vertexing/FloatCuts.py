import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import array
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TLatex, TF1, TGraph
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
    print '\t-T: fittails (default false)'
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
FitTails = False
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

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:g:i:e:q:t:j:k:m:n:o:p:a:b:y:fTrdcl')

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
		if opt=='-T':
			FitTails = True
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

n_massbins = 50
minmass = 0.04
maxmass = 0.175
masscut_nsigma = 1.9

def getZCut(fitfunc,zcut_val=0.5,scale=1.0,zBin=0.01,minZ=-60,maxZ=60):
    iMax = int((maxZ-minZ)/zBin)
    for i in range(iMax):
        z = maxZ - zBin*i
        integral = fitfunc.Integral(z,maxZ)
        if(integral > zcut_val/scale):
            return z
    print("ZCut not found!")
    return -9999.

def fitTails(events,cut,n_massbins,minmass,maxmass,masscut_nsigma,cutnorm):
	fitfunc = TF1("fitfunc","[0]*exp( (((x-[1])/[2])<[3])*(-0.5*(x-[1])^2/[2]^2) + (((x-[1])/[2])>=[3])*(0.5*[3]^2-[3]*(x-[1])/[2]))",-50,50)
	fitfunc.SetParName(0,"Amplitude")
	fitfunc.SetParName(1,"Mean")
	fitfunc.SetParName(2,"Sigma")
	fitfunc.SetParName(3,"Tail Z")

	massarray = array.array('d')
	zcutarray = array.array('d')
	zcutarrayscaled = array.array('d')

	zcut_val = 0.5
	mresf = TF1("mresf","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4".format(0.386/1000,0.06735,-0.7197,6.417,-17.63),0.04,0.2)
	for i in range(0,n_massbins):
		mass = minmass+i*(maxmass-minmass)/(n_massbins-1)
		massarray.append(mass)

		mres = mresf.Eval(mass)

		events.Draw("uncVZ>>ref(200,-50,50)","abs({0}-{1})<{2}/2*{3}&&({4})".format("uncM",mass,masscut_nsigma,mres,cutnorm),"")
		ref = gDirectory.Get("ref")

		events.Draw("uncVZ>>hnew1d(200,-50,50)","abs({0}-{1})<{2}/2*{3}&&({4})".format("uncM",mass,masscut_nsigma,mres,cut),"")

		h1d = gDirectory.Get("hnew1d")
		fit=h1d.Fit("gaus","QS")
		peak=fit.Get().Parameter(0)
		mean=fit.Get().Parameter(1)
		sigma=fit.Get().Parameter(2)
		fit=h1d.Fit("gaus","QS","",mean-3*sigma,mean+3*sigma)
		mean=fit.Get().Parameter(1)
		sigma=fit.Get().Parameter(2)
		print("mean {0}  sigma {1}".format(mean,sigma))
		fitfunc.SetParameters(peak,mean,sigma,3)
		fit=h1d.Fit(fitfunc,"LSQIM","",mean-2*sigma,mean+10*sigma)
		zcut = getZCut(fitfunc,zcut_val=zcut_val)
		zcutarray.append(zcut)
		scale_factor = ref.Integral()/h1d.Integral()
		zcut_val_scaled = zcut_val/scale_factor
		zcut_scaled = getZCut(fitfunc,zcut_val=zcut_val_scaled)
		zcutarrayscaled.append(zcut_scaled)
	return massarray, zcutarray, zcutarrayscaled

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

#dz = "0."
#if(useData):
#	dz = "((-3.517-13.41*uncM+88.16*uncM^2-173.1*uncM^3)-(-3.14-27.2*uncM+144*uncM^2-257.1*uncM^3))"

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

#plot = "uncVZ"
plot = "{0}+{1}".format('uncVZ',dz)
plotlabel = "Reconstructed z [mm]"

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
	label.append("Track/Cluster Match #chi^{2} < 10")
	label.append("Cluster Time Diff < 1.45 ns")
	label.append("Track/Cluster Time Diff < 4 ns")
	label.append("e- Momentum < 1.75 GeV")
	label.append("Track Chisq / dof < 6")
	label.append("Unconstrained Vertex #chi^{2} < 10")
	label.append("e- and e+ Momentum > 0.4 GeV")
	label.append("e+ e- Momentum Sum < 2.4 GeV")

else:
	label.append("Preselection")

	if(L1L2):
		#x0_cut1_pos_x0 = -0.3187
		#x1_cut1_pos_x0 = -0.9498

		#x0_cut1_neg_x0 = -0.09418
		#x1_cut1_neg_x0 = -0.7761

		#x0_cut1_pos_x1 = 0.02095
		#x1_cut1_pos_x1 = 0.05914

		#x0_cut1_neg_x1 = 0.02016
		#x1_cut1_neg_x1 = 0.05854

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

		#z0cut2 = "((eleTrkZ0>((-0.204298550172+-0.819203072994*uncM)+(0.0215541584276+0.0769066743212*uncM)*(uncVZ+{0}))&&-posTrkZ0>((-0.0131964462788+-0.356152922206*uncM)+(0.0199952852357+0.0682704240163*uncM)*(uncVZ+{0})))||(posTrkZ0>((-0.204298550172+-0.819203072994*uncM)+(0.0215541584276+0.0769066743212*uncM)*(uncVZ+{0}))&&-eleTrkZ0>((-0.0131964462788+-0.356152922206*uncM)+(0.0199952852357+0.0682704240163*uncM)*(uncVZ+{0}))))".format(dz) #80%
		#z0cut3 = "((eleTrkZ0>((-0.160212840296+-0.711401031858*uncM)+(0.0235892675119+0.0868362671156*uncM)*(uncVZ+{0}))&&-posTrkZ0>((0.0074583976511+-0.335278819542*uncM)+(0.0213379480119+0.0830900617137*uncM)*(uncVZ+{0})))||(posTrkZ0>((-0.160212840296+-0.711401031858*uncM)+(0.0235892675119+0.0868362671156*uncM)*(uncVZ+{0}))&&-eleTrkZ0>((0.0074583976511+-0.335278819542*uncM)+(0.0213379480119+0.0830900617137*uncM)*(uncVZ+{0}))))".format(dz) #70%

		cuts.append("((!eleHasL1&&posHasL1)||(eleHasL1&&!posHasL1))&&eleHasL2&&posHasL2")
		label.append("e- (!L1 & L2) or e+ (!L1 & L2)")
		uncVXSig = 1.25 * uncVXSig
		uncVYSig = 1.5 * uncVYSig
		uncTargProjXSig = 1.25 * uncTargProjXSig
		uncTargProjYSig = 1.5 * uncTargProjYSig

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

		eleZ0_up1 = "(eleTrkZ0>{0}+{4}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_1,a0_1,a1_1,dz,dy)
		posZ0_up1 = "(posTrkZ0>{0}+{4}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_1,a0_1,a1_1,dz,dy)
		eleZ0_down1 = "(-eleTrkZ0>{0}-{4}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_1,b0_1,b1_1,dz,dy)
		posZ0_down1 = "(-posTrkZ0>{0}-{4}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_1,b0_1,b1_1,dz,dy)
		z0cut1 = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up1,posZ0_down1,posZ0_up1,eleZ0_down1)

		eleZ0_up2 = "(eleTrkZ0>{0}+{4}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_2,a0_2,a1_2,dz,dy)
		posZ0_up2 = "(posTrkZ0>{0}+{4}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_2,a0_2,a1_2,dz,dy)
		eleZ0_down2 = "(-eleTrkZ0>{0}-{4}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_2,b0_2,b1_2,dz,dy)
		posZ0_down2 = "(-posTrkZ0>{0}-{4}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_2,b0_2,b1_2,dz,dy)
		z0cut2 = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up2,posZ0_down2,posZ0_up2,eleZ0_down2)

		eleZ0_up3 = "(eleTrkZ0>{0}+{4}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_3,a0_3,a1_3,dz,dy)
		posZ0_up3 = "(posTrkZ0>{0}+{4}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_3,a0_3,a1_3,dz,dy)
		eleZ0_down3 = "(-eleTrkZ0>{0}-{4}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_3,b0_3,b1_3,dz,dy)
		posZ0_down3 = "(-posTrkZ0>{0}-{4}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ+{3}))".format(m0_3,b0_3,b1_3,dz,dy)
		z0cut3 = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up3,posZ0_down3,posZ0_up3,eleZ0_down3)

	else:
		#x0_cut1_pos_x0 = -0.2289
		#x1_cut1_pos_x0 = -1.09

		#x0_cut1_neg_x0 = -0.0009241
		#x1_cut1_neg_x0 = -1.612

		#x0_cut1_pos_x1 = 0.009205
		#x1_cut1_pos_x1 = 0.2069

		#x0_cut1_neg_x1 = 0.0091
		#x1_cut1_neg_x1 = 0.2341

		eleiso_1 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-2.5*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
		posiso_1 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-2.5*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)
		eleiso_2 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
		posiso_2 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)
		eleiso_3 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3.5*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
		posiso_3 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3.5*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

		#z0cut2 = "((eleTrkZ0>{0}&&-posTrkZ0>{1})||(posTrkZ0>{0}&&-eleTrkZ0>{1}))".format(cut1_pos_2,cut1_neg_2)
		#z0cut3 = "((eleTrkZ0>{0}&&-posTrkZ0>{1})||(posTrkZ0>{0}&&-eleTrkZ0>{1}))".format(cut1_pos_3,cut1_neg_3)
		#z0cut2 = "((eleTrkZ0>((-0.177913468428+-0.932330924205*uncM)+(0.00961915803124+0.228303547556*uncM)*(uncVZ+{0}))&&-posTrkZ0>((0.0115212779435+-0.651929048499*uncM)+(0.0125216209858+0.217752673675*uncM)*(uncVZ+{0})))||(posTrkZ0>((-0.177913468428+-0.932330924205*uncM)+(0.00961915803124+0.228303547556*uncM)*uncVZ)&&-eleTrkZ0>((0.0115212779435+-0.651929048499*uncM)+(0.0125216209858+0.217752673675*uncM)*(uncVZ+{0}))))".format(dz) #80%
		#z0cut3 = "((eleTrkZ0>((-0.168325129572+-0.764572061732*uncM)+(0.0117844556696+0.238831014837*uncM)*(uncVZ+{0}))&&-posTrkZ0>((0.0144335686792+-0.576408853332*uncM)+(0.0158057745213+0.223434276362*uncM)*(uncVZ+{0})))||(posTrkZ0>((-0.168325129572+-0.764572061732*uncM)+(0.0117844556696+0.238831014837*uncM)*uncVZ)&&-eleTrkZ0>((0.0144335686792+-0.576408853332*uncM)+(0.0158057745213+0.223434276362*uncM)*(uncVZ+{0}))))".format(dz) #70%

		cuts.append("eleHasL1&&posHasL1&&eleHasL2&&posHasL2")
		label.append("e+e- L1 & L2")

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

	#x0_cut1_pos = "({0}+{1}*uncM)".format(x0_cut1_pos_x0,x1_cut1_pos_x0)
	#x1_cut1_pos = "({0}+{1}*uncM)".format(x0_cut1_pos_x1,x1_cut1_pos_x1)
	#cut1_pos = "({0}+{1}*(uncVZ+{2}))".format(x0_cut1_pos,x1_cut1_pos,dz)

	#x0_cut1_neg = "({0}+{1}*uncM)".format(x0_cut1_neg_x0,x1_cut1_neg_x0)
	#x1_cut1_neg = "({0}+{1}*uncM)".format(x0_cut1_neg_x1,x1_cut1_neg_x1)
	#cut1_neg = "({0}+{1}*(uncVZ+{2}))".format(x0_cut1_neg,x1_cut1_neg,dz)

	#z0cut = "((eleTrkZ0>{0}&&-posTrkZ0>{1})||(posTrkZ0>{0}&&-eleTrkZ0>{1}))".format(cut1_pos,cut1_neg)
	isocut1 = "({0}&&{1})".format(eleiso_1,posiso_1)
	isocut2 = "({0}&&{1})".format(eleiso_2,posiso_2)
	isocut3 = "({0}&&{1})".format(eleiso_3,posiso_3)

	#cuts.append("sqrt((abs((uncVX-(uncVZ-{4})*uncPX/uncPZ)-{0})/(2*{1}))^2+(abs((uncVY-(uncVZ-{4})*uncPY/uncPZ)-{2})/(2*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,zTarg))
	cuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,nSig))
	#cuts.append("uncChisq<4")
	cuts.append("uncP<9999")
	cuts.append("uncP>1.85")
	cuts.append(isocut2)
	cuts.append(z0cut2)

	label.append("V0 Projection 2#sigma")
	label.append("V0 Projection 1.5#sigma")
	label.append("V0 Projection 2.5#sigma")
	label.append("Unconstrained Vertex #chi^{2} < 4")
	label.append("Unconstrained Vertex #chi^{2} < 3")
	label.append("Unconstrained Vertex #chi^{2} < 5")
	label.append("V0 momentum > 1.85 GeV")
	label.append("V0 momentum > 1.75 GeV")
	label.append("V0 momentum > 1.95 GeV")
	label.append("Isolation Cut 3#sigma")
	label.append("Isolation Cut 2.5#sigma")
	label.append("Isolation Cut 3.5#sigma")
	label.append("Impact Parameter Cuts #alpha = 15%")
	label.append("Impact Parameter Cuts #alpha = 10%")
	label.append("Impact Parameter Cuts #alpha = 20%")

	#cut1_pos_2 = "({0}+{1}*(uncVZ+{2}))+0.1".format(x0_cut1_pos,x1_cut1_pos,dz)
	#cut1_neg_2 = "({0}+{1}*(uncVZ+{2}))+0.1".format(x0_cut1_neg,x1_cut1_neg,dz)
	#cut1_pos_3 = "({0}+{1}*(uncVZ+{2}))+0.2".format(x0_cut1_pos,x1_cut1_pos,dz)
	#cut1_neg_3 = "({0}+{1}*(uncVZ+{2}))+0.2".format(x0_cut1_neg,x1_cut1_neg,dz)

	#floatcuts.append("sqrt((abs((uncVX-(uncVZ-{4})*uncPX/uncPZ)-{0})/(1.5*{1}))^2+(abs((uncVY-(uncVZ-{4})*uncPY/uncPZ)-{2})/(1.5*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,zTarg))
	#floatcuts.append("sqrt((abs((uncVX-(uncVZ-{4})*uncPX/uncPZ)-{0})/(2.5*{1}))^2+(abs((uncVY-(uncVZ-{4})*uncPY/uncPZ)-{2})/(2.5*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,zTarg))
	floatcuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,1.5))
	floatcuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,2.5))
	floatcuts.append("uncChisq<3")
	floatcuts.append("uncChisq<5")
	floatcuts.append("uncP>1.75")
	floatcuts.append("uncP>1.95")
	floatcuts.append(isocut1)
	floatcuts.append(isocut3)
	floatcuts.append(z0cut1)
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

if(FitTails):
	for i in range(len(cuts)-2):
		if(i != 0 and i != 2):
			continue
		cuts_1 = cuts_1_arr[i+1]
		cut1 = cuts[i+2]
		cut2 = floatcuts[2*i]
		cut3 = floatcuts[2*i+1]
		massarray,zcutarray1,zcutarrayscaled1 = fitTails(events,cuts_1,n_massbins,minmass,maxmass,masscut_nsigma,cuts_1+"&&"+cut1)
		_,zcutarray2,zcutarrayscaled2 = fitTails(events,cuts_1+"&&"+cut1,n_massbins,minmass,maxmass,masscut_nsigma,cuts_1+"&&"+cut1)
		_,zcutarray3,zcutarrayscaled3 = fitTails(events,cuts_1+"&&"+cut2,n_massbins,minmass,maxmass,masscut_nsigma,cuts_1+"&&"+cut1)
		_,zcutarray4,zcutarrayscaled4 = fitTails(events,cuts_1+"&&"+cut3,n_massbins,minmass,maxmass,masscut_nsigma,cuts_1+"&&"+cut1)
		graph1=TGraph(len(massarray),massarray,zcutarray1)
		graph2=TGraph(len(massarray),massarray,zcutarray2)
		graph3=TGraph(len(massarray),massarray,zcutarray3)
		graph4=TGraph(len(massarray),massarray,zcutarray4)
		graph1.SetMarkerColor(1)
		graph1.SetLineColor(1)
		graph2.SetMarkerColor(2)
		graph2.SetLineColor(2)
		graph3.SetMarkerColor(4)
		graph3.SetLineColor(4)
		graph4.SetMarkerColor(6)
		graph4.SetLineColor(6)
		graph1.GetYaxis().SetRangeUser(-4.3,30)
		graph1.Draw("A*")
		graph1.SetTitle("Zcut for Varying {0} Cut".format(label[3*i+2]))
		graph1.GetXaxis().SetTitle("mass [GeV]")
		graph1.GetYaxis().SetTitle("zcut [mm]")
		graph2.Draw("*Psame")
		graph3.Draw("*Psame")
		graph4.Draw("*Psame")
		legend = TLegend(.53,.66,.77,.87)
		legend.SetBorderSize(0)
		legend.SetFillColor(0)
		legend.SetFillStyle(0)
		legend.SetTextFont(42)
		legend.SetTextSize(0.035)
		legend.AddEntry(graph1,"W/O {0}".format(label[3*i+2]),"P")
		legend.AddEntry(graph2,label[3*i+2],"P")
		legend.AddEntry(graph3,label[3*i+3],"P")
		legend.AddEntry(graph4,label[3*i+4],"P")
		legend.Draw("")
		c.Print(remainder[0]+".pdf","Title:zcut")
		c.Write()

		graphscaled1=TGraph(len(massarray),massarray,zcutarrayscaled1)
		graphscaled2=TGraph(len(massarray),massarray,zcutarrayscaled2)
		graphscaled3=TGraph(len(massarray),massarray,zcutarrayscaled3)
		graphscaled4=TGraph(len(massarray),massarray,zcutarrayscaled4)
		graphscaled1.SetMarkerColor(1)
		graphscaled1.SetLineColor(1)
		graphscaled2.SetMarkerColor(2)
		graphscaled2.SetLineColor(2)
		graphscaled3.SetMarkerColor(4)
		graphscaled3.SetLineColor(4)
		graphscaled4.SetMarkerColor(6)
		graphscaled4.SetLineColor(6)
		graphscaled1.GetYaxis().SetRangeUser(-4.3,30)
		graphscaled1.Draw("A*")
		graphscaled1.SetTitle("Zcut for Varying {0} Cut Normalized".format(label[3*i+2]))
		graphscaled1.GetXaxis().SetTitle("mass [GeV]")
		graphscaled1.GetYaxis().SetTitle("zcut [mm]")
		graphscaled2.Draw("*Psame")
		graphscaled3.Draw("*Psame")
		graphscaled4.Draw("*Psame")
		legend.Draw("")
		c.Print(remainder[0]+".pdf","Title:zcut")
		c.Write()

		del zcutarray1
		del zcutarray2
		del zcutarray3
		del zcutarray4
		del zcutarrayscaled1
		del zcutarrayscaled2
		del zcutarrayscaled3
		del zcutarrayscaled4
		del massarray
		del legend

for i in range(len(cuts)-2):
	cuts_1 = cuts_1_arr[i+1]
	cut1 = cuts[i+2]
	cut2 = floatcuts[2*i]
	cut3 = floatcuts[2*i+1]
	saveCutFlow(events,plot,i,cuts_1,cut1,cut2,cut3,nBins,minVZ,maxVZ,label,outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " {0}".format(Label),stats=0)

closePDF(outfile,c)
outfileroot.Close()