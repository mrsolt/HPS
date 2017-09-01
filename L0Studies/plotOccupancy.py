#!/usr/bin/env python
import sys
import array, math
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TH1F, TGraph, gPad, TF1, TGraphErrors, TLegend, TGaxis, TLine
import getopt


def print_usage():
    print "\nUsage:"
    print "Arguments: "
    print '\t-h: this help message'
    print "\n"

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hm:')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-m':
            mass = arg
        if opt=='-h':
            print_usage()
            sys.exit(0)

filename1 = "/home/mrsolt/hps/L0Studies/L0/1pt05/wab-beam-tri-5mrad/run1000000_occupancy.root"
filename2 = "/home/mrsolt/hps/L0Studies/nominal/1pt05/wab-beam-tri-5mrad/run5772_occupancy.root"

outname = "occupancy_"

inFile1 = TFile(filename1)
inFile2 = TFile(filename2)

L0b_axial_hole_L0 = inFile1.Get("module_L1b_halfmodule_axial_hole_sensor0 - Occupancy")
L0b_axial_slot_L0 = inFile1.Get("module_L1b_halfmodule_axial_slot_sensor0 - Occupancy")
L0b_stereo_hole_L0 = inFile1.Get("module_L1b_halfmodule_stereo_hole_sensor0 - Occupancy")
L0b_stereo_slot_L0 = inFile1.Get("module_L1b_halfmodule_stereo_slot_sensor0 - Occupancy")
L0t_axial_hole_L0 = inFile1.Get("module_L1t_halfmodule_axial_hole_sensor0 - Occupancy")
L0t_axial_slot_L0 = inFile1.Get("module_L1t_halfmodule_axial_slot_sensor0 - Occupancy")
L0t_stereo_hole_L0 = inFile1.Get("module_L1t_halfmodule_stereo_hole_sensor0 - Occupancy")
L0t_stereo_slot_L0 = inFile1.Get("module_L1t_halfmodule_stereo_slot_sensor0 - Occupancy")

L1b_axial_L0 = inFile1.Get("module_L2b_halfmodule_axial_sensor0 - Occupancy")
L1b_stereo_L0 = inFile1.Get("module_L2b_halfmodule_stereo_sensor0 - Occupancy")
L1t_axial_L0 = inFile1.Get("module_L2t_halfmodule_axial_sensor0 - Occupancy")
L1t_stereo_L0 = inFile1.Get("module_L2t_halfmodule_stereo_sensor0 - Occupancy")

L2b_axial_L0 = inFile1.Get("module_L3b_halfmodule_axial_sensor0 - Occupancy")
L2b_stereo_L0 = inFile1.Get("module_L3b_halfmodule_stereo_sensor0 - Occupancy")
L2t_axial_L0 = inFile1.Get("module_L3t_halfmodule_axial_sensor0 - Occupancy")
L2t_stereo_L0 = inFile1.Get("module_L3t_halfmodule_stereo_sensor0 - Occupancy")

L3b_axial_L0 = inFile1.Get("module_L4b_halfmodule_axial_sensor0 - Occupancy")
L3b_stereo_L0 = inFile1.Get("module_L4b_halfmodule_stereo_sensor0 - Occupancy")
L3t_axial_L0 = inFile1.Get("module_L4t_halfmodule_axial_sensor0 - Occupancy")
L3t_stereo_L0 = inFile1.Get("module_L4t_halfmodule_stereo_sensor0 - Occupancy")

L4b_axial_hole_L0 = inFile1.Get("module_L5b_halfmodule_axial_hole_sensor0 - Occupancy")
L4b_axial_slot_L0 = inFile1.Get("module_L5b_halfmodule_axial_slot_sensor0 - Occupancy")
L4b_stereo_hole_L0 = inFile1.Get("module_L5b_halfmodule_stereo_hole_sensor0 - Occupancy")
L4b_stereo_slot_L0 = inFile1.Get("module_L5b_halfmodule_stereo_slot_sensor0 - Occupancy")
L4t_axial_hole_L0 = inFile1.Get("module_L5t_halfmodule_axial_hole_sensor0 - Occupancy")
L4t_axial_slot_L0 = inFile1.Get("module_L5t_halfmodule_axial_slot_sensor0 - Occupancy")
L4t_stereo_hole_L0 = inFile1.Get("module_L5t_halfmodule_stereo_hole_sensor0 - Occupancy")
L4t_stereo_slot_L0 = inFile1.Get("module_L5t_halfmodule_stereo_slot_sensor0 - Occupancy")

