import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TPad, TLatex
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input Data file> <input MC text file> <input 80 MeV A' file> <input 100 MeV A' file>".format(sys.argv[0])
    print '\t-z: target position (default -4.3 mm)'
    print '\t-l: is L1L2 (default False)'
    print '\t-h: this help message'
    print

zTarg = -4.3
L1L2 = False

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'z:lh')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-l':
			L1L2 = True
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

datafile = TFile(remainder[1])
dataevents = datafile.Get("ntuple")

mcfile = open(remainder[2],"r")
mcFiles = []

for line in (raw.strip().split() for raw in mcfile):
	mcFiles.append(line[0])
mcevents = TChain("ntuple")
for i in range(len(mcFiles)):
    mcevents.Add(mcFiles[i])

ap1file = TFile(remainder[3])
ap1events = ap1file.Get("ntuple")

ap2file = TFile(remainder[4])
ap2events = ap2file.Get("ntuple")

eleisoL1 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))".format(zTarg)
posisoL1 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))".format(zTarg)
eleisoL2 = "eleMinPositiveIsoL2+1/3.*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))".format(zTarg)
posisoL2 = "posMinPositiveIsoL2+1/3.*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))".format(zTarg)

if(not L1L2):
	layercutele = "(eleHasL1&&eleHasL2)"
	layercutpos = "(posHasL1&&posHasL2)"
	eleiso = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))".format(zTarg)
	posiso = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))".format(zTarg)
	truthCutele = "((eleL1tIsGoodTruthHit>-0.5&&eleL1tIsGoodTruthHit<0.5)||(eleL2tIsGoodTruthHit>-0.5&&eleL2tIsGoodTruthHit<0.5)||(eleL1bIsGoodTruthHit>-0.5&&eleL1bIsGoodTruthHit<0.5)||(eleL2bIsGoodTruthHit>-0.5&&eleL2bIsGoodTruthHit<0.5))"
	truthCutpos = "((posL1tIsGoodTruthHit>-0.5&&posL1tIsGoodTruthHit<0.5)||(posL2tIsGoodTruthHit>-0.5&&posL2tIsGoodTruthHit<0.5)||(posL1bIsGoodTruthHit>-0.5&&posL1bIsGoodTruthHit<0.5)||(posL2bIsGoodTruthHit>-0.5&&posL2bIsGoodTruthHit<0.5))"

else:
	layercutele = "(!eleHasL1&&eleHasL2)"
	layercutpos = "(!posHasL1&&posHasL2)"
	eleiso = "eleMinPositiveIsoL2+1/3.*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))".format(zTarg)
	posiso = "posMinPositiveIsoL2+1/3.*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))".format(zTarg)
	truthCutele = "((eleL3tIsGoodTruthHit>-0.5&&eleL3tIsGoodTruthHit<0.5)||(eleL4tIsGoodTruthHit>-0.5&&eleL4tIsGoodTruthHit<0.5)||(eleL3bIsGoodTruthHit>-0.5&&eleL3bIsGoodTruthHit<0.5)||(eleL4bIsGoodTruthHit>-0.5&&eleL4bIsGoodTruthHit<0.5))"
	truthCutpos = "((posL3tIsGoodTruthHit>-0.5&&posL3tIsGoodTruthHit<0.5)||(posL4tIsGoodTruthHit>-0.5&&posL4tIsGoodTruthHit<0.5)||(posL3bIsGoodTruthHit>-0.5&&posL3bIsGoodTruthHit<0.5)||(posL4bIsGoodTruthHit>-0.5&&posL4bIsGoodTruthHit<0.5))"

#eleiso = "eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY)".format(zTarg)
#posiso = "posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY)".format(zTarg)

purityCut = "elePurity>0.99&&posPurity>0.99"

dataevents.Draw("uncVZ:{0}>>eleiso_data(100,-3,7,100,-40,60)".format(eleiso),layercutele)
dataevents.Draw("uncVZ:{0}>>posiso_data(100,-3,7,100,-40,60)".format(posiso),layercutpos)

