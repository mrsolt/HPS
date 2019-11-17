import ROOT as r
import os
import utilities as utils


utils.SetStyle()

path = ""
inFileList = [
    "nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/10per_L1L1_cleanup_nPos_plots.root",
    "nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/plots/tritrig-wab-beam_L1L1_cleanup_nPos.root"]
#inFileList = [
#    "home/mrsolt/hps/Data2016/pass4/fullplots.root",
#    "home/mrsolt/hps/Data2016/pass4/fullplots.root"]

#inFileList = [
#    "nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/10per_L1L2_cleanup_nPos_plots.root",
#    "nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/plots/tritrig-wab-beam_L1L2_cleanup_nPos.root"]

#inFileList = [
#    "nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/10per_L2L2_cleanup_nPos_plots.root",
#    "nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/plots/tritrig-wab-beam_L2L2_cleanup_nPos.root"]



colors = [r.kBlack, r.kRed, r.kBlue, r.kGreen+2, r.kOrange-2]

inputFiles = []
legends     = ["10% Data","100% tritrig-wab-beam"]
outdir     = "./"

if not os.path.exists(outdir):
    os.makedirs(outdir)

r.gROOT.SetBatch(1)

for ifile in inFileList:
    inf = r.TFile(path+"/"+ifile)
    inputFiles.append(inf)
    pass

canvs = []
for key in inputFiles[0].GetListOfKeys():
    histos = []
    print key.GetName()
    c = r.TCanvas()
    for i_f in range(0,len(inputFiles)):
        histos.append(inputFiles[i_f].Get(key.GetName()))
        if(histos[i_f] == None): continue
        histos[i_f].SetMarkerColor(colors[i_f])
        histos[i_f].SetLineColor(colors[i_f])
        pass
    if(histos == []): continue
    canvs.append(utils.MakePlot(key.GetName(),outdir,histos,legends,".png",LogY=True,RatioType="Sequential",Normalise=True))
    pass

outF = r.TFile("10per_L1L1_cleanup_nPos_compareplots.root","RECREATE")
#outF = r.TFile("10per_L1L2_cleanup_nPos_compareplots.root","RECREATE")
#outF = r.TFile("10per_L2L2_cleanup_nPos_compareplots.root","RECREATE")
outF.cd()
for canv in canvs: canv.Write()
outF.Close()