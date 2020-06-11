import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import array
import math
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TLatex, TF1, TGraph, TGraphErrors, TMath
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input text Data file> <input text MC file> <input text A' files>".format(sys.argv[0])
    print 'Note: Even when not using a data, MC, or Ap file, you must feed a dummy text file'
    print "Arguments: "
    print '\t-z: target position (default -4.3 mm)'
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
    print '\t-r: is L1L2 category (default false)'
    print '\t-y: plot label'
    print '\t-h: this help message'
    print

zTarg = -4.3
ebeam = 2.3
nBins = 140
minVZ = -40
maxVZ = 100
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

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:e:q:t:j:k:m:n:o:p:a:b:y:r')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
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
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

n_massbins = 25
minmass = 0.05
maxmass = 0.16

masscut_nsigma = 1.9

mresf = TF1("mresf","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4".format(0.386/1000,0.06735,-0.7197,6.417,-17.63),0.04,0.2)

massRes_avg = 0
dm = (maxmass - minmass) / 10000
for i in range(10000):
	m = minmass+i*(maxmass-minmass)/(10000-1)
	massRes_avg = massRes_avg + mresf.Eval(m) * dm
massRes_avg = massRes_avg / (maxmass - minmass)
local_to_global = (maxmass - minmass) / massRes_avg

def getZCut(fitfunc,zcut_val=0.5,scale=1.0,zBin=0.01,minZ=-60,maxZ=60):
    iMax = int((maxZ-minZ)/zBin)
    for i in range(iMax):
        z = maxZ - zBin*i
        integral = fitfunc.Integral(z,maxZ)
        if(integral > zcut_val/scale):
            return z
    print("ZCut not found!")
    return -9999.

def fitTails(events,cut,mass,label,canvas,outfile):
	fitfunc = TF1("fitfunc","[0]*exp( (((x-[1])/[2])<[3])*(-0.5*(x-[1])^2/[2]^2) + (((x-[1])/[2])>=[3])*(0.5*[3]^2-[3]*(x-[1])/[2]))",-30,30)
	fitfunc.SetParName(0,"Amplitude")
	fitfunc.SetParName(1,"Mean")
	fitfunc.SetParName(2,"Sigma")
	fitfunc.SetParName(3,"Tail Z")

	zcut_val = 0.5
	mres = mresf.Eval(mass)
	events.Draw("uncVZ>>hnew1d(200,-50,50)","abs({0}-{1})<{2}/2*{3}&&({4})".format("uncM",mass,masscut_nsigma,mres,cut),"")

	h1d = gDirectory.Get("hnew1d")
	fit=h1d.Fit("gaus","QS")
	peak=fit.Get().Parameter(0)
	mean=fit.Get().Parameter(1)
	sigma=fit.Get().Parameter(2)
	fit=h1d.Fit("gaus","QS","",mean-3*sigma,mean+3*sigma)
	mean=fit.Get().Parameter(1)
	sigma=fit.Get().Parameter(2)
	fitfunc.SetParameters(peak,mean,sigma,3)
	fit=h1d.Fit(fitfunc,"LSQIM","",mean-2*sigma,mean+10*sigma)
	zcut = getZCut(fitfunc,zcut_val=zcut_val)

	eventsData.Draw("uncM>>numZ(200,-50,50)","({0})&&(uncVZ>{1})&&abs(uncM-{2})<{3}/2*{4}".format(cut,zcut,mass,masscut_nsigma,mres),"")
	numZ = gDirectory.Get("numZ")
	numz = numZ.Integral()

	h1d.SetTitle(label)
	h1d.GetXaxis().SetTitle("reconstructed z (mm)")
	h1d.Draw()
	canvas.SetLogy(1)
	canvas.Print(outfile+".pdf")
	canvas.Write()

	return zcut, numz

