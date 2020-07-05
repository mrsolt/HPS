import sys
tmpargv = sys.argv
sys.argv = []
import getopt
from array import array
import ROOT
from ROOT import TFile, TChain, TF1
sys.argv = tmpargv
import csv
import numpy as np
import random

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input root file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-s: is signal MC'
    print '\t-M: mass in GeV (default 0.080)'
    print '\t-z: target position (default -4.3 mm)'
    print '\t-g: minimum uncVZ (default -60 mm)'
    print '\t-i: maximum uncVZ (default 80 mm)'
    print '\t-e: beam energy (default 2.3 GeV)'
    print '\t-q: number of bins (default 140)'
    print '\t-t: cluster time offset (default 56 ns)'
    print '\t-j: uncVX mean (default 0)'
    print '\t-k: uncVX sigma (default 9999)'
    print '\t-m: uncVY mean (default 0)'
    print '\t-n: uncVY sigma (default 9999)'
    print '\t-o: uncTargProjX mean (default 0)'
    print '\t-p: uncTargProjX sigma (default 9999)'
    print '\t-a: uncTargProjY mean (default 0)'
    print '\t-b: uncTargProjY sigma (default 9999)'
    print '\t-d: use data file (default False)'
    print '\t-h: this help message'
    print

isSignal = False
zTarg = -4.3
ebeam = 2.3
minVZ = -60
maxVZ = 80
minP = 1.85
nBins = 140
useData = False
clusterT = 56
uncVXmean = -0.0916034735685
uncVXSig = 0.216732544476 
uncVYmean = -0.0772321507928
uncVYSig = 0.0878428842895
uncTargProjX = -0.0995461972579
uncTargProjXSig = 0.217919555935
uncTargProjY = -0.0668941015569
uncTargProjYSig = 0.0831670646584
mass = 0.080

angleMC = 0.111025680707
angleData = 0.0386557750132
angle = angleMC

if(useData):
    angle = angleData
    uncVX = -0.132067895667
    uncVXSig = 0.33663731855
    uncVY = -0.0743550601346
    uncVYSig = 0.102015199636
    uncTargProjX = -0.139824865412
    uncTargProjXSig = 0.337082294325
    uncTargProjY = -0.0600724148472
    uncTargProjYSig = 0.0971755263948

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hsz:g:i:e:q:t:j:k:m:M:n:o:p:a:b:d')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-s':
            isSignal = True
        if opt=='-M':
            mass = float(arg)
        if opt=='-z':
            zTarg = float(arg)
        if opt=='-g':
            minVZ = float(arg)
        if opt=='-i':
            maxVZ = float(arg)
        if opt=='-e':
            ebeam = float(arg)
        if opt=='-q':
            nBins = float(arg)
        if opt=='-t':
            clusterT = float(arg)
        if opt=='-j':
            uncVXmean=float(arg)
        if opt=='-k':
            uncVXSig=float(arg)
        if opt=='-m':
            uncVYmean=float(arg)
        if opt=='-n':
            uncVYSig=float(arg)
        if opt=='-o':
            uncTargProjX=float(arg)
        if opt=='-p':
            uncTargProjXSig=float(arg)
        if opt=='-a':
            uncTargProjY=float(arg)
        if opt=='-b':
            uncTargProjYSig=float(arg)
        if opt=='-d':
            useData = True
        if opt=='-h':
            print_usage()
            sys.exit(0)

outfile = remainder[0]
events0 = TChain("ntuple")
for i in range(1,len(remainder)):
    events0.Add(remainder[i])