L5b_axial_hole_L0 = inFile1.Get("module_L6b_halfmodule_axial_hole_sensor0 - Occupancy")
L5b_axial_slot_L0 = inFile1.Get("module_L6b_halfmodule_axial_slot_sensor0 - Occupancy")
L5b_stereo_hole_L0 = inFile1.Get("module_L6b_halfmodule_stereo_hole_sensor0 - Occupancy")
L5b_stereo_slot_L0 = inFile1.Get("module_L6b_halfmodule_stereo_slot_sensor0 - Occupancy")
L5t_axial_hole_L0 = inFile1.Get("module_L6t_halfmodule_axial_hole_sensor0 - Occupancy")
L5t_axial_slot_L0 = inFile1.Get("module_L6t_halfmodule_axial_slot_sensor0 - Occupancy")
L5t_stereo_hole_L0 = inFile1.Get("module_L6t_halfmodule_stereo_hole_sensor0 - Occupancy")
L5t_stereo_slot_L0 = inFile1.Get("module_L6t_halfmodule_stereo_slot_sensor0 - Occupancy")

L6b_axial_hole_L0 = inFile1.Get("module_L7b_halfmodule_axial_hole_sensor0 - Occupancy")
L6b_axial_slot_L0 = inFile1.Get("module_L7b_halfmodule_axial_slot_sensor0 - Occupancy")
L6b_stereo_hole_L0 = inFile1.Get("module_L7b_halfmodule_stereo_hole_sensor0 - Occupancy")
L6b_stereo_slot_L0 = inFile1.Get("module_L7b_halfmodule_stereo_slot_sensor0 - Occupancy")
L6t_axial_hole_L0 = inFile1.Get("module_L7t_halfmodule_axial_hole_sensor0 - Occupancy")
L6t_axial_slot_L0 = inFile1.Get("module_L7t_halfmodule_axial_slot_sensor0 - Occupancy")
L6t_stereo_hole_L0 = inFile1.Get("module_L7t_halfmodule_stereo_hole_sensor0 - Occupancy")
L6t_stereo_slot_L0 = inFile1.Get("module_L7t_halfmodule_stereo_slot_sensor0 - Occupancy")



L1b_axial_nom = inFile2.Get("module_L1b_halfmodule_axial_sensor0 - Occupancy")
L1b_stereo_nom = inFile2.Get("module_L1b_halfmodule_stereo_sensor0 - Occupancy")
L1t_axial_nom = inFile2.Get("module_L1t_halfmodule_axial_sensor0 - Occupancy")
L1t_stereo_nom = inFile2.Get("module_L1t_halfmodule_stereo_sensor0 - Occupancy")

L2b_axial_nom = inFile2.Get("module_L2b_halfmodule_axial_sensor0 - Occupancy")
L2b_stereo_nom = inFile2.Get("module_L2b_halfmodule_stereo_sensor0 - Occupancy")
L2t_axial_nom = inFile2.Get("module_L2t_halfmodule_axial_sensor0 - Occupancy")
L2t_stereo_nom = inFile2.Get("module_L2t_halfmodule_stereo_sensor0 - Occupancy")

L3b_axial_nom = inFile2.Get("module_L3b_halfmodule_axial_sensor0 - Occupancy")
L3b_stereo_nom = inFile2.Get("module_L3b_halfmodule_stereo_sensor0 - Occupancy")
L3t_axial_nom = inFile2.Get("module_L3t_halfmodule_axial_sensor0 - Occupancy")
L3t_stereo_nom = inFile2.Get("module_L3t_halfmodule_stereo_sensor0 - Occupancy")

L4b_axial_hole_nom = inFile2.Get("module_L4b_halfmodule_axial_hole_sensor0 - Occupancy")
L4b_axial_slot_nom = inFile2.Get("module_L4b_halfmodule_axial_slot_sensor0 - Occupancy")
L4b_stereo_hole_nom = inFile2.Get("module_L4b_halfmodule_stereo_hole_sensor0 - Occupancy")
L4b_stereo_slot_nom = inFile2.Get("module_L4b_halfmodule_stereo_slot_sensor0 - Occupancy")
L4t_axial_hole_nom = inFile2.Get("module_L4t_halfmodule_axial_hole_sensor0 - Occupancy")
L4t_axial_slot_nom = inFile2.Get("module_L4t_halfmodule_axial_slot_sensor0 - Occupancy")
L4t_stereo_hole_nom = inFile2.Get("module_L4t_halfmodule_stereo_hole_sensor0 - Occupancy")
L4t_stereo_slot_nom = inFile2.Get("module_L4t_halfmodule_stereo_slot_sensor0 - Occupancy")

