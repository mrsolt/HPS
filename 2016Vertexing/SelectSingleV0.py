#!/usr/bin/env python
import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import root_numpy, numpy
sys.argv = tmpargv

def print_usage():
    print "\nUsage: {0} <output ROOT file name> <input ROOT file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-e: use this beam energy'
    print '\t-c: only write candidates that pass cuts'
    print '\t-b: only keep best candidate'
    print '\t-o: only keep candidate if it\'s the only one'
    print '\t-m: use MC information'
    print '\t-h: this help message'
    print

ebeam=2.3

cutOutput = False
onlyBest = False
onlyOnly = False
useMC = False

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:cbomh')
# Parse the command line arguments
for opt, arg in options:
        if opt=='-e':
            ebeam=float(arg)
        if opt=='-c':
            cutOutput = True
        if opt=='-b':
            onlyBest = True
        if opt=='-o':
            onlyOnly = True
        if opt=='-m':
            useMC = True
        if opt=='-h':
            print_usage()
            sys.exit(0)

if len(remainder)!=2:
    print_usage()
    sys.exit(0)
print remainder[0]
print remainder[1]

branchlist=["event",
    "run",
    "uncP",
    "uncM",
    "uncVZ",
    "bscChisq",
    "eleP",
    "posP",
    "elePX",
    "posPX",
    "eleMatchChisq",
    "posMatchChisq",
    "eleTrkChisq",
    "posTrkChisq",
    "eleTrkT",
    "posTrkT",
    "eleClY",
    "posClY",
    "eleClT",
    "posClT",
    "minIso",
    "minPositiveIso",
    "posTrkD0",
    "bscP",
    "eleHasL1",
    "posHasL1",
    "eleHasL2",
    "posHasL2",
    "eleFirstHitX",
    "posFirstHitX",
    "nPos"]

if useMC:
    branchlist.append("triP")
    branchlist.append("triPair1P")
    branchlist.append("triM")
    branchlist.append("triEndZ")
events = root_numpy.root2array(remainder[1],branches=branchlist,treename="ntuple")

n = events.size

cut = events["uncP"]>0.0
    #cut = numpy.row_stack((#events["isPair1"]==1,
        #events["uncP"]>0.8*ebeam)).all(0)

names = ["run",
        "event",
        "eleHasL1",
        "posHasL1",
        "uncP",
        "uncM",
        "uncVZ"]
if useMC:
    names.append("triP")
    names.append("triPair1P")
    names.append("triM")
    names.append("triEndZ")

stuff = [[events[i],(i,events.dtype[i])] for i in names]
stuff.append([cut,("cut",numpy.int8)])
stuff.append([numpy.zeros(n),("nPass",numpy.int8)])
stuff.append([numpy.zeros(n),("rank",numpy.int8)])

dataarray = [i[0] for i in stuff]
typearray = [i[1] for i in stuff]
output = numpy.core.records.fromarrays(dataarray,dtype=typearray)
currentevent = 0
candidates = []
mccandidates = []

duplicates = 0
for i in xrange(0,n):
    if events[i]["event"]!=currentevent:
        candidates.sort(key=lambda x:events[x]["bscChisq"],reverse=False)
        rank=1
        for j in candidates:
            output[j]["nPass"]=len(candidates)
            output[j]["rank"]=rank
            rank+=1
            if(rank>2):
                duplicates = duplicates + 1
        del candidates[:]
        currentevent = events[i]["event"]
    if output[i]["cut"]!=0:
        candidates.append(i)

if cutOutput:
    output = output[output["cut"]!=0]
if onlyBest:
    output = output[output["rank"]==1]
if onlyOnly:
    output = output[output["nPass"]==1]

print("Number of events with a duplicate V0 = {0}".format(duplicates))
print("Total Number of V0s = {0}".format(n))
root_numpy.array2root(output,remainder[0],mode="recreate",treename="ntuple")