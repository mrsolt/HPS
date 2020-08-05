import os 
from os.path import dirname
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotUtils
from DataParser import DataParser
from CsvParser  import CsvParser

plt.style.use('ggplot')

n_estimators = 100
max_depth = 15
minVZ = -20
maxVZ = 60

output = "test2"
#signal_file = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/MachineLearing/AnalysisWorkshopML/ap-beam_100MeV_4e9.csv'
#background_file = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/MachineLearing/AnalysisWorkshopML/tritrig-wab-beam_100MeV_L1L1_tight.csv'
signal_file = '~/CS230/cs230-project/notebooks/datasets/ap_100MeV_L1L1_tight_08mm.csv'
background_file = '~/CS230/cs230-project/notebooks/datasets/tritrig-wab-beam_100MeV_L1L1_tight.csv'

background = CsvParser(background_file)
signal     = CsvParser(signal_file)

param_min = []
param_max = []
param_min.append(minVZ)
param_max.append(maxVZ)

myData     = DataParser(signal=signal, background=background)

X_train, Y_train, X_test, Y_test, classes = myData.load_dataset()
print(Y_train.shape)
print(Y_test.shape)

X_train = X_train.T
Y_train = Y_train.T
X_test = X_test.T
Y_test = Y_test.T

from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth,random_state=0)

n_test = 0
for i in range(Y_test.shape[0]):
    if(Y_test[i] == 0):
        n_test = n_test + 1
print("n_test {0}".format(n_test))

print("Fitting Data")
clf.fit(X_train, Y_train) 
print("Fitting Complete. Making plots") 

#plot

clf_cut_train, tpr_at_threshold_train = plotUtils.MakePlots(clf, X_train, Y_train, param_min, param_max, n_test, clf_cut=0.5, PDFbasename=output+"_train")
_, tpr_at_threshold_test = plotUtils.MakePlots(clf, X_test, Y_test, param_min, param_max, n_test, clf_cut=clf_cut_train, PDFbasename=output+"_test")
