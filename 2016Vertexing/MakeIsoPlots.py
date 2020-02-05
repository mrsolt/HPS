import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input Data file> <input MC text file> <input 80 MeV A' file> <input 100 MeV A' file>".format(sys.argv[0])
    print '\t-z: target position (default -4.3 mm)'
    print '\t-h: this help message'
    print

zTarg = -4.3

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'z:h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def comparePlot(events0,events1,events2,inHisto,nBins,minX,maxX,outfile,canvas,title0,title1,title2,XaxisTitle="",YaxisTitle="",plotTitle="",cut="",stats=0,logY=0):
	events0.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo0",nBins,minX,maxX),cut)
	events1.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo1",nBins,minX,maxX),cut)
	events2.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo2",nBins,minX,maxX),cut)
	histo0 = ROOT.gROOT.FindObject("histo0")
	histo1 = ROOT.gROOT.FindObject("histo1")
	histo2 = ROOT.gROOT.FindObject("histo2")
	if(histo0.GetEntries() != 0):
		histo0.Scale(1./histo0.GetEntries())
	if(histo1.GetEntries() != 0):
		histo1.Scale(1./histo1.GetEntries())
	if(histo2.GetEntries() != 0):
		histo2.Scale(1./histo2.GetEntries())
	maximum = histo0.GetMaximum()
	if(histo1.GetMaximum() > maximum):
		maximum = histo1.GetMaximum()
	if(histo2.GetMaximum() > maximum):
		maximum = histo2.GetMaximum()
	histo0.GetYaxis().SetRangeUser(0,1.2*maximum)
	histo0.Draw()
	histo0.SetTitle(plotTitle)
	histo0.GetXaxis().SetTitle(XaxisTitle)
	histo0.GetYaxis().SetTitle(YaxisTitle)
	histo0.SetStats(stats)
	histo1.SetLineColor(2)
	histo1.Draw("same")
	histo2.SetLineColor(6)
	histo2.Draw("same")
	legend = TLegend(.58,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histo0,title0,"LP")
	legend.AddEntry(histo1,title1,"LP")
	legend.AddEntry(histo2,title2,"LP")
	legend.Draw("same")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	del histo0
	del histo1
	del histo2

def saveCutFlow(events,inHisto,cuts,nBins,minX,maxX,labels,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	histos = []
	for i in range(len(cuts)):
		events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,"histo{0}".format(i),nBins,minX,maxX),cuts[i])
		histos.append(ROOT.gROOT.FindObject("histo{0}".format(i)))
	histos[0].SetTitle(plotTitle)
	histos[0].GetXaxis().SetTitle(XaxisTitle)
	histos[0].GetYaxis().SetTitle(YaxisTitle)
	histos[0].SetStats(stats)
	color = 1
	for i in range(len(histos)):
		if(color == 5 or color == 10):
			color = color + 1
		histos[i].SetLineColor(color)
		color = color + 1
		histos[i].Scale(1.0)
		if(i == 0):
			histos[i].Draw("")
		else:
			histos[i].Draw("same")
	legend = TLegend(.08,.46,.42,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	for i in range(len(labels)):
		legend.AddEntry(histos[i],labels[i],"LP")
	legend.Draw("")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	del histos

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

eleiso = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))".format(zTarg)
posiso = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))".format(zTarg)

#eleiso = "eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY)".format(zTarg)
#posiso = "posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY)".format(zTarg)

truthCutele = "(eleL1tIsGoodTruthHit>-0.5&&eleL1tIsGoodTruthHit<0.5)||(eleL2tIsGoodTruthHit>-0.5&&eleL2tIsGoodTruthHit<0.5)||(eleL1bIsGoodTruthHit>-0.5&&eleL1bIsGoodTruthHit<0.5)||(eleL2bIsGoodTruthHit>-0.5&&eleL2bIsGoodTruthHit<0.5)"
truthCutpos = "(posL1tIsGoodTruthHit>-0.5&&posL1tIsGoodTruthHit<0.5)||(posL2tIsGoodTruthHit>-0.5&&posL2tIsGoodTruthHit<0.5)||(posL1bIsGoodTruthHit>-0.5&&posL1bIsGoodTruthHit<0.5)||(posL2bIsGoodTruthHit>-0.5&&posL2bIsGoodTruthHit<0.5)"
purityCut = "elePurity>0.99&&posPurity>0.99"

dataevents.Draw("uncVZ:{0}>>eleiso_data(100,-3,7,100,-40,60)".format(eleiso))
dataevents.Draw("uncVZ:{0}>>posiso_data(100,-3,7,100,-40,60)".format(posiso))

dataevents.Draw("{0}>>eleisocut_1D_data(100,-3,7)".format(eleiso))
dataevents.Draw("{0}>>posisocut_1D_data(100,-3,7)".format(posiso))

dataevents.Draw("eleMinPositiveIso>>eleiso_1D_data(100,0,10)")
dataevents.Draw("posMinPositiveIso>>posiso_1D_data(100,0,10)")