dataevents.Draw("{0}>>eleisocut_1D_data(100,-3,7)".format(eleiso),layercutele)
dataevents.Draw("{0}>>posisocut_1D_data(100,-3,7)".format(posiso),layercutpos)

if(not L1L2):
	dataevents.Draw("eleMinPositiveIso>>eleiso_1D_data(100,0,10)",layercutele)
	dataevents.Draw("posMinPositiveIso>>posiso_1D_data(100,0,10)",layercutpos)

else:
	dataevents.Draw("eleMinPositiveIsoL2>>eleiso_1D_data(100,0,10)",layercutele)
	dataevents.Draw("posMinPositiveIsoL2>>posiso_1D_data(100,0,10)",layercutpos)

mcevents.Draw("uncVZ:{0}>>eleiso_mc_truth(100,-3,7,100,-40,60)".format(eleiso),truthCutele+"&&"+layercutele)
mcevents.Draw("uncVZ:{0}>>posiso_mc_truth(100,-3,7,100,-40,60)".format(posiso),truthCutpos+"&&"+layercutpos)

mcevents.Draw("{0}>>eleisocut_1D_mc(100,-3,7)".format(eleiso),layercutele)
mcevents.Draw("{0}>>posisocut_1D_mc(100,-3,7)".format(posiso),layercutpos)

if(not L1L2):
	mcevents.Draw("eleMinPositiveIso>>eleiso_1D_mc(100,0,10)",layercutele)
	mcevents.Draw("posMinPositiveIso>>posiso_1D_mc(100,0,10)",layercutpos)

else:
	mcevents.Draw("eleMinPositiveIsoL2>>eleiso_1D_mc(100,0,10)",layercutele)
	mcevents.Draw("posMinPositiveIsoL2>>posiso_1D_mc(100,0,10)",layercutpos)

mcevents.Draw("uncVZ:{0}>>eleiso_mc(100,-3,7,100,-40,60)".format(eleiso),purityCut+"&&"+layercutele)
mcevents.Draw("uncVZ:{0}>>posiso_mc(100,-3,7,100,-40,60)".format(posiso),purityCut+"&&"+layercutpos)

mcevents.Draw("uncVZ>>uncVZ_mc_truth(100,-40,60)","("+truthCutele+"&&"+layercutele+")||("+truthCutpos+"&&"+layercutpos+")")
mcevents.Draw("uncVZ>>uncVZ_mc(100,-40,60)",purityCut)

ap1events.Draw("uncVZ:{0}>>eleiso_ap1(100,-3,7,100,-40,100)".format(eleiso),layercutele)
ap1events.Draw("uncVZ:{0}>>posiso_ap1(100,-3,7,100,-40,100)".format(posiso),layercutpos)
ap1events.Draw("uncVZ>>uncVZ_ap1(100,-40,100)")
if(not L1L2):
	ap1events.Draw("uncVZ>>uncVZ_ap1_isocut(100,-40,100)",eleiso+">0&&"+posiso+">0")
else:
	ap1events.Draw("uncVZ>>uncVZ_ap1_isocut(100,-40,100)","("+eleisoL1+">0&&"+posisoL2+">0)||("+eleisoL2+">0&&"+posisoL1+">0)")
#ap1events.Draw("uncVZ>>uncVZ_ap1_truth(100,-40,100)",truthCutele+"||"+truthCutpos)
#ap1events.Draw("uncVZ>>uncVZ_ap1(100,-40,100)",purityCut)

ap2events.Draw("uncVZ:{0}>>eleiso_ap2(100,-3,7,100,-40,100)".format(eleiso),layercutele)
ap2events.Draw("uncVZ:{0}>>posiso_ap2(100,-3,7,100,-40,100)".format(posiso),layercutpos)
ap2events.Draw("uncVZ>>uncVZ_ap2(100,-40,100)")
if(not L1L2):
	ap2events.Draw("uncVZ>>uncVZ_ap2_isocut(100,-40,100)",eleiso+">0&&"+posiso+">0")
else:
	ap2events.Draw("uncVZ>>uncVZ_ap2_isocut(100,-40,100)","("+eleisoL1+">0&&"+posisoL2+">0)||("+eleisoL2+">0&&"+posisoL1+">0)")
