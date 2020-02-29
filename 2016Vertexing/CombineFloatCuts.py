import sys
tmpargv = sys.argv
sys.argv = []
import getopt
#import utilities as utils
import ROOT
from ROOT import gROOT, TFile, gDirectory, gStyle, TCanvas, TH1, TLegend
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-y: plot label'
    print '\t-h: this help message'
    print

Label = ""

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'y:h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-y':
			Label=str(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def saveCutFlow(histo,histo2,histo3,histo4,histo5,histo6,histo7,histo8,label,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=1):
	outfileroot.cd()
	canvas.Clear()

	canvas.SetLogy(1)
	canvas.SetLogz(1)
	histo.SetLineColor(1)
	histo.Draw()
	histo.SetTitle(plotTitle + " " + label)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo2.SetLineColor(2)
	histo2.Draw("same")
	histo3.SetLineColor(4)
	histo3.Draw("same")
	histo4.SetLineColor(6)
	histo4.Draw("same")
	legend = TLegend(.08,.66,.42,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histo,"Without " + label,"LP")
	legend.AddEntry(histo2,"With Cut1","LP")
	legend.AddEntry(histo3,"With Cut2","LP")
	legend.AddEntry(histo4,"With Cut3","LP")
	legend.Draw("same")
	canvas.Print(outfile+".pdf")
	canvas.Write()

	canvas.SetLogy(0)
	histo5.Draw("COLZ")
	histo5.SetTitle("Vz vs Mass " + label + " Exclusive")
	histo5.GetXaxis().SetTitle("Mass [GeV]")
	histo5.GetYaxis().SetTitle("Reconstructed z [mm]")
	histo5.SetStats(stats)
	canvas.Print(outfile+".pdf")
	canvas.Write()

	histo6.Draw("COLZ")
	histo6.SetTitle("Vz vs Mass " + label + " Cut1")
	histo6.GetXaxis().SetTitle("Mass [GeV]")
	histo6.GetYaxis().SetTitle("Reconstructed z [mm]")
	histo6.SetStats(stats)
	canvas.Print(outfile+".pdf")
	canvas.Write()

	histo7.Draw("COLZ")
	histo7.SetTitle("Vz vs Mass " + label + " Cut2")
	histo7.GetXaxis().SetTitle("Mass [GeV]")
	histo7.GetYaxis().SetTitle("Reconstructed z [mm]")
	histo7.SetStats(stats)
	canvas.Print(outfile+".pdf")
	canvas.Write()

	histo8.Draw("COLZ")
	histo8.SetTitle("Vz vs Mass " + label + " Cut3")
	histo8.GetXaxis().SetTitle("Mass [GeV]")
	histo8.GetYaxis().SetTitle("Reconstructed z [mm]")
	histo8.SetStats(stats)
	canvas.Print(outfile+".pdf")
	canvas.Write()

	canvas.SetLogy(logY)

	del histo
	del histo2
	del histo3
	del histo4
	del histo5
	del histo6
	del histo7
	del histo8

gStyle.SetOptStat(110011)
c = TCanvas("c","c",800,600)

label = []
label.append("Preselection")
label.append("e+e- L1 & L2")
label.append("V0 Position")
label.append("V0 Projection")
label.append("Unconstrained Vertex Chisq")
label.append("V0 momentum")
label.append("Isolation Cut")
label.append("Impact Parameter Cuts")

plot = "uncVZ"

plotlabel = "Reconstructed z [mm]"

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")
infiles = []
for i in range(1,len(remainder)):
	infiles.append(TFile(remainder[i]))

openPDF(outfile,c)

histos = []
histos2 = []
histos3 = []
histos4 = []
histos5 = []
histos6 = []
histos7 = []
histos8 = []
for i in infiles[0].GetListOfKeys():
	infiles[0].cd()
	h = i.ReadObj()
	if((h.ClassName() != "TH1F") and (h.ClassName() != "TH1D") and (h.ClassName() != "TH2F") and (h.ClassName() != "TH2D")):
		continue
	for j in range(1,len(infiles)):
		infiles[j].cd()
		if(infiles[j].Get(h.GetName()) == None):
			print h.GetName()
			continue
		h.Add(infiles[j].Get(h.GetName()))
	if("histos" in h.GetName()):
		histos.append(h)
	elif("histo2" in h.GetName()):
		histos2.append(h)
	elif("histo3" in h.GetName()):
		histos3.append(h)
	elif("histo4" in h.GetName()):
		histos4.append(h)
	elif("histo5" in h.GetName()):
		histos5.append(h)
	elif("histo6" in h.GetName()):
		histos6.append(h)
	elif("histo7" in h.GetName()):
		histos7.append(h)
	elif("histo8" in h.GetName()):
		histos8.append(h)

for i in range(len(histos)):
	saveCutFlow(histos[i],histos2[i],histos3[i],histos4[i],histos5[i],histos6[i],histos7[i],histos8[i],label[i+2],outfile,c,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " {0}".format(Label),stats=0,logY=1)

closePDF(outfile,c)
outfileroot.Close()