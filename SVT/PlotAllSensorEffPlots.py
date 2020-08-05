import sys
import numpy as np
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

isL0 = False

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-l: if file uses L0 detector'
    print '\t-h: this help message'
    print

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hl')

# Parse the command line arguments
for opt, arg in options:
		if opt=='l':
			isL0 = True
		if opt=='-h':
			print_usage()
			sys.exit(0)


outfile = remainder[0]
infile = TFile(remainder[1])

def openPDF(outfile,canvas):
	canvas.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	canvas.Print(outfile+".pdf]")

def getHisto(histoTitle,infile):
	histo = infile.Get(histoTitle)
	return histo

def drawHisto(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,title=False,errors=True):
	if(errors): histo.Draw("COLZ")
	else: histo.Draw("HIST")

	if(not title): histo.SetTitle(histo.GetTitle())
	else: histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)

def saveHisto(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,title=False,errors=True):
	drawHisto(histo,XaxisTitle,YaxisTitle,plotTitle,stats,title,errors)
	canvas.Print(outfile+".pdf")

def saveHisto2(histo1,histo2,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,title=False,errors=True):
	drawHisto(histo1,XaxisTitle,YaxisTitle,plotTitle,stats,title,errors)
	histo1.SetAxisRange(0,1.2,"Y")
	histo2.Draw("same")
	histo2.SetLineColor(2)
	canvas.Print(outfile+".pdf")

