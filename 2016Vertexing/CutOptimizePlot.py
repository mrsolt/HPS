import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, gDirectory, gStyle, TCanvas, TH1, TLegend
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print '\t-c: is 80 MeV Ap (default False)'
    print '\t-f: is 100 MeV ap (default False)'
    print

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'cfh')

is80 = False
is100 = False

# Parse the command line arguments
for opt, arg in options:
		if opt=='-c':
			is80 = True
		if opt=='-f':
			is100 = True
		if opt=='-h':
			print_usage()
			sys.exit(0)

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

#gStyle.SetOptStat(0)
gStyle.SetOptStat(110011)
c = TCanvas("c","c",800,600)

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")
infile1 = TFile(remainder[1])
infile2 = TFile(remainder[2])
infile3 = TFile(remainder[3])
infile4 = TFile(remainder[4])
infile5 = TFile(remainder[5])

infile1.cd()
histo1 = infile1.Get("Integral")
infile2.cd()
histo2 = infile2.Get("Integral")
infile3.cd()
histo3 = infile3.Get("Integral")
infile4.cd()
histo4 = infile4.Get("Integral")
infile5.cd()
histo5 = infile5.Get("Integral")

openPDF(outfile,c)

outfileroot.cd()

maximum = histo1.GetMaximum()
if(histo2.GetMaximum() > maximum):
	maximum = histo2.GetMaximum()
if(histo3.GetMaximum() > maximum):
	maximum = histo3.GetMaximum()
histo1.SetLineColor(1)
histo1.GetXaxis().SetTitle("Cut Number")
histo1.GetYaxis().SetRangeUser(0,maximum*1.3)
histo1.SetTitle("Events Past Zcut{0}"format(label))
histo1.Draw()
histo2.SetLineColor(2)
histo2.Draw("same")
histo3.SetLineColor(4)
histo3.Draw("same")

legend = TLegend(.65,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(histo1,"10% Data","LP")
legend.AddEntry(histo2,"tritrig-wab-beam","LP")
legend.AddEntry(histo3,"tritrig","LP")
legend.Draw("")

c.Print(outfile+".pdf")
c.Write()

label = ""
if(is80):
	label = " 70 < mass < 90 MeV"
if(is100):
	label = " 90 < mass < 110 MeV"

maximum2 = histo4.GetMaximum()
if(histo5.GetMaximum() > maximum2):
	maximum2 = histo5.GetMaximum()

histo4.SetLineColor(1)
histo4.GetXaxis().SetTitle("Cut Number")
histo4.GetYaxis().SetRangeUser(0,maximum2*1.3)
histo4.SetTitle("Integrated Signal Past Zcut")
histo4.Draw()
histo5.SetLineColor(2)
histo5.Draw("same")

legend2 = TLegend(.65,.66,.92,.87)
legend2.SetBorderSize(0)
legend2.SetFillColor(0)
legend2.SetFillStyle(0)
legend2.SetTextFont(42)
legend2.SetTextSize(0.035)
legend2.AddEntry(histo4,"80 MeV A'","LP")
legend2.AddEntry(histo5,"100 MeV A'","LP")
legend2.Draw("")

c.Print(outfile+".pdf")
c.Write()

histo1.Write("Integral data")
histo2.Write("Integral tritrig-wab-beam")
histo3.Write("Integral tritrig")
histo4.Write("Integral ap 80")
histo5.Write("Integral ap 100")

outfileroot.Close()
closePDF(outfile,c)