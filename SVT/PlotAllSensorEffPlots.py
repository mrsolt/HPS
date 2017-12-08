import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend
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

def drawHisto(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	histo.Draw("COLZ")
	histo.SetTitle(histo.GetTitle())
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)

def saveHisto(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	drawHisto(histo,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.Print(outfile+".pdf")

def Plot(var,sensors,infile,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	openPDF(outfile,canvas)
	for i in range(len(sensors)):
		saveHisto(getHisto("{0} {1}".format(var,sensors[i]),infile),outfile,canvas,XaxisTitle,YaxisTitle,plotTitle,stats)
	closePDF(outfile,canvas)

def PlotVars(plotvars,sensors,infile,outfile,stats=0):
	c = TCanvas("c","c",800,600)
	for i in range(len(plotvars)):
		outputfile = outfile+"_"+plotvars[i]
		Plot("{0}".format(plotvars[i]),sensors,infile,outputfile,c,plotvars[i],"",plotvars[i],stats)	
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
	plotvars.append("Residual U")
	plotvars.append("Residual U Electron")
	plotvars.append("Residual U Positron")
	plotvars.append("Residual U vs V")
	plotvars.append("Residual U vs V Electron")
	plotvars.append("Residual U vs V Positron")
	plotvars.append("U Pulls")
	plotvars.append("U Pulls Electron")
	plotvars.append("U Pulls Positron")
	plotvars.append("U Pulls vs V")
	plotvars.append("U Pulls vs V Electron")
	plotvars.append("U Pulls vs V Positron")
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

sensors = buildSensorArray(isL0)
plotvars = buildVariableArray()

PlotVars(plotvars,sensors,infile,outfile)