L5b_axial_hole_nom = inFile2.Get("module_L5b_halfmodule_axial_hole_sensor0 - Occupancy")
L5b_axial_slot_nom = inFile2.Get("module_L5b_halfmodule_axial_slot_sensor0 - Occupancy")
L5b_stereo_hole_nom = inFile2.Get("module_L5b_halfmodule_stereo_hole_sensor0 - Occupancy")
L5b_stereo_slot_nom = inFile2.Get("module_L5b_halfmodule_stereo_slot_sensor0 - Occupancy")
L5t_axial_hole_nom = inFile2.Get("module_L5t_halfmodule_axial_hole_sensor0 - Occupancy")
L5t_axial_slot_nom = inFile2.Get("module_L5t_halfmodule_axial_slot_sensor0 - Occupancy")
L5t_stereo_hole_nom = inFile2.Get("module_L5t_halfmodule_stereo_hole_sensor0 - Occupancy")
L5t_stereo_slot_nom = inFile2.Get("module_L5t_halfmodule_stereo_slot_sensor0 - Occupancy")

L6b_axial_hole_nom = inFile2.Get("module_L6b_halfmodule_axial_hole_sensor0 - Occupancy")
L6b_axial_slot_nom = inFile2.Get("module_L6b_halfmodule_axial_slot_sensor0 - Occupancy")
L6b_stereo_hole_nom = inFile2.Get("module_L6b_halfmodule_stereo_hole_sensor0 - Occupancy")
L6b_stereo_slot_nom = inFile2.Get("module_L6b_halfmodule_stereo_slot_sensor0 - Occupancy")
L6t_axial_hole_nom = inFile2.Get("module_L6t_halfmodule_axial_hole_sensor0 - Occupancy")
L6t_axial_slot_nom = inFile2.Get("module_L6t_halfmodule_axial_slot_sensor0 - Occupancy")
L6t_stereo_hole_nom = inFile2.Get("module_L6t_halfmodule_stereo_hole_sensor0 - Occupancy")
L6t_stereo_slot_nom = inFile2.Get("module_L6t_halfmodule_stereo_slot_sensor0 - Occupancy")

def plot(histo,outName):
    histo.Draw("")
    histo.SetTitle(histo.GetTitle())
    c.Print(outName + ".pdf","Title:histoTitle")

c = TCanvas("c","c",800,600)

outnameL0 = outname + "L0"
outnamenom = outname + "nom"

c.Print(outnameL0 + ".pdf[","Title:histoTitle")

plot(L0b_axial_hole_L0,outnameL0)
plot(L0b_axial_slot_L0,outnameL0)
plot(L0b_stereo_hole_L0,outnameL0)
plot(L0b_stereo_slot_L0,outnameL0)
plot(L0t_axial_hole_L0,outnameL0)
plot(L0t_axial_slot_L0,outnameL0)
plot(L0t_stereo_hole_L0,outnameL0)
plot(L0t_stereo_slot_L0,outnameL0)

plot(L1b_axial_L0,outnameL0)
plot(L1b_stereo_L0,outnameL0)
plot(L1t_axial_L0,outnameL0)
plot(L1t_stereo_L0,outnameL0)

plot(L2b_axial_L0,outnameL0)
plot(L2b_stereo_L0,outnameL0)
plot(L2t_axial_L0,outnameL0)
plot(L2t_stereo_L0,outnameL0)

plot(L3b_axial_L0,outnameL0)
plot(L3b_stereo_L0,outnameL0)
plot(L3t_axial_L0,outnameL0)
plot(L3t_stereo_L0,outnameL0)

plot(L4b_axial_hole_L0,outnameL0)
plot(L4b_axial_slot_L0,outnameL0)
plot(L4b_stereo_hole_L0,outnameL0)
plot(L4b_stereo_slot_L0,outnameL0)
plot(L4t_axial_hole_L0,outnameL0)
plot(L4t_axial_slot_L0,outnameL0)
plot(L4t_stereo_hole_L0,outnameL0)
plot(L4t_stereo_slot_L0,outnameL0)