mcevents.Draw("uncVZ:{0}>>eleiso_mc_truth(100,-3,7,100,-40,60)".format(eleiso),truthCutele)
mcevents.Draw("uncVZ:{0}>>posiso_mc_truth(100,-3,7,100,-40,60)".format(posiso),truthCutpos)

mcevents.Draw("{0}>>eleisocut_1D_mc(100,-3,7)".format(eleiso))
mcevents.Draw("{0}>>posisocut_1D_mc(100,-3,7)".format(posiso))

mcevents.Draw("eleMinPositiveIso>>eleiso_1D_mc(100,0,10)")
mcevents.Draw("posMinPositiveIso>>posiso_1D_mc(100,0,10)")

mcevents.Draw("uncVZ:{0}>>eleiso_mc(100,-3,7,100,-40,60)".format(eleiso),purityCut)
mcevents.Draw("uncVZ:{0}>>posiso_mc(100,-3,7,100,-40,60)".format(posiso),purityCut)

mcevents.Draw("uncVZ>>uncVZ_mc_truth(100,-40,60)",truthCutele+"||"+truthCutpos)
mcevents.Draw("uncVZ>>uncVZ_mc(100,-40,60)",purityCut)

ap1events.Draw("uncVZ:{0}>>eleiso_ap1(100,-3,7,100,-40,60)".format(eleiso))
ap1events.Draw("uncVZ:{0}>>posiso_ap1(100,-3,7,100,-40,60)".format(posiso))
ap1events.Draw("uncVZ>>uncVZ_ap1(100,-40,60)")
ap1events.Draw("uncVZ>>uncVZ_ap1_isocut(100,-40,60)",eleiso+">0&&"+posiso+">0")
ap1events.Draw("uncVZ>>uncVZ_ap1_truth(100,-40,60)",truthCutele+"||"+truthCutpos)
ap1events.Draw("uncVZ>>uncVZ_ap1(100,-40,60)",purityCut)

ap2events.Draw("uncVZ:{0}>>eleiso_ap2(100,-3,7,100,-40,60)".format(eleiso))
ap2events.Draw("uncVZ:{0}>>posiso_ap2(100,-3,7,100,-40,60)".format(posiso))
ap2events.Draw("uncVZ>>uncVZ_ap2(100,-40,60)")
ap2events.Draw("uncVZ>>uncVZ_ap2_isocut(100,-40,60)",eleiso+">0&&"+posiso+">0")
ap2events.Draw("uncVZ>>uncVZ_ap2_truth(100,-40,60)",truthCutele+"||"+truthCutpos)
ap2events.Draw("uncVZ>>uncVZ_ap2(100,-40,60)",purityCut)

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
uncVZ_ap1_truth = gDirectory.FindObject("uncVZ_ap1_truth")
uncVZ_ap1 = gDirectory.FindObject("uncVZ_ap1")

eleiso_ap2 = gDirectory.FindObject("eleiso_ap2")
posiso_ap2 = gDirectory.FindObject("posiso_ap2")
uncVZ_ap2 = gDirectory.FindObject("uncVZ_ap2")
uncVZ_ap2_isocut = gDirectory.FindObject("uncVZ_ap2_isocut")
uncVZ_ap2_truth = gDirectory.FindObject("uncVZ_ap2_truth")
uncVZ_ap2 = gDirectory.FindObject("uncVZ_ap2")

eleiso_data.Add(posiso_data)
eleiso_data.Draw("COLZ")
eleiso_data.GetXaxis().SetTitle("Isolation Cut Value (mm)")
eleiso_data.GetYaxis().SetTitle("Reconstructed z (mm)")
eleiso_data.SetTitle("10% Data Preselection Isolation Cut")
c.Print(outfile+".pdf")
outfileroot.cd()
eleiso_data.Write()

eleisocut_1D_data.Add(posisocut_1D_data)
eleisocut_1D_mc.Add(posisocut_1D_mc)
eleisocut_1D_data.Sumw2()
eleisocut_1D_mc.Sumw2()
eleisocut_1D_data.Scale(1/eleisocut_1D_data.Integral())
eleisocut_1D_mc.Scale(1/eleisocut_1D_mc.Integral())
eleisocut_1D_mc.SetLineColor(2)
eleisocut_1D_data.Draw("")
eleisocut_1D_data.GetXaxis().SetTitle("Isolation Cut Value (mm)")
eleisocut_1D_data.SetTitle("Preselection Isolation Cut")
eleisocut_1D_mc.Draw("same")
legend4 = TLegend(.10,.46,.42,.67)
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
eleiso_1D_data.Scale(1/eleiso_1D_data.Integral())
eleiso_1D_mc.Scale(1/eleiso_1D_mc.Integral())
eleiso_1D_mc.SetLineColor(2)
eleiso_1D_data.Draw("")
eleiso_1D_data.GetXaxis().SetTitle("Isolation Value (mm)")
eleiso_1D_data.SetTitle("Preselection Isolation Value")
eleiso_1D_mc.Draw("same")
#legend4 = TLegend(.10,.46,.42,.67)
#legend4.SetBorderSize(0)
#legend4.SetFillColor(0)
#legend4.SetFillStyle(0)
#legend4.SetTextFont(42)
#legend4.SetTextSize(0.035)
#legend4.AddEntry(eleiso_1D_data,"10% Data","LP")
#legend4.AddEntry(eleiso_1D_mc,"MC","LP")
legend4.Draw("same")
c.Print(outfile+".pdf")
c.Write()