def saveCutFlow(eventsData,eventsAp,eventstruth,cuts,cutsdata,varcutdata,varcutMC,nBins,minX,maxX,outfile,canvas,stats=0,logY=0):
	outfileroot.cd()

	eventstruth.Draw("{0}>>{1}({2},{3},{4})".format("triM","histomass",20000,0,0.2))
	histomass = ROOT.gROOT.FindObject("histomass")
	mass = histomass.GetMean()
	eps = (3*(mass-0.08)/(0.1-0.08) + 2*(mass-0.1)/(0.08-0.1)) * 1e-9

	mlow = mass-mresf.Eval(mass)*masscut_nsigma/2
	mhigh = mass+mresf.Eval(mass)*masscut_nsigma/2
	#masscut = "uncM>{0}&&uncM<{0}".format(mlow,mhigh)
	
	deltaM = 0.001
	hbar_c = 1.973e-13
	gamma = 0.965
	gammact = hbar_c*3.0*2.3*gamma/(mass*mass*(1/137.036)*eps)

	eventstruth.Draw("{0}>>{1}({2},{3},{4})".format("triEndZ","histotruth",nBins,minX,maxX))
	histostruth = ROOT.gROOT.FindObject("histotruth")

	exppol1=TF1("exppol1","exp(pol1(0))",-5,100)

	sigarr = array.array('d')
	zeroArr = array.array('d')
	sigErr = array.array('d')
	ZBi = array.array('d')
	norm = 1

	cutstot = "{0}&&{1}".format(cuts,varcutMC[0])
	cutstotdata = "{0}&&{1}".format(cutsdata,varcutdata[0])
	cutstotIP = "{0}&&{1}".format(cuts,varcutMC[1])
	cutstotdataIP = "{0}&&{1}".format(cutsdata,varcutdata[1])

	zcut, numz = fitTails(eventsData,cutstotdata,mass,"10 % Data {0:0.3f} < uncM < {1:0.3f} GeV No IP".format(mlow,mhigh),canvas,outfile)
	zcutIP, numzIP = fitTails(eventsData,cutstotdataIP,mass,"10 % Data {0:0.3f} < uncM < {1:0.3f} GeV With IP".format(mlow,mhigh),canvas,outfile)

	eventsData.Draw("uncVZ>>num(200,-50,50)","abs({0}-{1})<{2}/2*{3}&&({4})".format("uncM",mass,1,deltaM,cutstotdata),"")
	num = gDirectory.Get("num")
	num_rad = num.Integral()

	eventsAp.Draw("{0}>>{1}({2},{3},{4})".format("triEndZ","histo",nBins,minX,maxX),"{0}&&{1}".format(cutstot,"(uncVZ>{0})".format(zcut)))
	histo = ROOT.gROOT.FindObject("histo")
	sig = histo.Integral()

	eventsAp.Draw("{0}>>{1}({2},{3},{4})".format("triEndZ","histoIP",nBins,minX,maxX),"{0}&&{1}".format(cutstotIP,"(uncVZ>{0})".format(zcutIP)))
	histoIP = ROOT.gROOT.FindObject("histoIP")
	sigIP = histoIP.Integral()

	eventsAp.Draw("{0}>>{1}({2},{3},{4})".format("triEndZ","histoIP2",nBins,minX,maxX),"{0}&&{1}".format(cutstotIP,"(uncVZ>{0})".format(zcut)))
	histoIP2 = ROOT.gROOT.FindObject("histoIP2")
	sigIP2 = histoIP2.Integral()

	ap_yield = 3*math.pi/(2*(1/137.0))*num_rad*(mass/deltaM)
	exppol1.SetParameters(zTarg/gammact-math.log(gammact),-1.0/gammact)

	histo.Divide(histostruth)
	histoIP.Divide(histostruth)
	histoIP2.Divide(histostruth)

	histo2 = TH1F("histo2","histo2",nBins,minX,maxX)
	histo2IP = TH1F("histo2IP","histo2IP",nBins,minX,maxX)
	histo2IP2 = TH1F("histo2IP2","histo2IP2",nBins,minX,maxX)
	for j in range(histo.GetNbinsX()):
		sig_bin = histo.GetBinContent(j+1) * exppol1.Eval(histo.GetBinCenter(j+1))
		histo2.SetBinContent(j+1,sig_bin)
		sig_binIP = histoIP.GetBinContent(j+1) * exppol1.Eval(histoIP.GetBinCenter(j+1))
		histo2IP.SetBinContent(j+1,sig_binIP)
		sig_binIP2 = histoIP2.GetBinContent(j+1) * exppol1.Eval(histoIP2.GetBinCenter(j+1))
		histo2IP2.SetBinContent(j+1,sig_binIP2)
	sigyield = histo.Integral() #* ap_yield
	sigyieldIP = histoIP.Integral() #* ap_yield
	sigyieldIP2 = histoIP2.Integral() #* ap_yield
	norm = sigyield
	back = max(0.5,numz)
	backIP = max(0.5,numzIP)
	print("No IP Cut  Signal Yield: {0}   Background: {1}   Sig/Back: {2}   Zcut: {3}".format(sigyield/norm,numz,sigyield/(norm*back),zcut))
	print("With IP Cut  Signal Yield: {0}   Background: {1}   Sig/Back: {2}   Zcut: {3}".format(sigyieldIP/norm,numzIP,sigyieldIP/(norm*backIP),zcutIP))
	print("With IP Cut2  Signal Yield: {0}   Background: {1}   Sig/Back: {2}   Zcut: {3}".format(sigyieldIP2/norm,numzIP,sigyieldIP2/(norm*backIP),zcut))

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

