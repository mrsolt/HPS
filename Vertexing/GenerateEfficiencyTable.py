#!/usr/bin/env python
#Author Matt Solt mrsolt@slac.stanford.edu
import sys
import array, math
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, TH1F, TLegend
import getopt

def print_usage():
    print "\nUsage: {0} <output file basename> <acceptance ROOT files>".format(sys.argv[0])
    print "Arguments: "
    print '\t-e: use this beam energy'
    print '\t-t: use this target position'
    print '\t-n: number of bins in histograms'
    print '\t-z: total range in z covered'
    print '\t-T: plot Test plots'
    print '\t-h: this help message'
    print

#Default Values
eBeam=1.056
makeTestPlots = False
targZ = -5.
nBins = 50
zRange = 100

#Function to plot efficiency tests of known masses
def plotTest(iMass,inputFile,output,targZ,maxZ):
    inputfile = open(inputFile,"r")
    mass = []
    z = []
    result = []
    eff = []
    #Readlines from input file
    lines = inputfile.readlines()
    for x in lines:
        result.append(x.split())
    inputfile.close()
    nMass = len(result[0])
    nBins = len(result[1])
    #Grab Array of Masses
    for i in range(nMass):
        mass.append(float(result[0][i]))
    #Grab Array of z's
    for i in range(nBins):
        z.append(float(result[1][i]))
    #Convert the strings from input file into floats
    for i in range(nMass):
	dummy = []
	for j in range(nBins):
	    dummy.append(float(result[i+2][j]))
	eff.append(dummy)
	del dummy
    #define histograms
    histo1 = TH1F("histo1","histo1",nBins-1,targZ,maxZ) #test histogram
    histo2 = TH1F("histo2","histo2",nBins,targZ,maxZ) #known histogram
    #Use the mass greater than and less than the mass of interest
    iMass1 = iMass - 1
    iMass2 = iMass + 1
    for i in range(nBins-1):
	iZ1 = i
	iZ2 = i + 1
        Q11 = eff[iMass1][iZ1]
	Q12 = eff[iMass2][iZ1]
	Q21 = eff[iMass1][iZ2]
	Q22 = eff[iMass2][iZ2]
        #Interpolate value
        interpolate = Bilinear(z[i],mass[iMass],z[iZ1],z[iZ2],mass[iMass1],mass[iMass2],Q11,Q12,Q21,Q22)
        histo1.SetBinContent(i,interpolate)
    for i in range(nBins):
	histo2.SetBinContent(i,eff[iMass][i])
    #Draw Histograms
    legend = TLegend(.68,.66,.92,.87)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)
    legend.AddEntry(histo1,"Extrapolation","LP")
    legend.AddEntry(histo2,"MC","LP")
    maximum = histo1.GetMaximum()
    if(histo2.GetMaximum() > maximum): maximum = histo2.GetMaximum()
    histo1.Draw("")
    histo1.GetXaxis().SetTitle("z [mm]")
    histo1.SetTitle("A' Efficiency " + str(mass[iMass]) + " GeV")
    histo1.GetYaxis().SetRangeUser(0,maximum*1.2)
    histo2.Draw("same")
    histo2.SetLineColor(2)
    legend.Draw("")
    gStyle.SetOptStat(0)
    c.Print(output+".pdf")

#Function to plot efficiency tests of known masses
def Interpolate(Mass,Z,mass,z,eff):
    iMass = 0
    iZ = 0
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

datafile=""
options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:t:n:z:Th')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-e':
            eBeam=float(arg)
	if opt=='-t':
            targZ=float(arg)
	if opt=='-n':
            nBins=int(arg)
	if opt=='-z':
            zRange=float(arg)
	if opt=='-T':
	    makeTestPlots = True
        if opt=='-h':
            print_usage()
            sys.exit(0)

if len(remainder)!=2:
    print_usage()
    sys.exit(0)

gROOT.SetBatch(True)
maxZ = targZ + zRange #Define Maximum Z

#Set outfile and grab infile
outfile = remainder[0]
inputfile = open(remainder[1],"r")

reconFiles=[]

#Read files from input text file
for line in (raw.strip().split() for raw in inputfile):
            reconFiles.append(line[0])

mass = array.array('d')
z = array.array('d')
nMass = len(reconFiles)/2

#Grab values of mass from the truth in the tuple files
for i in range(nMass):
    inputReconFile = TFile(str(reconFiles[i]))
    inputReconFile.Get("cut").Draw("triM>>histoMass({0},{1},{2})".format(1000,0,1))
    histoMass = ROOT.gROOT.FindObject("histoMass")
    mass.append(histoMass.GetMean())
    del histoMass

#Build array of z values
for i in range(nBins):
    z.append(targZ+i*(maxZ-targZ)/float(nBins))

#Create text file to write to
textfile = open(outfile + ".eff","w")

#Write values of mass in the first row
for i in range(nMass):
    textfile.write(str(mass[i]) + " ")
textfile.write("\n")
#Write values of z in the 2nd row
for i in range(nBins):
    textfile.write(str(z[i]) + " ")  
textfile.write("\n")

#Loop over all values of mass
for i in range(nMass):
    inputReconFile = TFile(str(reconFiles[i])) #tuple files after cuts
    inputTruthFile = TFile(str(reconFiles[i+nMass])) #truth files
    inputReconFile.Get("cut").Draw("triEndZ>>histoRecon({0},{1},{2})".format(nBins,targZ,maxZ),"triP>0.8*{0}".format(eBeam))
    histoRecon = ROOT.gROOT.FindObject("histoRecon")
    inputTruthFile.Get("ntuple").Draw("triEndZ>>histoTruth({0},{1},{2})".format(nBins,targZ,maxZ),"triP>0.8*{0}".format(eBeam))
    histoTruth = ROOT.gROOT.FindObject("histoTruth")
    #Write the efficiency for a given mass (row) as function of z
    for j in range(nBins):
        if (histoTruth.GetBinContent(j+1) == 0): textfile.write(str(0))
        else: textfile.write(str(histoRecon.GetBinContent(j+1)/histoTruth.GetBinContent(j+1)) + " ")
    textfile.write("\n")

textfile.close()

#Make test plots if desired
if(makeTestPlots):
    c = TCanvas("c","c",1200,900)
    c.Print(outfile+".pdf[")

    for i in range(1,nMass-1):
        plotTest(i,outfile+".eff",outfile,targZ,maxZ)

    c.Print(outfile+".pdf]")