eleiso_1D_data.Add(posiso_1D_data)
eleiso_1D_mc.Add(posiso_1D_mc)
c.Print(outfile+".pdf")
c.Write()

eleiso_mc_truth.Add(posiso_mc_truth)
eleiso_mc_truth.Draw("COLZ")
eleiso_mc_truth.GetXaxis().SetTitle("Isolation Cut Value (mm)")
eleiso_mc_truth.GetYaxis().SetTitle("Reconstructed z (mm)")
eleiso_mc_truth.SetTitle("MC Preselection Isolation Cut with L1 Bad Hits")
c.Print(outfile+".pdf")
eleiso_mc_truth.Write()

eleiso_mc.Add(posiso_mc)
eleiso_mc.Draw("COLZ")
eleiso_mc.GetXaxis().SetTitle("Isolation Cut Value (mm)")
eleiso_mc.GetYaxis().SetTitle("Reconstructed z (mm)")
eleiso_mc.SetTitle("MC Preselection Isolation Cut with Pure Tracks")
c.Print(outfile+".pdf")
eleiso_mc.Write()


n_mc_truth = uncVZ_mc_truth.Integral()
n_mc = uncVZ_mc.Integral()
uncVZ_mc.Sumw2()
uncVZ_mc_truth.Sumw2()
uncVZ_mc.Scale(1./uncVZ_mc.Integral())
uncVZ_mc_truth.Scale(1./uncVZ_mc_truth.Integral())
uncVZ_mc.SetLineColor(2)
uncVZ_mc.Draw()
uncVZ_mc_truth.Draw("same")
uncVZ_mc_truth.GetXaxis().SetTitle("Reconstructed z (mm)")
uncVZ_mc_truth.SetTitle("Reconstructed Z - Good and Bad Tracks")
legend3 = TLegend(.10,.46,.42,.67)
legend3.SetBorderSize(0)
legend3.SetFillColor(0)
legend3.SetFillStyle(0)
legend3.SetTextFont(42)
legend3.SetTextSize(0.035)
legend3.AddEntry(uncVZ_mc,"Good Tracks","LP")
legend3.AddEntry(uncVZ_mc_truth,"Bad L1 Hit","LP")
legend3.Draw("same")
c.Print(outfile+".pdf")
c.Write()

eleiso_ap1.Add(posiso_ap1)
eleiso_ap1.Draw("COLZ")
eleiso_ap1.GetXaxis().SetTitle("Isolation Cut Value (mm)")
eleiso_ap1.GetYaxis().SetTitle("Reconstructed z (mm)")
eleiso_ap1.SetTitle("80 MeV A' Preselection Isolation Cut")
c.Print(outfile+".pdf")
eleiso_ap1.Write()

uncVZ_ap1.Sumw2()
uncVZ_ap1_isocut.Sumw2()
uncVZ_ap1_isocut.SetLineColor(2)
uncVZ_ap1.Draw()
uncVZ_ap1.GetXaxis().SetTitle("Reconstructed z (mm)")
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

n_ap1_truth = uncVZ_ap1_truth.Integral()
n_ap1 = uncVZ_ap1.Integral()

eleiso_ap2.Add(posiso_ap2)
eleiso_ap2.Draw("COLZ")
eleiso_ap2.GetXaxis().SetTitle("Isolation Cut Value (mm)")
eleiso_ap2.GetYaxis().SetTitle("Reconstructed z (mm)")
eleiso_ap2.SetTitle("100 MeV A' Preselection Isolation Cut")
c.Print(outfile+".pdf")
eleiso_ap2.Write()

uncVZ_ap2.Sumw2()
uncVZ_ap2_isocut.Sumw2()
uncVZ_ap2_isocut.SetLineColor(2)
uncVZ_ap2.Draw()
uncVZ_ap2.GetXaxis().SetTitle("Reconstructed z (mm)")
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

n_ap2_truth = uncVZ_ap2_truth.Integral()
n_ap2 = uncVZ_ap2.Integral()

closePDF(outfile,c)
outfileroot.Close()

print ("Number of total MC events:{0}  Number of Bad L1 Hits: {1}  Number of True Tracks: {2}".format(mcevents.GetEntries(),n_mc_truth,n_mc))
print ("Number of total A' 80 MeV events:{0}  Number of Bad L1 Hits: {1}  Number of True Tracks: {2}".format(ap1events.GetEntries(),n_ap1_truth,n_ap1))
print ("Number of total A' 80 MeV events:{0}  Number of Bad L1 Hits: {1}  Number of True Tracks: {2}".format(ap2events.GetEntries(),n_ap2_truth,n_ap2))