file = TFile(remainder[1])
eventsData = file.Get("ntuple")

file2 = TFile(remainder[2])
eventsAp = file2.Get("ntuple")

file3 = TFile(remainder[3])
eventstruth = file3.Get("ntuple")

angleMC = 0.111025680707
angleData = 0.0386557750132
angle = angleMC
xProj = "(uncVX-(uncVZ-{0})*uncPX/uncPZ)".format(zTarg)
yProj = "(uncVY-(uncVZ-{0})*uncPY/uncPZ)".format(zTarg)
xProj_rot = "{0}*cos({2})-{1}*sin({2})".format(xProj,yProj,-angle)
yProj_rot = "{0}*sin({2})+{1}*cos({2})".format(xProj,yProj,-angle)
nSig = 2

uncTargProjX = -0.0995461972579
uncTargProjXSig = 0.217919555935 
uncTargProjY = -0.0668941015569
uncTargProjYSig = 0.0831670646584

dy = 0.0
dz = 0.0

eleiso = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3.0*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(zTarg)
posiso = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3.0*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(zTarg)

m0 = -0.201776054859
a0 = 0.0518988558564
a1 = -0.00230111045957
b0 = 0.0471576968062
b1 = -0.00108639651791

isocut = "({0}&&{1})".format(eleiso,posiso)

eleZ0_up = "(eleTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,a0,a1,dz,dy)
posZ0_up = "(posTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,a0,a1,dz,dy)
eleZ0_down = "(-eleTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,b0,b1,dz,dy)
posZ0_down = "(-posTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,b0,b1,dz,dy)
z0cut = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up,posZ0_down,posZ0_up,eleZ0_down)

cuts = []
cuts.append("eleHasL1&&posHasL1&&eleHasL2&&posHasL2")
cuts.append(isocut)
cuts.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,2.0))
#cuts.append(z0cut)
cuts.append("uncP>1.85")

varcutMC = []
varcutMC.append("uncP<9999")
varcutMC.append(z0cut)

angle = angleData
xProj = "(uncVX-(uncVZ-{0})*uncPX/uncPZ)".format(zTarg)
yProj = "(uncVY-(uncVZ-{0})*uncPY/uncPZ)".format(zTarg)
xProj_rot = "{0}*cos({2})-{1}*sin({2})".format(xProj,yProj,-angle)
yProj_rot = "{0}*sin({2})+{1}*cos({2})".format(xProj,yProj,-angle)

uncTargProjX = -0.132056961029
uncTargProjXSig = 0.335342793001
uncTargProjY = -0.0741286476856
uncTargProjYSig = 0.100009325509

c0 = -0.377
c1 = 13.79
c2 = -55.84
c3 = 84.0

dy = uncTargProjY - (-0.0668941015569)
dz = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3".format(c0,c1,c2,c3)

eleZ0_up = "(eleTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,a0,a1,dz,dy)
posZ0_up = "(posTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,a0,a1,dz,dy)
eleZ0_down = "(-eleTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,b0,b1,dz,dy)
posZ0_down = "(-posTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,b0,b1,dz,dy)
z0cut = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up,posZ0_down,posZ0_up,eleZ0_down)

cutsdata = []
cutsdata.append("eleHasL1&&posHasL1&&eleHasL2&&posHasL2")
cutsdata.append(isocut)
cutsdata.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,2.0))
#cutsdata.append(z0cut)
cutsdata.append("uncP>1.85")

varcutdata = []
varcutdata.append("uncP<9999")
varcutdata.append(z0cut)

nomcut = ""
nomcutdata = ""
for i in range(len(cuts)):
	if(i == 0):
		nomcut = cuts[i]
		nomcutdata = cutsdata[i]
	else:
		nomcut = "{0}&&{1}".format(nomcut,cuts[i])
		nomcutdata = "{0}&&{1}".format(nomcutdata,cutsdata[i])


openPDF(outfile,c)

saveCutFlow(eventsData,eventsAp,eventstruth,nomcut,nomcutdata,varcutdata,varcutMC,nBins,minVZ,maxVZ,outfile,c)

closePDF(outfile,c)
outfileroot.Close()