import sys
tmpargv = sys.argv
sys.argv = []
import getopt
from array import array
import ROOT
from ROOT import TFile, TChain
sys.argv = tmpargv
import csv
import numpy as np

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name 0> <input file name 1> ".format(sys.argv[0])
    print "Arguments: "
    print '\t-f: use full truth info'
    print '\t-s: is signal MC'
    print '\t-x: x position of beam'
    print '\t-y: y position of beam'
    print '\t-z: target position in z'
    print '\t-h: this help message'
    print

xBeam = -0.224
yBeam = -0.08
zTarg = -4.3

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'x:y:z:h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-x':
			xBeam = float(arg)
		if opt=='-y':
			yBeam = float(arg)
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

np.random.seed(1)

nData = 65536
nSig = 65536

outfile = remainder[0]
file0 = TFile(remainder[1])
file1 = TFile(remainder[2])
events0 = file0.Get("ntuple")
events1 = file1.Get("tree")

uncVY = array('d',[0])
uncVZ = array('d',[0])
uncM = array('d',[0])
uncTargProjY = array('d',[0])
uncCovYY = array('d',[0])
uncCovZZ = array('d',[0])
eleTrkLambda = array('d',[0])
eleTrkZ0 = array('d',[0])
posTrkLambda = array('d',[0])
posTrkZ0 = array('d',[0])

events0.Branch("uncVY",uncVY,"uncVY")
events0.Branch("uncVZ",uncVZ,"uncVZ")
events0.Branch("uncM",uncM,"uncM")
events0.Branch("uncTargProjY",uncTargProjY,"uncTargProjY")
events0.Branch("uncCovYY",uncCovYY,"uncCovYY")
events0.Branch("uncCovZZ",uncCovZZ,"uncCovZZ")
events0.Branch("eleTrkLambda",eleTrkLambda,"eleTrkLambda")
events0.Branch("eleTrkZ0",eleTrkZ0,"eleTrkZ0")
events0.Branch("posTrkLambda",posTrkLambda,"posTrkLambda")
events0.Branch("posTrkZ0",posTrkZ0,"posTrkZ0")

events1.Branch("uncVY",uncVY,"uncVY")
events1.Branch("uncVZ",uncVZ,"uncVZ")
events1.Branch("uncM",uncM,"uncM")
events1.Branch("uncTargProjY",uncTargProjY,"uncTargProjY")
events1.Branch("uncCovYY",uncCovYY,"uncCovYY")
events1.Branch("uncCovZZ",uncCovZZ,"uncCovZZ")
events1.Branch("eleTrkLambda",eleTrkLambda,"eleTrkLambda")
events1.Branch("eleTrkZ0",eleTrkZ0,"eleTrkZ0")
events1.Branch("posTrkLambda",posTrkLambda,"posTrkLambda")
events1.Branch("posTrkZ0",posTrkZ0,"posTrkZ0")

vz_bck = []
vzPull_bck = []
vy_bck = []
vyPull_bck = []
uncM_bck = []
eleZ0_bck = []
posZ0_bck = []
projY_bck = []
eleTrkTanLambda_bck = []
posTrkTanLambda_bck = []

vz_sig = []
vzPull_sig = []
vy_sig = []
vyPull_sig = []
uncM_sig = []
eleZ0_sig = []
posZ0_sig = []
projY_sig = []
eleTrkTanLambda_sig = []
posTrkTanLambda_sig = []