def Plot(var,sensors,infile,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	openPDF(outfile,canvas)
	for i in range(len(sensors)):
		saveHisto(getHisto("{0} {1}".format(var,sensors[i]),infile),outfile,canvas,XaxisTitle,YaxisTitle,plotTitle,stats)
	closePDF(outfile,canvas)

def Fit(var,sensors,infile,outfile,canvas,top,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	ex = "Null Fit"
	volume = "Top"
	if(not top): volume = "Bottom"
	histoMean = TH1F("histoMean","histoMean",len(sensors),0,len(sensors))
	histoSigma = TH1F("histoSigma","histoSigma",len(sensors),0,len(sensors))
	openPDF(outfile,canvas)
	for i in range(len(sensors)):
		histo = getHisto("{0} {1}".format(var,sensors[i]),infile)
		histoFit = histo.Fit("gaus","S")
		saveHisto(histo,outfile,canvas,XaxisTitle,YaxisTitle,plotTitle,stats)
		mean = 0
		meanErr = 0
		sigma = 0
		sigmaErr = 0
		try:
			mean = histoFit.Parameter(1)
			meanErr = histoFit.ParError(1)
			sigma = histoFit.Parameter(2)
			sigmaErr = histoFit.ParError(2)
		except Exception as ex:
			print(ex)
		#for j in range(len(sensors)):
		histoMean.SetBinContent(i+1,mean)
		histoMean.SetBinError(i+1,meanErr)
		histoSigma.SetBinContent(i+1,sigma)
		histoSigma.SetBinError(i+1,sigmaErr)
		del histo
		del histoFit
	titleMean = plotTitle+" Mean "+volume
	titleSigma = plotTitle+" Sigma "+volume
	saveHisto(histoMean,outfile,canvas,"sensor ID","",titleMean,0,True)
	saveHisto(histoSigma,outfile,canvas,"sensor ID","",titleSigma,0,True)
	closePDF(outfile,canvas)
	del histoMean
	del histoSigma

def PlotVars(plotvars,sensors,infile,outfile,stats=0):
	c = TCanvas("c","c",800,600)
	for i in range(len(plotvars)):
		outputfile = outfile+"_"+plotvars[i]
		Plot("{0}".format(plotvars[i]),sensors,infile,outputfile,c,plotvars[i],"",plotvars[i],stats)	
	del c

def FitVars(fitvars,sensors,infile,outfile,top,stats=0):
	c = TCanvas("c","c",800,600)
	volume = "Top"
	if(not top): volume = "Bottom"
	for i in range(len(fitvars)):
		outputfile = outfile+"_"+fitvars[i]+"_fits_"+volume
		Fit("{0}".format(fitvars[i]),sensors,infile,outputfile,c,top,fitvars[i],"",fitvars[i],stats)	
	del c

def PlotEff(EffArr,sensors,infile,outfile,top,stats=0):
	c = TCanvas("c","c",800,600)
	volume = "Top"
	if(not top): volume = "Bottom"
	outputfile = outfile+"_"+"eff_"+volume
	openPDF(outputfile,c)	
	for i in range(len(EffArr)):
		histo = TH1F("{0} {1}".format(EffArr[i],volume),"{0} {1}".format(EffArr[i],volume),len(sensors),0,len(sensors))
		for j in range(len(sensors)):
			eff = getHisto("{0} {1}".format(EffArr[i],sensors[j]),infile)
			effErr = getHisto("{0} Error {1}".format(EffArr[i],sensors[j]),infile)
			histo.SetBinContent(j+1,eff.GetBinContent(1))
			histo.SetBinError(j+1,effErr.GetBinContent(1))
		saveHisto(histo,outputfile,c,"sensor ID","","{0} {1}".format(EffArr[i],volume),stats,True)
		del histo
	closePDF(outputfile,c)	
	del c

def FitVars2D(fitvars2D,sensors,infile,outfile,stats=0):
	c = TCanvas("c","c",800,600)
	for i in range(len(fitvars2D)):
		outputfile = outfile+"_"+fitvars2D[i]+"_fits_"
		Fit2D("{0}".format(fitvars[i]),sensors,infile,outputfile,c,top,fitvars2D[i],"",fitvars2D[i],stats)	
	del c

def Fit2D(var,sensors,infile,outfile,canvas,top,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	ex = "Null Fit"
	histoMean = TH1F("histoMean","histoMean",len(sensors),0,len(sensors))
	histoSigma = TH1F("histoSigma","histoSigma",len(sensors),0,len(sensors))
	openPDF(outfile,canvas)
	for i in range(len(sensors)):
		histo = getHisto("{0} {1}".format(var,sensors[i]),infile)
		histoFit = histo.Fit("gaus","S")
		saveHisto(histo,outfile,canvas,XaxisTitle,YaxisTitle,plotTitle,stats)
		mean = 0
		meanErr = 0
		sigma = 0
		sigmaErr = 0
		try:
			mean = histoFit.Parameter(1)
			meanErr = histoFit.ParError(1)
			sigma = histoFit.Parameter(2)
			sigmaErr = histoFit.ParError(2)
		except Exception as ex:
			print(ex)
		#for j in range(len(sensors)):
		histoMean.SetBinContent(i+1,mean)
		histoMean.SetBinError(i+1,meanErr)
		histoSigma.SetBinContent(i+1,sigma)
		histoSigma.SetBinError(i+1,sigmaErr)
		del histo
		del histoFit
	titleMean = plotTitle+" Mean "+volume
	titleSigma = plotTitle+" Sigma "+volume
	saveHisto(histoMean,outfile,canvas,"sensor ID","",titleMean)
	saveHisto(histoSigma,outfile,canvas,"sensor ID","",titleSigma)
	closePDF(outfile,canvas)
	del histoMean
	del histoSigma

def ms(p,beta,t,z):
	return 0.0136/(beta*p)*z*np.sqrt(t)*(1+0.038*np.log(t))

def theta_Si(p,t):
	return ms(p,1,t,1)

def extrap_error(p,t,d):
	#return 1/np.sqrt(3)*theta_Si(p,t)*d
	return theta_Si(p,t)*d

def ms_histo(t,layer,maxP):
	nBins = 500
	minP = 0.
	d1 = 0
	d2 = 0
	histo = TH1F("histo","histo",nBins,minP,maxP)
	dp = (maxP - minP)/(nBins - 1)
	for i in range(nBins):
		p = dp * i + minP + dp/2.
		if(layer == 1):
			d1 = 100
			d2 = 0
		if(layer == 2):
			d1 = 100
			d2 = 100
		if(layer == 3):
			d1 = 100
			d2 = 200
		if(layer == 4):
			d1 = 200
			d2 = 200
		if(layer == 5):
			d1 = 200
			d2 = 200
		if(layer == 6):
			d1 = 200
			d2 = 0

		extrap_error1 = extrap_error(p,t,d1)
		extrap_error2 = extrap_error(p,t,d2)
		error = 0
		if(extrap_error2 == 0):
			error = extrap_error1
		else:
			error = 1/np.sqrt(1/extrap_error1**2 + 1/extrap_error2**2)
		histo.Fill(p,error)
	return histo

def save_ms_histo(sensors,infile,outfile,stats=0):
	c = TCanvas("c","c",800,600)
	outputfile = outfile+"_"+"ms"
	openPDF(outputfile,c)
	t = 0.007
	d = 100	
	for i in range(len(sensors)):
		histo = getHisto("Error U vs P {0}".format(sensors[i]),infile)
		proj = histo.ProjectionX("proj")
		nBins = proj.GetNbinsX()
		maxP = proj.GetBinLowEdge(nBins+2)
		histoproj = TH1F("histoproj","histoproj",nBins,0,maxP)
		layer = 0
		if(i >= 0 and i <=3): layer = 1
		if(i >= 4 and i <=7): layer = 2
		if(i >= 8 and i <=11): layer = 3
		if(i >= 12 and i <=19): layer = 4
		if(i >= 20 and i <=27): layer = 5
		if(i >= 28 and i <=35): layer = 6
		for j in range(nBins):
			histoproj.SetBinContent(j+1,histo.ProjectionX("h",j+1,j+2).GetMean())
		saveHisto2(ms_histo(t,layer,maxP),histoproj,outputfile,c,"p [GeV]","error U [mm]","Calculated Error as Function of P {0}".format(sensors[i]),stats,True,False)
		del histo
		del histoproj
	closePDF(outputfile,c)	
	del c

def buildSensorArray(isL0):
	sensors = []
	if(not isL0):
		sensors.append("module_L1b_halfmodule_axial_sensor0")
		sensors.append("module_L1b_halfmodule_stereo_sensor0")
		sensors.append("module_L1t_halfmodule_axial_sensor0")
		sensors.append("module_L1t_halfmodule_stereo_sensor0")
		sensors.append("module_L2b_halfmodule_axial_sensor0")
		sensors.append("module_L2b_halfmodule_stereo_sensor0")
		sensors.append("module_L2t_halfmodule_axial_sensor0")
		sensors.append("module_L2t_halfmodule_stereo_sensor0")
		sensors.append("module_L3b_halfmodule_axial_sensor0")
		sensors.append("module_L3b_halfmodule_stereo_sensor0")
		sensors.append("module_L3t_halfmodule_axial_sensor0")
		sensors.append("module_L3t_halfmodule_stereo_sensor0")
		sensors.append("module_L4b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L4b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L4b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L4b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L4t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L4t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L4t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L4t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L5b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L5b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L5b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L5b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L5t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L5t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L5t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L5t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L6b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L6b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L6b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L6b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L6t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L6t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L6t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L6t_halfmodule_stereo_slot_sensor0")

	else:
		sensors.append("module_L1b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L1b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L1b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L1b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L1t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L1t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L1t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L1t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L2b_halfmodule_axial_sensor0")
		sensors.append("module_L2b_halfmodule_stereo_sensor0")
		sensors.append("module_L2t_halfmodule_axial_sensor0")
		sensors.append("module_L2t_halfmodule_stereo_sensor0")
		sensors.append("module_L3b_halfmodule_axial_sensor0")
		sensors.append("module_L3b_halfmodule_stereo_sensor0")
		sensors.append("module_L3t_halfmodule_axial_sensor0")
		sensors.append("module_L3t_halfmodule_stereo_sensor0")
		sensors.append("module_L4b_halfmodule_axial_sensor0")
		sensors.append("module_L4b_halfmodule_stereo_sensor0")
		sensors.append("module_L4t_halfmodule_axial_sensor0")
		sensors.append("module_L4t_halfmodule_stereo_sensor0")
		sensors.append("module_L5b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L5b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L5b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L5b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L5t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L5t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L5t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L5t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L6b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L6b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L6b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L6b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L6t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L6t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L6t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L6t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L7b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L7b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L7b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L7b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L7t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L7t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L7t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L7t_halfmodule_stereo_slot_sensor0")
	return sensors

def buildSensorArrayTop(isL0):
	sensors = []
	if(not isL0):
		sensors.append("module_L1t_halfmodule_axial_sensor0")
		sensors.append("module_L1t_halfmodule_stereo_sensor0")
		sensors.append("module_L2t_halfmodule_axial_sensor0")
		sensors.append("module_L2t_halfmodule_stereo_sensor0")
		sensors.append("module_L3t_halfmodule_axial_sensor0")
		sensors.append("module_L3t_halfmodule_stereo_sensor0")
		sensors.append("module_L4t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L4t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L4t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L4t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L5t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L5t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L5t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L5t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L6t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L6t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L6t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L6t_halfmodule_stereo_slot_sensor0")

	else:
		sensors.append("module_L1t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L1t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L1t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L1t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L2t_halfmodule_axial_sensor0")
		sensors.append("module_L2t_halfmodule_stereo_sensor0")
		sensors.append("module_L3t_halfmodule_axial_sensor0")
		sensors.append("module_L3t_halfmodule_stereo_sensor0")
		sensors.append("module_L4t_halfmodule_axial_sensor0")
		sensors.append("module_L4t_halfmodule_stereo_sensor0")
		sensors.append("module_L5t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L5t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L5t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L5t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L6t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L6t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L6t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L6t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L7t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L7t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L7t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L7t_halfmodule_stereo_slot_sensor0")
	return sensors

def buildSensorArrayBot(isL0):
	sensors = []
	if(not isL0):
		sensors.append("module_L1b_halfmodule_axial_sensor0")
		sensors.append("module_L1b_halfmodule_stereo_sensor0")
		sensors.append("module_L2b_halfmodule_axial_sensor0")
		sensors.append("module_L2b_halfmodule_stereo_sensor0")
		sensors.append("module_L3b_halfmodule_axial_sensor0")
		sensors.append("module_L3b_halfmodule_stereo_sensor0")
		sensors.append("module_L4b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L4b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L4b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L4b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L5b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L5b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L5b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L5b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L6b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L6b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L6b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L6b_halfmodule_stereo_slot_sensor0")

	else:
		sensors.append("module_L1b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L1b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L1b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L1b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L2b_halfmodule_axial_sensor0")
		sensors.append("module_L2b_halfmodule_stereo_sensor0")
		sensors.append("module_L3b_halfmodule_axial_sensor0")
		sensors.append("module_L3b_halfmodule_stereo_sensor0")
		sensors.append("module_L4b_halfmodule_axial_sensor0")
		sensors.append("module_L4b_halfmodule_stereo_sensor0")
		sensors.append("module_L5b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L5b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L5b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L5b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L6b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L6b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L6b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L6b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L7b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L7b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L7b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L7b_halfmodule_stereo_slot_sensor0")
	return sensors

def buildVariableArray():
	plotvars = []
	plotvars.append("D0 Error")
	plotvars.append("Z0 Error")
	plotvars.append("Omega Error")
	plotvars.append("TanLambda Error")
	plotvars.append("Phi0 Error")
	plotvars.append("Error U")
	plotvars.append("Error U Electron")
	plotvars.append("Error U Positron")
	plotvars.append("Error U vs V")
	plotvars.append("Error U vs V Electron")
	plotvars.append("Error U vs V Positron")
	plotvars.append("Error U vs U")
	plotvars.append("Error U vs U Electron")
	plotvars.append("Error U vs U Positron")
	plotvars.append("Error U vs P")
	plotvars.append("Error U vs P Electron")
	plotvars.append("Error U vs P Positron")
	plotvars.append("Residual U")
	plotvars.append("Residual U Electron")
	plotvars.append("Residual U Positron")
	plotvars.append("Residual U vs V")
	plotvars.append("Residual U vs V Electron")
	plotvars.append("Residual U vs V Positron")
	plotvars.append("Residual U vs U")
	plotvars.append("Residual U vs U Electron")
	plotvars.append("Residual U vs U Positron")
	plotvars.append("Residual U vs P")
	plotvars.append("Residual U vs P Electron")
	plotvars.append("Residual U vs P Positron")
	plotvars.append("U Pulls")
	plotvars.append("U Pulls Electron")
	plotvars.append("U Pulls Positron")
	plotvars.append("U Pulls vs V")
	plotvars.append("U Pulls vs V Electron")
	plotvars.append("U Pulls vs V Positron")
	plotvars.append("U Pulls vs U")
	plotvars.append("U Pulls vs U Electron")
	plotvars.append("U Pulls vs U Positron")
	plotvars.append("U Pulls vs P")
	plotvars.append("U Pulls vs P Electron")
	plotvars.append("U Pulls vs P Positron")
	plotvars.append("HitEfficiency Channel Corrected")
	plotvars.append("HitEfficiency Channel Corrected Ele")
	plotvars.append("HitEfficiency Channel Corrected Pos")
	plotvars.append("HitEfficiency P Corrected")
	plotvars.append("HitEfficiency P Corrected Ele")
	plotvars.append("HitEfficiency P Corrected Pos")
	plotvars.append("HitEfficiency Y Corrected")
	plotvars.append("HitEfficiency Y Corrected Ele")
	plotvars.append("HitEfficiency Y Corrected Pos")
	plotvars.append("HitEfficiency Channel")
	plotvars.append("HitEfficiency Channel Ele")
	plotvars.append("HitEfficiency Channel Pos")
	plotvars.append("HitEfficiency P")
	plotvars.append("HitEfficiency P Ele")
	plotvars.append("HitEfficiency P Pos")
	plotvars.append("HitEfficiency Y")
	plotvars.append("HitEfficiency Y Ele")
	plotvars.append("HitEfficiency Y Pos")
	return plotvars

def buildFitArray():
	fitvars = []
	fitvars.append("Residual U")
	fitvars.append("Residual U Electron")
	fitvars.append("Residual U Positron")
	fitvars.append("U Pulls")
	fitvars.append("U Pulls Electron")
	fitvars.append("U Pulls Positron")
	return fitvars

def buildFit2DArray():
	fitvars2D = []
	fitvars2D.append("Residual U vs V")
	fitvars2D.append("Residual U vs V Electron")
	fitvars2D.append("Residual U vs V Positron")
	fitvars2D.append("Residual U vs U")
	fitvars2D.append("Residual U vs U Electron")
	fitvars2D.append("Residual U vs U Positron")
	fitvars2D.append("Residual U vs P")
	fitvars2D.append("Residual U vs P Electron")
	fitvars2D.append("Residual U vs P Positron")
	fitvars2D.append("U Pulls vs V Electron")
	fitvars2D.append("U Pulls vs V Positron")
	fitvars2D.append("U Pulls vs U")
	fitvars2D.append("U Pulls vs U Electron")
	fitvars2D.append("U Pulls vs U Positron")
	fitvars2D.append("U Pulls vs P")
	fitvars2D.append("U Pulls vs P Electron")
	fitvars2D.append("U Pulls vs P Positron")
	return fitvars2D

def buildEffArray():
	EffArr = []
	EffArr.append("Total Eff")
	EffArr.append("Total Eff Ele")
	EffArr.append("Total Eff Pos")
	EffArr.append("Total Corrected Eff")
	EffArr.append("Total Corrected Eff Ele")
	EffArr.append("Total Corrected Eff Pos")
	return EffArr

sensors = buildSensorArray(isL0)
sensorsTop = buildSensorArrayTop(isL0)
sensorsBot = buildSensorArrayBot(isL0)
plotvars = buildVariableArray()
fitvars = buildFitArray()
fitvars2D = buildFit2DArray()
EffArr = buildEffArray()

save_ms_histo(sensors,infile,outfile)
#PlotVars(plotvars,sensors,infile,outfile,1)
#FitVars(fitvars,sensorsTop,infile,outfile,True,1)
#FitVars(fitvars,sensorsBot,infile,outfile,False,1)
#PlotEff(EffArr,sensorsTop,infile,outfile,True)
#PlotEff(EffArr,sensorsBot,infile,outfile,False)
#FitVars2D(fitvars2D,sensors,infile,outfile,1)