#ap2events.Draw("uncVZ>>uncVZ_ap2_truth(100,-40,100)",truthCutele+"||"+truthCutpos)
#ap2events.Draw("uncVZ>>uncVZ_ap2(100,-40,100)",purityCut)

openPDF(outfile,c)

c.SetLogz(1)

eleiso_data = gDirectory.FindObject("eleiso_data")
posiso_data = gDirectory.FindObject("posiso_data")

eleisocut_1D_data = gDirectory.FindObject("eleisocut_1D_data")
posisocut_1D_data = gDirectory.FindObject("posisocut_1D_data")

eleiso_1D_data = gDirectory.FindObject("eleiso_1D_data")
posiso_1D_data = gDirectory.FindObject("posiso_1D_data")

eleiso_mc_truth = gDirectory.FindObject("eleiso_mc_truth")
posiso_mc_truth = gDirectory.FindObject("posiso_mc_truth")

eleiso_mc = gDirectory.FindObject("eleiso_mc")
posiso_mc = gDirectory.FindObject("posiso_mc")

eleisocut_1D_mc = gDirectory.FindObject("eleisocut_1D_mc")
posisocut_1D_mc = gDirectory.FindObject("posisocut_1D_mc")

eleiso_1D_mc = gDirectory.FindObject("eleiso_1D_mc")
posiso_1D_mc = gDirectory.FindObject("posiso_1D_mc")

uncVZ_mc_truth = gDirectory.FindObject("uncVZ_mc_truth")
uncVZ_mc = gDirectory.FindObject("uncVZ_mc")

eleiso_ap1 = gDirectory.FindObject("eleiso_ap1")
posiso_ap1 = gDirectory.FindObject("posiso_ap1")
uncVZ_ap1 = gDirectory.FindObject("uncVZ_ap1")
uncVZ_ap1_isocut = gDirectory.FindObject("uncVZ_ap1_isocut")
#uncVZ_ap1_truth = gDirectory.FindObject("uncVZ_ap1_truth")
#uncVZ_ap1 = gDirectory.FindObject("uncVZ_ap1")

eleiso_ap2 = gDirectory.FindObject("eleiso_ap2")
posiso_ap2 = gDirectory.FindObject("posiso_ap2")
uncVZ_ap2 = gDirectory.FindObject("uncVZ_ap2")
uncVZ_ap2_isocut = gDirectory.FindObject("uncVZ_ap2_isocut")
#uncVZ_ap2_truth = gDirectory.FindObject("uncVZ_ap2_truth")
#uncVZ_ap2 = gDirectory.FindObject("uncVZ_ap2")

eleiso_data.Add(posiso_data)
eleiso_data.Draw("COLZ")
#eleiso_data.GetXaxis().SetTitle("Isolation Cut Value (mm)")
eleiso_data.GetXaxis().SetTitle("#delta + 1/2 (z0_{corr} - n_{#sigma} #Deltaz0_{corr}) (mm)")
eleiso_data.GetYaxis().SetTitle("Reconstructed z (mm)")
eleiso_data.GetXaxis().SetLabelSize(0.04)
eleiso_data.GetYaxis().SetLabelSize(0.05)
eleiso_data.GetXaxis().SetTitleOffset(0.8)
eleiso_data.GetXaxis().SetTitleSize(0.05)
eleiso_data.GetYaxis().SetTitleOffset(0.8)
eleiso_data.GetYaxis().SetTitleSize(0.06)
eleiso_data.SetTitle("10% Data Preselection Isolation Cut")
c.Print(outfile+".pdf")
outfileroot.cd()
eleiso_data.Write("eleiso_data")
c.Write()