i = 0
for entry in xrange(events0.GetEntries()):
    events0.GetEntry(entry)
    vz_bck.append(events0.uncVZ - zTarg)
    vzPull_bck.append((events0.uncVZ - zTarg) / np.sqrt(events0.uncCovZZ))
    vy_bck.append(events0.uncVY - yBeam)
    vyPull_bck.append((events0.uncVY - yBeam) / np.sqrt(events0.uncCovYY))
    uncM_bck.append(events0.uncM)
    eleZ0_bck.append(events0.eleTrkZ0 - zTarg * events0.eleTrkLambda)
    posZ0_bck.append(events0.posTrkZ0 - zTarg * events0.posTrkLambda)
    projY_bck.append(events0.uncTargProjY - yBeam)
    eleTrkTanLambda_bck.append(events0.eleTrkLambda)
    posTrkTanLambda_bck.append(events0.eleTrkLambda)
    i = i + 1
    if(i > nData+1): break

for entry in xrange(events1.GetEntries()):
    events1.GetEntry(entry)
    vz_sig.append(events1.uncVZ - zTarg)
    vzPull_sig.append((events1.uncVZ - zTarg) / np.sqrt(events1.uncCovZZ))
    vy_sig.append(events1.uncVY - yBeam)
    vyPull_sig.append((events1.uncVY - yBeam) / np.sqrt(events1.uncCovYY))
    uncM_sig.append(events1.uncM)
    eleZ0_sig.append(events1.eleTrkZ0 - zTarg * events1.eleTrkLambda)
    posZ0_sig.append(events1.posTrkZ0 - zTarg * events1.posTrkLambda)
    projY_sig.append(events1.uncTargProjY - yBeam)
    eleTrkTanLambda_sig.append(events1.eleTrkLambda)
    posTrkTanLambda_sig.append(events1.eleTrkLambda)

def sync_shuffle(i0, i1, i2, i3, i4, i5, i6, i7, i8, i9):
    n_elem = len(i0)
    indeces = np.random.permutation(n_elem)
    i0=np.asarray(i0)
    i1=np.asarray(i1)
    i2=np.asarray(i2)
    i3=np.asarray(i3)
    i4=np.asarray(i4)
    i5=np.asarray(i5)
    i6=np.asarray(i6)
    i7=np.asarray(i7)
    i8=np.asarray(i8)
    i9=np.asarray(i9)
    return i0[indeces], i1[indeces], i2[indeces], i3[indeces], i4[indeces], i5[indeces], i6[indeces], i7[indeces], i8[indeces], i9[indeces]

vz_bck,vzPull_bck,vy_bck,vyPull_bck,uncM_bck,eleZ0_bck,posZ0_bck,projY_bck,eleTrkTanLambda_bck,posTrkTanLambda_bck = sync_shuffle(vz_bck,vzPull_bck,vy_bck,vyPull_bck,uncM_bck,eleZ0_bck,posZ0_bck,projY_bck,eleTrkTanLambda_bck,posTrkTanLambda_bck)
vz_sig,vzPull_sig,vy_sig,vyPull_sig,uncM_sig,eleZ0_sig,posZ0_sig,projY_sig,eleTrkTanLambda_sig,posTrkTanLambda_sig = sync_shuffle(vz_sig,vzPull_sig,vy_sig,vyPull_sig,uncM_sig,eleZ0_sig,posZ0_sig,projY_sig,eleTrkTanLambda_sig,posTrkTanLambda_sig)

with open(outfile+'_data.csv', mode='w') as output_file:
    file_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(nData):
        file_writer.writerow([str(vz_bck[i]),str(vzPull_bck[i]),  str(vy_bck[i]), str(vyPull_bck[i]),
            str(uncM_bck[i]), str(eleZ0_bck[i]), str(posZ0_bck[i]), str(projY_bck[i]),
            str(eleTrkTanLambda_bck[i]), str(posTrkTanLambda_bck[i]), '0'])
    for i in range(nSig):
        file_writer.writerow([str(vz_sig[i]),str(vzPull_sig[i]),  str(vy_sig[i]), str(vyPull_sig[i]),
            str(uncM_sig[i]), str(eleZ0_sig[i]), str(posZ0_sig[i]), str(projY_sig[i]),
            str(eleTrkTanLambda_sig[i]), str(posTrkTanLambda_sig[i]), '1'])