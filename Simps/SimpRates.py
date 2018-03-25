#Simp Rates
#author Matt Solt

import numpy as np
import sys
import array
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1, TH1F, TH2F, TF1, RooDataSet, RooWorkspace, RooFit, RooArgList
sys.argv = tmpargv

def openPDF(outfile,canvas):
	canvas.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	canvas.Print(outfile+".pdf]")

def drawHisto(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	histo.Draw("")
	#histo.GetXaxis().SetRangeUser(-5,150)
	#histo.GetYaxis().SetRangeUser(0,1.1)
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)

def saveHisto(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logy=0,logx=0):
	drawHisto(histo,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.SetLogx(logx)
	canvas.SetLogy(logy)
	canvas.Print(outfile+".pdf")

def rate_Ap(m_Ap,eps,N_eff):
	alpha = 1/137.
	return N_eff * m_Ap * alpha * eps**2

def rate_2pi(m_Ap,m_pi,m_V,alpha_D):
	coeff = 2*alpha_D/3 * m_Ap
	pow1 = (1-4*m_pi**2/(m_Ap**2))**(3/2.)
	pow2 = (m_V**2/(m_Ap**2-m_V**2))**2
	return coeff * pow1 * pow2

def rate_Vpi(m_Ap,m_pi,m_V,alpha_D,f_pi,rho,phi):
	x = m_pi/m_Ap
	y = m_V/m_Ap
	pi = 3.14159
	coeff = alpha_D*Tv(rho,phi)/(192*pi**4)
	return coeff * 1/(x**2) * (y**2/(x**2)) * (m_pi/f_pi)**4 * m_Ap*Beta(x,y)**(3/2.)

def br_Vpi(m_Ap,m_pi,m_V,alpha_D,f_pi,rho,phi):
	rate = rate_Vpi(m_Ap,m_pi,m_V,alpha_D,f_pi,rho,phi) + rate_2pi(m_Ap,m_pi,m_V,alpha_D)
	if(2*m_V < m_Ap): rate = rate_Vpi(m_Ap,m_pi,m_V,alpha_D,f_pi,rho,phi) + rate_2pi(m_Ap,m_pi,m_V,alpha_D) + rate_2V(m_Ap,m_V,alpha_D)
	return rate_Vpi(m_Ap,m_pi,m_V,alpha_D,f_pi,rho,phi)/rate

def br_2V(m_Ap,m_pi,m_V,alpha_D,f_pi,rho,phi):
	if(2*m_V >= m_Ap): return 0.
	rate = rate_Vpi(m_Ap,m_pi,m_V1,alpha_D,f_pi,rho,phi) + rate_2pi(m_Ap,m_pi,m_V1,alpha_D) + rate_2V(m_Ap,m_V1,alpha_D)
	return rate_2V(m_Ap,m_V1,alpha_D)/rate

def Tv(rho,phi):
	if rho:
		return 3/4.
	elif phi:
		return 3/2.
	else:
		return 18

def Beta(x,y):
	return (1+y**2-x**2-2*y)*(1+y**2-x**2+2*y)

def rate_2V(m_Ap,m_V,alpha_D):
	r = m_V/m_Ap
	return alpha_D/6 * m_Ap * f(r)

def f(r):
	num = 1 + 16*r**2 - 68*r**4 - 48*r**6
	den = (1-r**2) ** 2
	return num/den * (1-4*r**2)**0.5

def rate_2l(m_Ap,m_pi,m_V,eps,alpha_D,f_pi,m_l,rho):
	alpha = 1/137.
	pi = 3.14159
	coeff = 16*pi*alpha_D*alpha*eps**2*f_pi**2/(3*m_V**2)
	term1 = (m_V**2/(m_Ap**2 - m_V**2))**2
	term2 = (1-4*m_l**2/m_V**2)**0.5
	term3 = 1+2*m_l**2/m_V**2
	const = 1
	if rho:
		const = 2
	return coeff * term1 * term2 * term3 * m_V * const

def ctau(m_Ap,m_pi,m_V,eps,alpha_D,f_pi,m_l,rho):
	hbar_c = 1.973e-13
	return hbar_c / rate_2l(m_Ap,m_pi,m_V,eps,alpha_D,f_pi,m_l,rho)

def Vdistribution(z,targZ,gammact):
	return np.exp(targZ/gammact-1/gammact*z)/gammact

def integrate(minZ,maxZ,n,targZ,gammact,mass,inputFile):
	tot = 0
	zwidth = (maxZ-minZ)/float(n)
	for i in range(0,n):
		z = minZ + (i + 0.5) * zwidth
		tot = tot + InterpolateFromFile(mass,z,inputFile) * Vdistribution(z,targZ,gammact) * zwidth
	return tot

#Function to plot efficiency tests of known masses
def Interpolate(Mass,Z,mass,z,eff):
    iMass = 0
    iZ = 0
    nMass = len(mass)
    nBins = len(z)
    #Grab the index of mass and z
    for i in range(nMass):
        if(Mass < mass[i]):
	    iMass = i
	    break
    for i in range(nBins):
        if(Z < z[i]):
	    iZ = i
	    break
    #Check to make sure mass and z are not out of range
    if(iMass == 0):
        print "Mass is out of range!"
        return
    if(iZ == 0):
        print "Z is behind target!"
        return
    iMass1 = iMass - 1
    iMass2 = iMass
    iZ1 = iZ - 1
    iZ2 = iZ
    Q11 = eff[iMass1][iZ1]
    Q12 = eff[iMass2][iZ1]
    Q21 = eff[iMass1][iZ2]
    Q22 = eff[iMass2][iZ2]
    #Interpolate value
    interpolate = Bilinear(Z,Mass,z[iZ1],z[iZ2],mass[iMass1],mass[iMass2],Q11,Q12,Q21,Q22)
    return interpolate

#Function to plot efficiency tests of known masses directly from file
def InterpolateFromFile(Mass,Z,inputFile):
	mass = getMassArray(inputFile)
	z = getZArray(inputFile)
	eff = getEfficiency(inputFile)
	interpolate = Interpolate(Mass,Z,mass,z,eff)
	return interpolate

def getMassArray(inputFile):
 	inputfile = open(inputFile,"r")
	mass = []
	result = []
	#Readlines from input file
	lines = inputfile.readlines()
	for x in lines:
		result.append(x.split())
	inputfile.close()
	nMass = len(result[0])
	#Grab Array of Masses
	for i in range(nMass):
		mass.append(float(result[0][i]))
	return mass

def getZArray(inputFile):
 	inputfile = open(inputFile,"r")
	z = []
	result = []
	#Readlines from input file
	lines = inputfile.readlines()
	for x in lines:
		result.append(x.split())
	inputfile.close()
	nBins = len(result[1])
	#Grab Array of z's
	for i in range(nBins):
		z.append(float(result[1][i]))
	return z

def getEfficiency(inputFile):
	inputfile = open(inputFile,"r")
	result = []
	eff = []
	#Readlines from input file
	lines = inputfile.readlines()
	for x in lines:
 		result.append(x.split())
	inputfile.close()
        nMass = len(result[0])
        nBins = len(result[1])
	#Convert the strings from input file into floats
	for i in range(nMass):
		dummy = []
		for j in range(nBins):
	    		dummy.append(float(result[i+2][j]))
		eff.append(dummy)
		del dummy
	return eff

#Function for Bilinear interpolation
def Bilinear(x,y,x1,x2,y1,y2,Q11,Q12,Q21,Q22):
    denom = (x2-x1)*(y2-y1)
    t1 = (x2-x)*(y2-y)/denom*Q11
    t2 = (x-x1)*(y2-y)/denom*Q21
    t3 = (x2-x)*(y-y1)/denom*Q12
    t4 = (x-x1)*(y-y1)/denom*Q22
    return t1+t2+t3+t4

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

scale = 1.0

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hs:')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-s':
			scale = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

alpha_D = 0.01
#hbar_c = 1.973e-13
m_l = 0.000000511
Ebeam = 2.3
gamma = 0.65
targetz = 0.0
maxZ = 80.
zcut_count = 0.5
masscut_nsigma = 2.80
masscut_eff = 0.838

outfile = remainder[0]
efffile = remainder[1]
tailsfile = TFile(remainder[2])
infile = TFile(remainder[3])
massresfile = TFile(remainder[4])
radfile = TFile(remainder[5])

NepsBins = 20
epsmin = -4
epsmax = -2
Nfpi = 1
fpimin = 3
fpimax = 3
Nalphad = 1
alphadmin = 0.01
alphadmax = 0.01
nApMass = 20
massApmin = 0.07
massApmax = 0.139
nVMass = 1
massVmin = 0.01
massVmax = 1.0
nPiMass = 1
massPimin = 0.01
massPimax = 1.0

fitfunc = TF1("fitfunc","[0]*exp( ((x-[1])<[3])*(-0.5*(x-[1])^2/[2]^2) + ((x-[1])>=[3])*(-0.5*[3]^2/[2]^2-(x-[1]-[3])/[4]))",-50,50)
fitfunc.SetParName(0,"Amplitude")
fitfunc.SetParName(1,"Mean")
fitfunc.SetParName(2,"Sigma")
fitfunc.SetParName(3,"Tail Z")
fitfunc.SetParName(4,"Tail length")


w = RooWorkspace("w")
w.factory("{0}[0,0.1]".format("uncM"))
w.factory("uncVZ[-100,100]")
w.factory("uncP[0,10]")
w.factory("cut[0,1]")

w.defineSet("myVars","{0},uncVZ".format("uncM"))

events = infile.Get("cut")
eventsrad = radfile.Get("ntuple")
dataset = RooDataSet("data","data",events,w.set("myVars"),"")

w.factory("Gaussian::vtx_model(uncVZ,mean[-50,50],sigma[0,50])")
gauss_pdf = w.pdf("vtx_model")
w.factory("EXPR::gaussExp('exp( ((@0-@1)<@3)*(-0.5*(@0-@1)^2/@2^2) + ((@0-@1)>=@3)*(-0.5*@3^2/@2^2-(@0-@1-@3)/@4))',uncVZ,gauss_mean[-5,-20,20],gauss_sigma[5,1,50],exp_breakpoint[10,0,50],exp_length[3,0.5,20])")
gaussexp_pdf = w.pdf("gaussExp")
w.defineSet("obs_1d","uncVZ")
obs=w.set("obs_1d")
uncVZ = w.var("uncVZ")
uncVZ.setBins(200)
gauss_params = gauss_pdf.getParameters(obs)
gaussexp_params = gaussexp_pdf.getParameters(obs)

Medges = array.array('d')
Epsedges = array.array('d')
for i in range(0,nApMass+1):
    Medges.append(massApmin+(i-0.5)*(massApmax-massApmin)/float(nApMass-1))
for j in range(0,NepsBins+1):
	Epsedges.append(10**(epsmin+(j-0.5)*(epsmax-epsmin)/float(NepsBins-1)))

#detectable = TH2F("detectable","detectable",nApMass,massApmin,massApmax,NepsBins,10**epsmin,10**epsmax)
ZRes = TH1F("ZRes","ZRes",nApMass,massApmin*0.6,massApmax*0.6)
ZCut = TH1F("ZCut","ZCut",nApMass,massApmin*0.6,massApmax*0.6)
ApProduced = TH2F("ApProduced","ApProduced",nApMass,Medges,NepsBins,Epsedges)
VProduced = TH2F("VProduced","VProduced",nApMass,Medges,NepsBins,Epsedges)
detectable = TH2F("detectable","detectable",nApMass,Medges,NepsBins,Epsedges)


#Make more intermediate plots
#Cut on A' tuples
#Figure out cuts
#Fix Generate Efficiency Code.
#Obtain Mass Resolution
#Calculate gamma correctly
#Normalize properly
#Do both vector and scalar decays
#Radiative Fraction
#Cleanup Code
#Cleanup Plots


massApArr = []
zresArr = []
zcutArr = []
for i in range(0,nApMass):
	massAp = (massApmax - massApmin)/float(nApMass - 1) * i + massApmin
	massApArr.append(massAp)
	massVarr = []
	massApres = 0.01
	for j in range(0,nVMass):
		#massV = (massVmax - massVmin)/float(nVMass - 1) * j + massVmin
		massV = 0.6*massAp
		massVarr.append(massV)
		massPiarr = []
		massVres = massresfile.Get("mres_l1_p0").GetFunction("pol1").Eval(massV)
		#zcut = 10.
		breakz = tailsfile.Get("breakz").GetFunction("pol3").Eval(massV)
		length = tailsfile.Get("length").GetFunction("pol3").Eval(massV)

		frame = uncVZ.frame()
		dataInRange = dataset.reduce(obs,"abs({0}-{1})<{2}/2*({3}+{4}*uncVZ)".format("uncM",massV,masscut_nsigma,massVres,0))
		binnedData = dataInRange.binnedClone()
		binnedData.plotOn(frame)
		mean = binnedData.mean(uncVZ)
		sigma = binnedData.sigma(uncVZ)
		uncVZ.setRange("fitRange",mean-2*sigma,mean+2*sigma)
		gauss_params.setRealValue("mean",mean)
		gauss_params.setRealValue("sigma",sigma)
		gauss_pdf.fitTo(binnedData,RooFit.Range("fitRange"),RooFit.PrintLevel(-1))
		mean = gauss_params.getRealValue("mean")
		sigma = gauss_params.getRealValue("sigma")
		gaussexp_params.setRealValue("gauss_mean",mean)
		gaussexp_params.setRealValue("gauss_sigma",sigma)
		gaussexp_params.setRealValue("exp_breakpoint",breakz)
		gaussexp_params.setRealValue("exp_length",length)
		w.var("gauss_mean").setConstant(True)
		w.var("gauss_sigma").setConstant(True)
		w.var("exp_breakpoint").setConstant(True)
		w.var("exp_length").setConstant(True)
		func = gaussexp_pdf.createCdf(obs).asTF(RooArgList(obs),RooArgList(gaussexp_params))
		zcut_frac = zcut_count/(dataInRange.sumEntries()*scale)
		zcut = func.GetX(1-zcut_frac,0,50)
		ZRes.SetBinContent(i+1,sigma)
		ZCut.SetBinContent(i+1,zcut)
		#zresArr.append(sigma)
		#zcutArr.append(zcut)

		#fitfunc.SetParameters(1.0,mean,sigma,breakz,length)
		for k in range(0,nPiMass):
			#massPi = (massPimax - massPimin)/float(nPiMass - 1) * k + massPimin
			massPi = massAp/3.
			massPiarr.append(massPi)
			fpiarr = []
			for l in range(0,Nfpi):
				#fPi = (fpimax - fpimin)/float(Nfpi -1) * l + fpimin
				fPi = massPi/3.
				fpiarr.append(fPi)
				alphadarr = []
				for m in range(0,Nalphad):
					#alphaD = (alphadmax - alphadmin)/float(Nalphad - 1) * m + alphadmin
					alphaD = 0.01
					alphadarr.append(alphaD)
					epsarr = []
					for n in range(0,NepsBins):
						logeps = (epsmax - epsmin)/float(NepsBins - 1) * n + epsmin
						eps = 10**logeps
						epsarr.append(eps)
						ct = ctau(massAp,massPi,massV,eps,alphaD,fPi,m_l,False)
						gammact = ct * Ebeam * gamma/massV
						eff = 0.05
						deltaM = 0.001
						#events.Draw("{0}>>massAp(100,{1}-{2},{1}+{2})".format("uncM",massAp,0.5*deltaM),"abs({0}-{1})<{2}".format("uncM",massAp,0.5*deltaM),"")
						eventsrad.Draw("{0}>>massAp(100,{1}-{2},{1}+{2})".format("triPair1M",massAp,0.5*deltaM),"abs({0}-{1})<{2}".format("triPair1M",massAp,0.5*deltaM),"")
						#num_pairs = gDirectory.Get("massAp").GetEntries() * scale * 5.
						#rad_frac = 0.15
						#num_rad = num_pairs * rad_frac
						num_rad = gDirectory.Get("massAp").GetEntries() * 7089/(1.92 * 99) #* scale
						ap_yield = 3*np.pi/(2*(1/137.0))*num_rad*(massAp/deltaM)*eps**2
						brVpi_rho = br_Vpi(massAp,massPi,massV,alphaD,fPi,False,True)
						#events.Draw("{0}>>massV(100,{1}-{2},{1}+{2})".format("uncM",massV,0.5*deltaM),"abs({0}-{1})<{2}".format("uncM",massV,0.5*deltaM),"")
						#rho_yield = gDirectory.Get("massV").GetEntries() * scale
						rho_yield = brVpi_rho * ap_yield
						ApProduced.Fill(massAp,eps,ap_yield)
						VProduced.Fill(massAp,eps,rho_yield)
						detectable.Fill(massAp,eps,rho_yield * integrate(zcut,maxZ,1000,targetz,gammact,massV,efffile))






nBins = 50
minRatio = 1
maxRatio = 13
minMass = 0.01
maxMass = 1

brVpi1 = TH1F("brVpi1","brVpi1",nBins,minRatio,maxRatio)
brVpi2 = TH1F("brVpi2","brVpi2",nBins,minRatio,maxRatio)
brrhophipi1 = TH1F("brrhophipi1","brrhophipi1",nBins,minRatio,maxRatio)
brrhophipi2 = TH1F("brrhophipi2","brrhophipi2",nBins,minRatio,maxRatio)
brpipi1 = TH1F("brpipi1","brpipi1",nBins,minRatio,maxRatio)
brpipi2 = TH1F("brpipi2","brpipi2",nBins,minRatio,maxRatio)
brVV = TH1F("brVV","brVV",nBins,minRatio,maxRatio)

dlrho = TH1F("dlrho","dlrho",nBins,minMass,maxMass)
dlphi = TH1F("dlphi","dlphi",nBins,minMass,maxMass)

for i in range(nBins):
	m_pi = 0.02
	m_Ap = 3*m_pi
	ratio1 = 1.4
	ratio2 = 1.8
	m_V1 = m_pi*ratio1
	m_V2 = m_pi*ratio2
	ratio = (maxRatio-minRatio)/float(nBins) * i + minRatio
	f_pi = m_pi/ratio
	rate1 = rate_Vpi(m_Ap,m_pi,m_V1,alpha_D,f_pi,False,False) + rate_2pi(m_Ap,m_pi,m_V1,alpha_D) + rate_2V(m_Ap,m_V1,alpha_D)
	rate2 = rate_Vpi(m_Ap,m_pi,m_V2,alpha_D,f_pi,False,False) + rate_2pi(m_Ap,m_pi,m_V2,alpha_D)
	brVpi1.SetBinContent(i+1,rate_Vpi(m_Ap,m_pi,m_V1,alpha_D,f_pi,False,False)/rate1)
	brVpi2.SetBinContent(i+1,rate_Vpi(m_Ap,m_pi,m_V2,alpha_D,f_pi,False,False)/rate2)
	brrhophipi1.SetBinContent(i+1,(rate_Vpi(m_Ap,m_pi,m_V1,alpha_D,f_pi,True,False)+rate_Vpi(m_Ap,m_pi,m_V1,alpha_D,f_pi,False,True))/rate1)
	brrhophipi2.SetBinContent(i+1,(rate_Vpi(m_Ap,m_pi,m_V2,alpha_D,f_pi,True,False)+rate_Vpi(m_Ap,m_pi,m_V2,alpha_D,f_pi,False,True))/rate2)
	brpipi1.SetBinContent(i+1,rate_2pi(m_Ap,m_pi,m_V1,alpha_D)/rate1)
	brpipi2.SetBinContent(i+1,rate_2pi(m_Ap,m_pi,m_V2,alpha_D)/rate2)
	brVV.SetBinContent(i+1,rate_2V(m_Ap,m_V1,alpha_D)/rate1)

for i in range(nBins):
	eps = 0.001
	m_l = 0.000511
	m_V = (maxMass-minMass)/float(nBins) * i + minMass
	m_pi = m_V/1.8
	m_Ap = 3*m_pi
	f_pi = m_pi/3
	dlrho.SetBinContent(i+1,ctau(m_Ap,m_pi,m_V,eps,alpha_D,f_pi,m_l,True))
	dlphi.SetBinContent(i+1,ctau(m_Ap,m_pi,m_V,eps,alpha_D,f_pi,m_l,False))

openPDF(outfile,c)
detectable.Draw("COLZ")
nlevels = 3
minValue = 2.3#detectable.GetMinimum(0)
bottom = int(np.floor(np.log10(minValue)))
limitLevels = array.array('d')
for i in range(bottom,bottom+nlevels):
	for j in range(1,10):
		limitLevels.append((10**i)*j)
#detectable.SetContour(len(limitLevels),limitLevels)
#detectable.GetXaxis().SetMoreLogLabels()
#detectable.GetXaxis().SetTitle("mass [GeV]")
#detectable.GetYaxis().SetTitle("epsilon^2")
#detectable.Draw("cont1z")
#detectable.GetZaxis().SetRangeUser(10**(bottom-nlevels),10**bottom)
c.SetLogx(1)
c.SetLogy(1)
c.Print(outfile+".pdf")
ApProduced.Draw("COLZ")
c.Print(outfile+".pdf")
VProduced.Draw("COLZ")
c.Print(outfile+".pdf")
c.SetLogx(0)
c.SetLogy(0)
ZRes.Draw()
c.Print(outfile+".pdf")
ZCut.Draw()
c.Print(outfile+".pdf")
saveHisto(brVpi1,outfile,c,"m_pi/f_pi","Branching Ratio V_pi","m_Ap/m_pi = 3; m_V/m_pi = 1.4",0,1)
saveHisto(brVpi2,outfile,c,"m_pi/f_pi","Branching Ratio V_pi","m_Ap/m_pi = 3; m_V/m_pi = 1.8",0,1)
saveHisto(brrhophipi1,outfile,c,"m_pi/f_pi","Branching Ratio rho pi + phi pi","m_Ap/m_pi = 3; m_V/m_pi = 1.4",0,1)
saveHisto(brrhophipi2,outfile,c,"m_pi/f_pi","Branching Ratio rho pi + phi pi","m_Ap/m_pi = 3; m_V/m_pi = 1.8",0,1)
saveHisto(brpipi1,outfile,c,"m_pi/f_pi","Branching Ratio 2pi","m_Ap/m_pi = 3; m_V/m_pi = 1.4",0,1)
saveHisto(brpipi2,outfile,c,"m_pi/f_pi","Branching Ratio 2pi","m_Ap/m_pi = 3; m_V/m_pi = 1.8",0,1)
saveHisto(brVV,outfile,c,"m_pi/f_pi","Branching Ratio 2V","m_Ap/m_pi = 3; m_V/m_pi = 1.4",0,1)
saveHisto(dlrho,outfile,c,"m_V [GeV]","rho c tau [cm]","m_Ap/m_pi = 3; m_V/m_pi = 1.8; m_pi/f_pi = 3",0,1,1)
saveHisto(dlphi,outfile,c,"m_V [GeV]","phi c tau [cm]","m_Ap/m_pi = 3; m_V/m_pi = 1.8; m_pi/f_pi = 3",0,1,1)
closePDF(outfile,c)