plot(L5b_axial_hole_L0,outnameL0)
plot(L5b_axial_slot_L0,outnameL0)
plot(L5b_stereo_hole_L0,outnameL0)
plot(L5b_stereo_slot_L0,outnameL0)
plot(L5t_axial_hole_L0,outnameL0)
plot(L5t_axial_slot_L0,outnameL0)
plot(L5t_stereo_hole_L0,outnameL0)
plot(L5t_stereo_slot_L0,outnameL0)

plot(L6b_axial_hole_L0,outnameL0)
plot(L6b_axial_slot_L0,outnameL0)
plot(L6b_stereo_hole_L0,outnameL0)
plot(L6b_stereo_slot_L0,outnameL0)
plot(L6t_axial_hole_L0,outnameL0)
plot(L6t_axial_slot_L0,outnameL0)
plot(L6t_stereo_hole_L0,outnameL0)
plot(L6t_stereo_slot_L0,outnameL0)

c.Print(outnameL0 + ".pdf]","Title:histoTitle")



c.Print(outnamenom + ".pdf[","Title:histoTitle")

plot(L1b_axial_nom,outnamenom)
plot(L1b_stereo_nom,outnamenom)
plot(L1t_axial_nom,outnamenom)
plot(L1t_stereo_nom,outnamenom)

plot(L2b_axial_nom,outnamenom)
plot(L2b_stereo_nom,outnamenom)
plot(L2t_axial_nom,outnamenom)
plot(L2t_stereo_nom,outnamenom)

plot(L3b_axial_nom,outnamenom)
plot(L3b_stereo_nom,outnamenom)
plot(L3t_axial_nom,outnamenom)
plot(L3t_stereo_nom,outnamenom)

plot(L4b_axial_hole_nom,outnamenom)
plot(L4b_axial_slot_nom,outnamenom)
plot(L4b_stereo_hole_nom,outnamenom)
plot(L4b_stereo_slot_nom,outnamenom)
plot(L4t_axial_hole_nom,outnamenom)
plot(L4t_axial_slot_nom,outnamenom)
plot(L4t_stereo_hole_nom,outnamenom)
plot(L4t_stereo_slot_nom,outnamenom)

plot(L5b_axial_hole_nom,outnamenom)
plot(L5b_axial_slot_nom,outnamenom)
plot(L5b_stereo_hole_nom,outnamenom)
plot(L5b_stereo_slot_nom,outnamenom)
plot(L5t_axial_hole_nom,outnamenom)
plot(L5t_axial_slot_nom,outnamenom)
plot(L5t_stereo_hole_nom,outnamenom)
plot(L5t_stereo_slot_nom,outnamenom)

plot(L6b_axial_hole_nom,outnamenom)
plot(L6b_axial_slot_nom,outnamenom)
plot(L6b_stereo_hole_nom,outnamenom)
plot(L6b_stereo_slot_nom,outnamenom)
plot(L6t_axial_hole_nom,outnamenom)
plot(L6t_axial_slot_nom,outnamenom)
plot(L6t_stereo_hole_nom,outnamenom)
plot(L6t_stereo_slot_nom,outnamenom)

c.Clear()


c.Print(outnamenom + ".pdf]","Title:histoTitle")

def getEdge(histo,reverse,L0):
    chan = 1
    if(reverse and not L0): chan = 640
    if(reverse and L0): chan = 256 
    if(L0): histo.Scale(1/1.1)
    if(not L0): histo.Scale(1/1.5)
    return histo.GetBinContent(chan)

layerArrL0 = array.array('d')
layerArrnom = array.array('d')
occupancyL0Top = array.array('d')
occupancyL0Bot = array.array('d')
occupancynomTop = array.array('d')
occupancynomBot = array.array('d')
nL0 = 22
nNom = 18

occupancyL0Bot.append(getEdge(L0b_axial_hole_L0,False,True))
occupancyL0Bot.append(getEdge(L0b_axial_slot_L0,True,True))
occupancyL0Bot.append(getEdge(L0b_stereo_hole_L0,True,True))
occupancyL0Bot.append(getEdge(L0b_stereo_slot_L0,False,True))
occupancyL0Top.append(getEdge(L0t_axial_hole_L0,False,True))
occupancyL0Top.append(getEdge(L0t_axial_slot_L0,True,True))
occupancyL0Top.append(getEdge(L0t_stereo_hole_L0,True,True))
occupancyL0Top.append(getEdge(L0t_stereo_slot_L0,False,True))

occupancyL0Bot.append(getEdge(L1b_axial_L0,False,False))
occupancyL0Bot.append(getEdge(L1b_stereo_L0,True,False))
occupancyL0Top.append(getEdge(L1t_axial_L0,False,False))
occupancyL0Top.append(getEdge(L1t_stereo_L0,True,False))