eleisocut_1D_data.Add(posisocut_1D_data)
eleisocut_1D_mc.Add(posisocut_1D_mc)
eleisocut_1D_data.Sumw2()
eleisocut_1D_mc.Sumw2()
eleisocut_1D_data.Write("eleisocut_1D_data")
eleisocut_1D_mc.Write("eleisocut_1D_mc")
eleisocut_1D_data.Scale(1/eleisocut_1D_data.Integral())
eleisocut_1D_mc.Scale(1/eleisocut_1D_mc.Integral())
eleisocut_1D_mc.SetLineColor(2)
eleisocut_1D_data.Draw("")
#eleisocut_1D_data.GetXaxis().SetTitle("Isolation Cut Value (mm)")
eleisocut_1D_data.GetXaxis().SetTitle("#delta + 1/2 (z0_{corr} - n_{#sigma} #Deltaz0_{corr}) (mm)")
eleisocut_1D_data.SetTitle("Preselection Isolation Cut")
eleisocut_1D_data.GetXaxis().SetLabelSize(0.04)
eleisocut_1D_data.GetYaxis().SetLabelSize(0.05)
eleisocut_1D_data.GetXaxis().SetTitleOffset(0.8)
eleisocut_1D_data.GetXaxis().SetTitleSize(0.05)
eleisocut_1D_mc.Draw("same")
legend4 = TLegend(.60,.46,.92,.67)
legend4.SetBorderSize(0)
legend4.SetFillColor(0)
legend4.SetFillStyle(0)
legend4.SetTextFont(42)
legend4.SetTextSize(0.035)
legend4.AddEntry(eleisocut_1D_data,"10% Data","LP")
legend4.AddEntry(eleisocut_1D_mc,"MC","LP")
legend4.Draw("same")
c.Print(outfile+".pdf")
c.Write()

eleiso_1D_data.Add(posiso_1D_data)
eleiso_1D_mc.Add(posiso_1D_mc)
eleiso_1D_data.Sumw2()
eleiso_1D_mc.Sumw2()
eleiso_1D_data.Write("eleiso_1D_data")
eleiso_1D_mc.Write("eleiso_1D_mc")
eleiso_1D_data.Scale(1/eleiso_1D_data.Integral())
eleiso_1D_mc.Scale(1/eleiso_1D_mc.Integral())
eleiso_1D_mc.SetLineColor(2)
eleiso_1D_data.Draw("")
eleiso_1D_data.GetXaxis().SetTitle("Isolation Value (mm)")
eleiso_1D_data.GetXaxis().SetLabelSize(0.04)
eleiso_1D_data.GetYaxis().SetLabelSize(0.05)
eleiso_1D_data.GetXaxis().SetTitleOffset(0.8)
eleiso_1D_data.GetXaxis().SetTitleSize(0.05)
eleiso_1D_data.SetTitle("Preselection Isolation Value")
eleiso_1D_mc.Draw("same")
legend4.Draw("same")
c.Print(outfile+".pdf")
c.Write()

eleiso_mc_truth.Add(posiso_mc_truth)
eleiso_mc_truth.Draw("COLZ")
#eleiso_mc_truth.GetXaxis().SetTitle("Isolation Cut Value (mm)")
eleiso_mc_truth.GetXaxis().SetTitle("#delta + 1/2 (z0_{corr} - n_{#sigma} #Deltaz0_{corr}) (mm)")
eleiso_mc_truth.GetYaxis().SetTitle("Reconstructed z (mm)")
eleiso_mc_truth.GetXaxis().SetLabelSize(0.04)
eleiso_mc_truth.GetYaxis().SetLabelSize(0.05)
eleiso_mc_truth.GetXaxis().SetTitleOffset(0.8)
eleiso_mc_truth.GetXaxis().SetTitleSize(0.05)
eleiso_mc_truth.GetYaxis().SetTitleOffset(0.8)
eleiso_mc_truth.GetYaxis().SetTitleSize(0.06)
eleiso_mc_truth.SetTitle("MC Preselection Isolation Cut with L1 Bad Hits")
c.Print(outfile+".pdf")
eleiso_mc_truth.Write("eleiso_mc_truth")
c.Write()

