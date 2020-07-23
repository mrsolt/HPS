import os 
from os.path import dirname
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotUtils
from DataParser import DataParser
from CsvParser  import CsvParser
from DataParser2 import DataParser2
from CsvParser2  import CsvParser2
from joblib import dump, load
import array
import csv

plt.style.use('ggplot')

n_estimators = 100
max_depth = 10
targZ = -4.3
nBins = 100
minVZ = -20
maxVZ = 60
uncVZi = 0

param_min = []
param_max = []
param_min.append(minVZ)
param_max.append(maxVZ)

outfile = "test"
infile = "test"

massArr = array.array('d')
massArr.append(0.080)
massArr.append(0.090)
massArr.append(0.100)

clf_cut = array.array('d')
clf_cut.append(0.95)
clf_cut.append(0.95)
clf_cut.append(0.95)

for i in range(len(massArr)):
	mass = massArr[i] * 1000
	print(mass)
	clf = load("Models/{0}_{1:0.0f}.joblib".format(infile,mass))
	signal_file = '~/hps/Data2016/MachineLearning/files/ap{0:0.0f}MeV.csv'.format(mass)
	data_file = '~/hps/Data2016/MachineLearning/files/{0:0.0f}MeV_10per.csv'.format(mass)

	data = CsvParser(data_file)
	signal = CsvParser(signal_file)
	signalz = CsvParser2(signal_file)

	myData     = DataParser(signal=signal, background=data)
	myData_data     = DataParser2(sample=data)
	myData_signal     = DataParser2(sample=signal)
	myData_signalz     = DataParser2(sample=signalz)

	X_all, Y_all, _, _, classes = myData.load_dataset(test_size=1e-9)
	X_data, Y_data, classes = myData_data.load_dataset()
	X_sig, Y_sig, classes = myData_signal.load_dataset()
	X_sigz, Y_sigz, classesz = myData_signalz.load_dataset()

	X_all = X_all.T
	Y_all = Y_all.T
	X_data = X_data.T
	Y_data = Y_data.T
	X_sig = X_sig.T
	Y_sig = Y_sig.T
	X_sigz = X_sigz.T
	Y_sigz = Y_sigz.T

	_, _ = plotUtils.MakePlots(clf, X_all, Y_all, param_min, param_max, Y_data.shape[0], clf_cut=clf_cut[i], PDFbasename="Plots/"+outfile+"_data_{0:0.0f}".format(mass))

	with open('/home/mrsolt/hps/Data2016/MachineLearning/CsvFinal/{0}_{1:0.0f}MeV_sig.csv'.format(outfile,mass), mode='w') as output_file:
		file_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		file_writer.writerow(["truthZ","clf"])
		for j in range(Y_sig.shape[0]):
			X = X_sig[j,:].reshape(1,-1)
			y_predictions_proba = clf.predict_proba(X)
			if(y_predictions_proba[0,1] > clf_cut[i]):
				Xz = X_sigz[j,:].reshape(1,-1)
				file_writer.writerow([str(Xz[0, 0]),str(y_predictions_proba[0,1])])

	with open('/home/mrsolt/hps/Data2016/MachineLearning/CsvFinal/{0}_{1:0.0f}MeV_data.csv'.format(outfile,mass), mode='w') as output_file:
		file_writer2 = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		file_writer2.writerow(["uncVZ","clf"])
		for j in range(Y_data.shape[0]):
			X = X_data[j,:].reshape(1,-1)
			y_predictions_proba = clf.predict_proba(X)
			if(y_predictions_proba[0,1] > clf_cut[i]):
				file_writer2.writerow([str(X[0, uncVZi]),str(y_predictions_proba[0,1])])