occupancyL0Bot.append(getEdge(L2b_axial_L0,False,False))
occupancyL0Bot.append(getEdge(L2b_stereo_L0,True,False))
occupancyL0Top.append(getEdge(L2t_axial_L0,False,False))
occupancyL0Top.append(getEdge(L2t_stereo_L0,True,False))

occupancyL0Bot.append(getEdge(L3b_axial_L0,False,False))
occupancyL0Bot.append(getEdge(L3b_stereo_L0,True,False))
occupancyL0Top.append(getEdge(L3t_axial_L0,False,False))
occupancyL0Top.append(getEdge(L3t_stereo_L0,True,False))

occupancyL0Bot.append(getEdge(L4b_axial_hole_L0,False,False))
occupancyL0Bot.append(getEdge(L4b_axial_slot_L0,True,False))
occupancyL0Bot.append(getEdge(L4b_stereo_hole_L0,True,False))
occupancyL0Bot.append(getEdge(L4b_stereo_slot_L0,False,False))
occupancyL0Top.append(getEdge(L4t_axial_hole_L0,False,False))
occupancyL0Top.append(getEdge(L4t_axial_slot_L0,True,False))
occupancyL0Top.append(getEdge(L4t_stereo_hole_L0,True,False))
occupancyL0Top.append(getEdge(L4t_stereo_slot_L0,False,False))

occupancyL0Bot.append(getEdge(L5b_axial_hole_L0,False,False))
occupancyL0Bot.append(getEdge(L5b_axial_slot_L0,True,False))
occupancyL0Bot.append(getEdge(L5b_stereo_hole_L0,True,False))
occupancyL0Bot.append(getEdge(L5b_stereo_slot_L0,False,False))
occupancyL0Top.append(getEdge(L5t_axial_hole_L0,False,False))
occupancyL0Top.append(getEdge(L5t_axial_slot_L0,True,False))
occupancyL0Top.append(getEdge(L5t_stereo_hole_L0,True,False))
occupancyL0Top.append(getEdge(L5t_stereo_slot_L0,False,False))

occupancyL0Bot.append(getEdge(L6b_axial_hole_L0,False,False))
occupancyL0Bot.append(getEdge(L6b_axial_slot_L0,True,False))
occupancyL0Bot.append(getEdge(L6b_stereo_hole_L0,True,False))
occupancyL0Bot.append(getEdge(L6b_stereo_slot_L0,False,False))
occupancyL0Top.append(getEdge(L6t_axial_hole_L0,False,False))
occupancyL0Top.append(getEdge(L6t_axial_slot_L0,True,False))
occupancyL0Top.append(getEdge(L6t_stereo_hole_L0,True,False))
occupancyL0Top.append(getEdge(L6t_stereo_slot_L0,False,False))



occupancynomBot.append(getEdge(L1b_axial_nom,False,False))
occupancynomBot.append(getEdge(L1b_stereo_nom,True,False))
occupancynomTop.append(getEdge(L1t_axial_nom,False,False))
occupancynomTop.append(getEdge(L1t_stereo_nom,True,False))

occupancynomBot.append(getEdge(L2b_axial_nom,False,False))
occupancynomBot.append(getEdge(L2b_stereo_nom,True,False))
occupancynomTop.append(getEdge(L2t_axial_nom,False,False))
occupancynomTop.append(getEdge(L2t_stereo_nom,True,False))

occupancynomBot.append(getEdge(L3b_axial_nom,False,False))
occupancynomBot.append(getEdge(L3b_stereo_nom,True,False))
occupancynomTop.append(getEdge(L3t_axial_nom,False,False))
occupancynomTop.append(getEdge(L3t_stereo_nom,True,False))

occupancynomBot.append(getEdge(L4b_axial_hole_nom,False,False))
occupancynomBot.append(getEdge(L4b_axial_slot_nom,True,False))
occupancynomBot.append(getEdge(L4b_stereo_hole_nom,True,False))
occupancynomBot.append(getEdge(L4b_stereo_slot_nom,False,False))
occupancynomTop.append(getEdge(L4t_axial_hole_nom,False,False))
occupancynomTop.append(getEdge(L4t_axial_slot_nom,True,False))
occupancynomTop.append(getEdge(L4t_stereo_hole_nom,True,False))
occupancynomTop.append(getEdge(L4t_stereo_slot_nom,False,False))