eleiso_mc.Add(posiso_mc)
eleiso_mc.Draw("COLZ")
#eleiso_mc.GetXaxis().SetTitle("Isolation Cut Value (mm)")
eleiso_mc.GetXaxis().SetTitle("#delta + 1/2 (z0_{corr} - n_{#sigma} #Deltaz0_{corr}) (mm)")
eleiso_mc.GetYaxis().SetTitle("Reconstructed z (mm)")
eleiso_mc.GetXaxis().SetLabelSize(0.04)
eleiso_mc.GetYaxis().SetLabelSize(0.05)
eleiso_mc.GetXaxis().SetTitleOffset(0.8)
eleiso_mc.GetXaxis().SetTitleSize(0.05)
eleiso_mc.GetYaxis().SetTitleOffset(0.8)
eleiso_mc.GetYaxis().SetTitleSize(0.06)
eleiso_mc.SetTitle("MC Preselection Isolation Cut with Pure Tracks")
c.Print(outfile+".pdf")
eleiso_mc.Write("eleiso_mc")
c.Write()


n_mc_truth = uncVZ_mc_truth.Integral()
n_mc = uncVZ_mc.Integral()
uncVZ_mc.Sumw2()
uncVZ_mc_truth.Sumw2()
uncVZ_mc.Write("uncVZ_mc")
uncVZ_mc_truth.Write("uncVZ_mc_truth")
#uncVZ_mc.Scale(1./uncVZ_mc.Integral())
#uncVZ_mc_truth.Scale(1./uncVZ_mc_truth.Integral())
uncVZ_mc_truth.SetLineColor(2)
uncVZ_mc.GetXaxis().SetTitle("Reconstructed z (mm)")
uncVZ_mc.GetYaxis().SetTitle("dN/dz (mm^{-1} )")
uncVZ_mc.GetXaxis().SetLabelSize(0.04)
uncVZ_mc.GetYaxis().SetLabelSize(0.05)
uncVZ_mc.GetXaxis().SetTitleOffset(0.8)
uncVZ_mc.GetXaxis().SetTitleSize(0.05)
uncVZ_mc.GetYaxis().SetTitleOffset(0.8)
uncVZ_mc.GetYaxis().SetTitleSize(0.06)
uncVZ_mc.SetTitle("Reconstructed Z - Good and Bad Tracks")
uncVZ_mc.Draw()
uncVZ_mc_truth.Draw("same")
legend3 = TLegend(.60,.66,.92,.87)
legend3.SetBorderSize(0)
legend3.SetFillColor(0)
legend3.SetFillStyle(0)
legend3.SetTextFont(42)
legend3.SetTextSize(0.05)
legend3.AddEntry(uncVZ_mc,"Good Tracks","LP")
legend3.AddEntry(uncVZ_mc_truth,"Bad L1 Hit","LP")
legend3.Draw("same")
c.SetLogy(1)
c.Print(outfile+".pdf")
c.Write()

eleiso_ap1.Add(posiso_ap1)
eleiso_ap1.Draw("COLZ")
#eleiso_ap1.GetXaxis().SetTitle("Isolation Cut Value (mm)")
eleiso_ap1.GetXaxis().SetTitle("#delta + 1/2 (z0_{corr} - n_{#sigma} #Deltaz0_{corr}) (mm)")
eleiso_ap1.GetYaxis().SetTitle("Reconstructed z (mm)")
eleiso_ap1.GetXaxis().SetLabelSize(0.04)
eleiso_ap1.GetYaxis().SetLabelSize(0.05)
eleiso_ap1.GetXaxis().SetTitleOffset(0.8)
eleiso_ap1.GetXaxis().SetTitleSize(0.05)
eleiso_ap1.GetYaxis().SetTitleOffset(0.8)
eleiso_ap1.GetYaxis().SetTitleSize(0.06)
eleiso_ap1.SetTitle("80 MeV A' Preselection Isolation Cut")
c.SetLogy(0)
c.Print(outfile+".pdf")
eleiso_ap1.Write("eleiso_ap1")
c.Write()

uncVZ_ap1.Sumw2()
uncVZ_ap1_isocut.Sumw2()
uncVZ_ap1.Write("uncVZ_ap1")
uncVZ_ap1_isocut.Write("uncVZ_ap1_isocut")
uncVZ_ap1_isocut.SetLineColor(2)
uncVZ_ap1.Draw()
uncVZ_ap1.GetXaxis().SetTitle("Reconstructed z (mm)")
uncVZ_ap1.GetXaxis().SetLabelSize(0.04)
uncVZ_ap1.GetYaxis().SetLabelSize(0.05)
uncVZ_ap1.GetXaxis().SetTitleOffset(0.8)
uncVZ_ap1.GetXaxis().SetTitleSize(0.05)
uncVZ_ap1.SetTitle("80 MeV A'")
uncVZ_ap1_isocut.Draw("same")
legend = TLegend(.10,.46,.42,.67)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(uncVZ_ap1,"preselection","LP")
legend.AddEntry(uncVZ_ap1_isocut,"isolation cut","LP")
legend.Draw("same")
c.Print(outfile+".pdf")
c.Write()

