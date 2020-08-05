import yaml

def parse(file):
    return file

def getThreshold(FEB,hyb,chan):
    parse(file)
    return chan

def checkThinSensor(feb,hyb,FEB_thin,Hyb_thin):
    if(feb == FEB_thin and hyb == Hyb_thin):
        return True
    else:
        return False

def createDataFormat():
    data = {
        "FEB": {
            "Hyb": {
                "chan": {
                     "base0":'0'
                }
            }
        }
    }

    return data

outfile = 'test'
out = outfile+'.yml'

nFeb = 10
nHyb = 4
nChan_nom = 10 #640
nChan_thin = 512

FEB_thin = 9999
Hyb_thin = 9999

#data = dict(
#    FEB = dict(
#        hyb = dict(
#            chan = dict(
#                base0='0',base1='0',base2='0',base3='0',base4='0',base5='0',threshold='0',
#            )
#        )
#    )
#)

data = createDataFormat()

for feb in range(nFeb):
    for hyb in range(nHyb):
        if(checkThinSensor(feb,hyb,FEB_thin,Hyb_thin) == False):
            nChan = nChan_nom
        else:
            nChan = nChan_thin
        for chan in range(nChan):
            CalibKey = {
                'base0': 0,
                'base1': 1,
                'base2': 2,
                'base3': 3,
                'base4': 4,
                'base5': 5,
                'noise': 0,
                'threshold': 0,
            }
            newChanKey = {
            "CHAN{0}".format(chan):
                CalibKey
            }
            if(chan == 0):
                ChanKey = newChanKey
            else:
                ChanKey.update(newChanKey)
        newHybKey = {
        "HYB{0}".format(hyb): 
            ChanKey
        }
        if(hyb == 0):
            HybKey = newHybKey
        else:
            HybKey.update(newHybKey)
    newdata = {
    "FEB{0}".format(feb):
        HybKey
    }
    with open(out,'r') as stream:
        data_loaded = yaml.safe_load(stream) or {}
    data_loaded.update(newdata)
    with open(out,'w') as ofile:
        yaml.dump(data_loaded,ofile,default_flow_style=False)
        



#with open(out,'w') as outfile:
#    yaml.dump(data,outfile,default_flow_style=False)

with open(out,'r') as stream:
    data_loaded = yaml.safe_load(stream)

print(data == data_loaded)