occupancynomBot.append(getEdge(L5b_axial_hole_nom,False,False))
occupancynomBot.append(getEdge(L5b_axial_slot_nom,True,False))
occupancynomBot.append(getEdge(L5b_stereo_hole_nom,True,False))
occupancynomBot.append(getEdge(L5b_stereo_slot_nom,False,False))
occupancynomTop.append(getEdge(L5t_axial_hole_nom,False,False))
occupancynomTop.append(getEdge(L5t_axial_slot_nom,True,False))
occupancynomTop.append(getEdge(L5t_stereo_hole_nom,True,False))
occupancynomTop.append(getEdge(L5t_stereo_slot_nom,False,False))

occupancynomBot.append(getEdge(L6b_axial_hole_nom,False,False))
occupancynomBot.append(getEdge(L6b_axial_slot_nom,True,False))
occupancynomBot.append(getEdge(L6b_stereo_hole_nom,True,False))
occupancynomBot.append(getEdge(L6b_stereo_slot_nom,False,False))
occupancynomTop.append(getEdge(L6t_axial_hole_nom,False,False))
occupancynomTop.append(getEdge(L6t_axial_slot_nom,True,False))
occupancynomTop.append(getEdge(L6t_stereo_hole_nom,True,False))
occupancynomTop.append(getEdge(L6t_stereo_slot_nom,False,False))



layerArrL0.append(0)
layerArrL0.append(0.25)
layerArrL0.append(0.5)
layerArrL0.append(0.75)
layerArrL0.append(1)
layerArrL0.append(1.5)
layerArrL0.append(2)
layerArrL0.append(2.5)
layerArrL0.append(3)
layerArrL0.append(3.5)
layerArrL0.append(4)
layerArrL0.append(4.25)
layerArrL0.append(4.5)
layerArrL0.append(4.75)
layerArrL0.append(5)
layerArrL0.append(5.25)
layerArrL0.append(5.5)
layerArrL0.append(5.75)
layerArrL0.append(6)
layerArrL0.append(6.25)
layerArrL0.append(6.5)
layerArrL0.append(6.75)

layerArrnom.append(1)
layerArrnom.append(1.5)
layerArrnom.append(2)
layerArrnom.append(2.5)
layerArrnom.append(3)
layerArrnom.append(3.5)
layerArrnom.append(4)
layerArrnom.append(4.25)
layerArrnom.append(4.5)
layerArrnom.append(4.75)
layerArrnom.append(5)
layerArrnom.append(5.25)
layerArrnom.append(5.5)
layerArrnom.append(5.75)
layerArrnom.append(6)
layerArrnom.append(6.25)
layerArrnom.append(6.5)
layerArrnom.append(6.75)

GraphL0Top = TGraph(nL0,layerArrL0,occupancyL0Top)
GraphnomTop = TGraph(nNom,layerArrnom,occupancynomTop)
GraphL0Bot = TGraph(nL0,layerArrL0,occupancyL0Bot)
GraphnomBot = TGraph(nNom,layerArrnom,occupancynomBot)

legend = TLegend(.65,.66,.89,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(GraphL0Top,"L0","LP")
legend.AddEntry(GraphnomTop,"Nominal","LP")

GraphL0Top.Draw("")
GraphL0Top.SetTitle("SVT Sensor Edge Cluster Occupancies Top")
#GraphL0Top.GetXaxis().SetRangeUser(-5,150)
GraphL0Top.GetYaxis().SetRangeUser(0,0.03)
GraphL0Top.GetXaxis().SetTitle("Layer Number")
GraphL0Top.GetYaxis().SetTitle("Occupancy")

GraphnomTop.Draw("same")
GraphnomTop.SetMarkerColor(2)
GraphnomTop.SetLineColor(2)

c.Update()
legend.Draw()
c.Print(outname + "_top_1st.pdf","Title:histoTitle")

c.Clear()

GraphL0Bot.Draw("")
GraphL0Bot.SetTitle("SVT Sensor Edge Cluster Occupancies Bottom")
#GraphL0Bot.GetXaxis().SetRangeUser(-5,150)
GraphL0Bot.GetYaxis().SetRangeUser(0,0.03)
GraphL0Bot.GetXaxis().SetTitle("Layer Number")
GraphL0Bot.GetYaxis().SetTitle("Occupancy")

GraphnomBot.Draw("same")
GraphnomBot.SetMarkerColor(2)
GraphnomBot.SetLineColor(2)

c.Update()
legend.Draw()
c.Print(outname + "_bot_1st.pdf","Title:histoTitle")