#n_ap1_truth = uncVZ_ap1_truth.Integral()
#n_ap1 = uncVZ_ap1.Integral()

eleiso_ap2.Add(posiso_ap2)
eleiso_ap2.Draw("COLZ")
#eleiso_ap2.GetXaxis().SetTitle("Isolation Cut Value (mm)")
eleiso_ap2.GetXaxis().SetTitle("#delta + 1/2 (z0_{corr} - n_{#sigma} #Deltaz0_{corr}) (mm)")
eleiso_ap2.GetYaxis().SetTitle("Reconstructed z (mm)")
eleiso_ap2.GetXaxis().SetLabelSize(0.04)
eleiso_ap2.GetYaxis().SetLabelSize(0.05)
eleiso_ap2.GetXaxis().SetTitleOffset(0.8)
eleiso_ap2.GetXaxis().SetTitleSize(0.05)
eleiso_ap2.GetYaxis().SetTitleOffset(0.8)
eleiso_ap2.GetYaxis().SetTitleSize(0.06)
eleiso_ap2.SetTitle("100 MeV A' Preselection Isolation Cut")
c.Print(outfile+".pdf")
eleiso_ap2.Write("eleiso_ap2")
c.Write()

uncVZ_ap2.Sumw2()
uncVZ_ap2_isocut.Sumw2()
uncVZ_ap2.Write("uncVZ_ap2")
uncVZ_ap2_isocut.Write("uncVZ_ap2_isocut")
uncVZ_ap2_isocut.SetLineColor(2)
uncVZ_ap2.Draw()
uncVZ_ap2.GetXaxis().SetTitle("Reconstructed z (mm)")
uncVZ_ap2.GetXaxis().SetLabelSize(0.04)
uncVZ_ap2.GetYaxis().SetLabelSize(0.05)
uncVZ_ap2.GetXaxis().SetTitleOffset(0.8)
uncVZ_ap2.GetXaxis().SetTitleSize(0.05)
uncVZ_ap2.SetTitle("100 MeV A'")
uncVZ_ap2_isocut.Draw("same")
legend2 = TLegend(.10,.46,.42,.67)
legend2.SetBorderSize(0)
legend2.SetFillColor(0)
legend2.SetFillStyle(0)
legend2.SetTextFont(42)
legend2.SetTextSize(0.035)
legend2.AddEntry(uncVZ_ap2,"preselection","LP")
legend2.AddEntry(uncVZ_ap2_isocut,"isolation cut","LP")
legend2.Draw("same")
c.Print(outfile+".pdf")
c.Write()

#n_ap2_truth = uncVZ_ap2_truth.Integral()
#n_ap2 = uncVZ_ap2.Integral()

print ("Number of total MC events:{0}  Number of Bad L1 Hits: {1}  Number of True Tracks: {2}".format(mcevents.GetEntries(),n_mc_truth,n_mc))
#print ("Number of total A' 80 MeV events:{0}  Number of Bad L1 Hits: {1}  Number of True Tracks: {2}".format(ap1events.GetEntries(),n_ap1_truth,n_ap1))
#print ("Number of total A' 100 MeV events:{0}  Number of Bad L1 Hits: {1}  Number of True Tracks: {2}".format(ap2events.GetEntries(),n_ap2_truth,n_ap2))



c.Clear()
RatioMin = 0.2
RatioMax = 2.2

top = TPad("top","top",0,0.42,1,1)
top.SetLogy(1)

bot = TPad("bot","bot",0,0,1,0.38)

top.Draw()
top.SetBottomMargin(0)
#top.SetTopMargin(gStyle.GetPadTopMargin()*topScale)
bot.Draw()
bot.SetTopMargin(0)
bot.SetBottomMargin(0.4)
top.cd()