zcut_shift = 10
fz_mc = TF1("fz_mc","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(23.55-zcut_shift,152.9,-9489,1.091e5,-5.19e5,9.013e5),0.05,0.150) #L1L1 MC
zcut_loose = fz_mc.Eval(mass)

minZ = 5
masscut_nsigma = 1.90
mres = TF1("mres","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4".format(0.9348/1000,0.05442,-0.5784,5.852,-17.24),0.04,0.2)
minM = mass - masscut_nsigma/2 * mres.Eval(mass)
maxM = mass + masscut_nsigma/2 * mres.Eval(mass)

mass_index = int((mass*1000-57.5)/5)

massshift = []
massshift.append(0.08)
massshift.append(0.12)
massshift.append(0.15)
massshift.append(0.16)
massshift.append(0.20)
massshift.append(0.23)
massshift.append(0.27)
massshift.append(0.32)
massshift.append(0.35)
massshift.append(0.35)
massshift.append(0.45)
massshift.append(0.46)
massshift.append(0.48)
massshift.append(0.47)
massshift.append(0.46)
massshift.append(0.44)
massshift.append(0.55)
massshift.append(0.44)
massshift.append(0.32)

mass_shift = massshift[mass_index]/1000

cut = "eleHasL1&&posHasL1&&eleHasL1&&posHasL1"
cut = "{0}&&uncVZ>{1}".format(cut,zcut_loose)
cut = "{0}&&uncM>{1}&&uncM<{2}".format(cut,minM,maxM)
cut = "{0}&&uncP>{1}".format(cut,minP)
file = TFile("/nfs/slac/g/hps_data2/tuple/2pt3/ML/Dum/dum_{0:0.0f}MeV_{1}.root".format(mass*1000,outfile),"recreate")
events = events0.CopyTree(cut)

uncVX = array('d',[0])
uncVY = array('d',[0])
uncVZ = array('d',[0])
uncP = array('d',[0])
uncPX = array('d',[0])
uncPY = array('d',[0])
uncPZ = array('d',[0])
uncM = array('d',[0])
eleP = array('d',[0])
eleHasL1 = array('I',[0])
eleHasL2 = array('I',[0])
eleNTrackHits = array('d',[0])
eleTrkLambda = array('d',[0])
eleTrkZ0 = array('d',[0])
eleTrkOmega = array('d',[0])
eleTrkOmegaErr = array('d',[0])
eleTrkLambdaErr = array('d',[0])
eleTrkZ0Err = array('d',[0])
posP = array('d',[0])
posHasL1 = array('I',[0])
posHasL2 = array('I',[0])
posNTrackHits = array('d',[0])
posTrkLambda = array('d',[0])
posTrkZ0 = array('d',[0])
posTrkOmega = array('d',[0])
posTrkOmegaErr = array('d',[0])
posTrkLambdaErr = array('d',[0])
posTrkZ0Err = array('d',[0])
eleMinPositiveIso = array('d',[0])
posMinPositiveIso = array('d',[0])

events.Branch("uncVX",uncVX,"uncVX")
events.Branch("uncVY",uncVY,"uncVY")
events.Branch("uncVZ",uncVZ,"uncVZ")
events.Branch("uncP",uncP,"uncP")
events.Branch("uncPX",uncPX,"uncPX")
events.Branch("uncPY",uncPY,"uncPY")
events.Branch("uncPZ",uncPZ,"uncPZ")
events.Branch("uncM",uncM,"uncM")
events.Branch("eleP",eleP,"eleP")
events.Branch("eleHasL1",eleHasL1,"eleHasL1/I")
events.Branch("eleHasL2",eleHasL2,"eleHasL2/I")
events.Branch("eleNTrackHits",eleNTrackHits,"eleNTrackHits")
events.Branch("eleTrkLambda",eleTrkLambda,"eleTrkLambda")
events.Branch("eleTrkZ0",eleTrkZ0,"eleTrkZ0")
events.Branch("eleTrkOmega",eleTrkOmega,"eleTrkOmega")
events.Branch("eleTrkOmegaErr",eleTrkOmegaErr,"eleTrkOmegaErr")
events.Branch("eleTrkLambdaErr",eleTrkLambdaErr,"eleTrkLambdaErr")
events.Branch("eleTrkZ0Err",eleTrkZ0Err,"eleTrkZ0Err")
events.Branch("posP",posP,"posP")
events.Branch("posHasL1",posHasL1,"posHasL1/I")
events.Branch("posHasL2",posHasL2,"posHasL2/I")
events.Branch("posNTrackHits",posNTrackHits,"posNTrackHits")
events.Branch("posTrkLambda",posTrkLambda,"posTrkLambda")
events.Branch("posTrkZ0",posTrkZ0,"posTrkZ0")
events.Branch("posTrkOmega",posTrkOmega,"posTrkOmega")
events.Branch("posTrkOmegaErr",posTrkOmegaErr,"posTrkOmegaErr")
events.Branch("posTrkLambdaErr",posTrkLambdaErr,"posTrkLambdaErr")
events.Branch("posTrkZ0Err",posTrkZ0Err,"posTrkZ0Err")
events.Branch("eleMinPositiveIso",eleMinPositiveIso,"eleMinPositiveIso")
events.Branch("posMinPositiveIso",posMinPositiveIso,"posMinPositiveIso")

smear_Top5hits = 0.0589307 
smear_Top6hits = 0.0433669 
smear_Bot5hits = 0.0551252 
smear_Bot6hits = 0.045657 

with open(outfile+'.csv', mode='w') as output_file:
    file_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(["truthZ","vx","vy","vz","vxPull","vyPull",
        "vzPull","vzErr","uncM","projX","projY","projXPull",
        "projYPull","eleP","eleTrkTanLambda","eleZ0","posP","posTrkTanLambda",
        "posZ0","signal"])
    for entry in xrange(events.GetEntries()):
        events.GetEntry(entry)

        #if((not events.eleHasL1) or (not events.eleHasL2) or (not events.posHasL1) or (not events.posHasL2)): continue

        #if(events.uncVZ < zcut_loose): continue

        #if(events.uncM < minM or events.uncM > maxM): continue

        #if(events.uncP < minP): continue

        eleiso = events.eleMinPositiveIso+0.5*((events.eleTrkZ0+zTarg*events.elePY/events.eleP)*np.sign(events.elePY)-3*(events.eleTrkZ0Err+abs(zTarg*events.eleTrkLambdaErr)+abs(2*zTarg*events.eleTrkLambda*events.eleTrkOmegaErr/events.eleTrkOmega)))
        posiso = events.posMinPositiveIso+0.5*((events.posTrkZ0+zTarg*events.posPY/events.posP)*np.sign(events.posPY)-3*(events.posTrkZ0Err+abs(zTarg*events.posTrkLambdaErr)+abs(2*zTarg*events.posTrkLambda*events.posTrkOmegaErr/events.posTrkOmega)))
        if(eleiso < 0 or posiso < 0): continue

        xProj = (events.uncVX-(events.uncVZ-zTarg)*events.uncPX/events.uncPZ)
        yProj = (events.uncVY-(events.uncVZ-zTarg)*events.uncPY/events.uncPZ)
        uncTargProjXrot = xProj*np.cos(-angle)-yProj*np.sin(-angle)
        uncTargProjYrot = xProj*np.sin(-angle)+yProj*np.cos(-angle)

        truthZ = 0
        signal = "0"
        if(isSignal):
        	signal = "1"
        	truthZ = events.triEndZ
        #shift targz
        zTargShift = zTarg
        if(useData):
            c0 = -0.377
            c1 = 13.79
            c2 = -55.84
            c3 = 84.0
            zTargShift = zTarg + c0 + c1*events.uncM + c2*events.uncM*events.uncM + c3*events.uncM*events.uncM*events.uncM
        vx = events.uncVX - uncVXmean 
        vy = events.uncVY - uncVYmean
        vz = events.uncVZ - zTargShift
        vxPull = (events.uncVX - uncVXmean) / uncVXSig
        vyPull = (events.uncVY - uncVYmean) / uncVYSig
        vzPull = (events.uncVZ - zTargShift) / np.sqrt(events.uncCovZZ)
        vzErr = np.sqrt(events.uncCovZZ)

        projX = uncTargProjXrot - uncTargProjX
        projY = uncTargProjYrot - uncTargProjY
        projXPull = (uncTargProjXrot - uncTargProjX) / uncTargProjXSig
        projYPull = (uncTargProjYrot - uncTargProjY) / uncTargProjYSig
        
        if(not useData):
            #Smear momentum
            if(events.eleTrkLambda > 0):
                if(events.eleNTrackHits == 5):
                    ele_smear = smear_Top5hits
                else:
                    ele_smear = smear_Top6hits
                if(events.posNTrackHits == 5):
                    pos_smear = smear_Bot5hits
                else:
                    pos_smear = smear_Bot6hits
            else:
                if(events.eleNTrackHits == 5):
                    ele_smear = smear_Bot5hits
                else:
                    ele_smear = smear_Bot6hits
                if(events.posNTrackHits == 5):
                    pos_smear = smear_Top5hits
                else:
                    pos_smear = smear_Top6hits

            P_positron_Smear = random.gauss(events.posP, events.posP*pos_smear)
            P_electron_Smear = random.gauss(events.eleP, events.eleP*ele_smear)

            eleP = P_positron_Smear
            posP = P_electron_Smear
            #Shift Mass Mean
            uncM = np.sqrt((P_positron_Smear/events.posP)*(P_electron_Smear/events.eleP))*events.uncM + mass_shift
            eleZ0 = events.eleTrkZ0 - zTargShift * events.eleTrkLambda
            posZ0 = events.posTrkZ0 - zTargShift * events.posTrkLambda
        else:
            eleP = events.eleP
            posP = events.posP
            uncM = events.uncM
            #shift Z0
            dy = events.uncTargProjY - (-0.0668941015569)
            eleZ0 = events.eleTrkZ0 - zTargShift * events.eleTrkLambda - dy
            posZ0 = events.posTrkZ0 - zTargShift * events.posTrkLambda - dy

        file_writer.writerow([str(truthZ), str(vx),str(vy),str(vz), str(vxPull), str(vyPull), str(vzPull), 
            str(vzErr), str(uncM), str(projX), str(projY), str(projXPull), str(projYPull),
            str(eleP), str(events.eleTrkLambda), str(eleZ0), 
            str(posP), str(events.posTrkLambda), str(posZ0), signal])