eleisocut_1D_data.Draw("")
#eleisocut_1D_data.GetXaxis().SetTitle("Isolation Cut Value (mm)")
eleisocut_1D_data.GetXaxis().SetTitle("#delta + 1/2 (z0_{corr} - n_{#sigma} #Deltaz0_{corr}) (mm)")
eleisocut_1D_data.GetXaxis().SetTitleOffset(0.7)
eleisocut_1D_data.GetXaxis().SetTitleSize(0.06)
eleisocut_1D_data.GetYaxis().SetLabelSize(0.08)
eleisocut_1D_data.SetTitle("Preselection Isolation Cut")
eleisocut_1D_mc.Draw("same")
legend4.Draw("same")
bot.cd()
reference = eleisocut_1D_mc.Clone("reference")
reference.GetYaxis().SetTitle("Ratio")
#reference.GetYaxis().SetTitleSize(0.06)
reference.GetYaxis().SetLabelSize(0.1)
#reference.GetXaxis().SetTitleSize(0.1)
reference.GetXaxis().SetLabelSize(0.1)
#reference.GetXaxis().SetTitle("Isolation Cut Value (mm)")
reference.GetXaxis().SetTitle("#delta + 1/2 (z0_{corr} - n_{#sigma} #Deltaz0_{corr}) (mm)")
reference.GetXaxis().SetTitleOffset(0.8)
reference.GetXaxis().SetTitleSize(0.12)
reference.GetYaxis().SetTitleOffset(0.4)
reference.GetYaxis().SetTitleSize(0.1)
reference.GetYaxis().SetRangeUser(RatioMin,RatioMax)
reference.GetYaxis().SetNdivisions(508)
reference.GetYaxis().SetDecimals(True)
reference.Draw("axis")
ratio = eleisocut_1D_data.Clone("Ratio"+eleisocut_1D_data.GetName())
ratio.Divide(reference)
ratio.SetLineColor(1)
ratio.DrawCopy("pe same")
c.Print(outfile+".pdf")
c.Write()

c.Clear()
top = TPad("top","top",0,0.42,1,1)
top.SetLogy(1)

bot = TPad("bot","bot",0,0,1,0.38)
top.Draw()
top.SetBottomMargin(0)
#top.SetTopMargin(gStyle.GetPadTopMargin()*topScale)
bot.Draw()
bot.SetTopMargin(0)
bot.SetBottomMargin(0.4)
top.cd()

eleiso_1D_data.Draw("")
eleiso_1D_data.GetXaxis().SetTitle("Isolation Value (mm)")
eleiso_1D_data.GetYaxis().SetLabelSize(0.08)
eleiso_1D_data.SetTitle("Preselection Isolation Value")
eleiso_1D_mc.Draw("same")
legend4.Draw("same")
bot.cd()
reference2 = eleiso_1D_mc.Clone("reference2")
reference2.GetYaxis().SetTitle("Ratio")
#reference2.GetYaxis().SetTitleSize(0.06)
reference2.GetYaxis().SetLabelSize(0.1)
#reference2.GetXaxis().SetTitleSize(0.1)
reference2.GetXaxis().SetLabelSize(0.1)
reference2.GetXaxis().SetTitle("Isolation Value (mm)")
reference2.GetYaxis().SetRangeUser(RatioMin,RatioMax)
reference2.GetYaxis().SetNdivisions(508)
reference2.GetYaxis().SetDecimals(True)
reference2.GetXaxis().SetTitleOffset(0.8)
reference2.GetXaxis().SetTitleSize(0.12)
reference2.GetYaxis().SetTitleOffset(0.4)
reference2.GetYaxis().SetTitleSize(0.1)
reference2.Draw("axis")
ratio2 = eleiso_1D_data.Clone("Ratio2"+eleiso_1D_data.GetName())
ratio2.Divide(reference2)
ratio2.SetLineColor(1)
ratio2.DrawCopy("pe same")
c.Print(outfile+".pdf")
c.Write()

closePDF(outfile,c)
outfileroot.Close()
