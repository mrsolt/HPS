import os 
from os.path import dirname
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from DataParser import DataParser
from CsvParser  import CsvParser

#data_dir        = os.path.join(os.getcwd(), '../notebooks/datasets')
#signal_file     = 'ap_100MeV_L1L1_tight_08mm.csv'
#background_file = 'tritrig-wab-beam_100MeV_L1L1_tight.csv'
signal_file = '~/hps/Data2016/MachineLearning/files/test_ap80MeV.csv'
background_file = '~/hps/Data2016/MachineLearning/files/test_tritrig-wab-beam80MeV.csv'

#background = CsvParser(os.path.join(data_dir, background_file))
#signal     = CsvParser(os.path.join(data_dir, signal_file))

background = CsvParser(background_file)
signal     = CsvParser(signal_file)

myData     = DataParser(signal=signal, background=background)

X_train, Y_train, X_test, Y_test, classes = myData.load_dataset()

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
clf = RandomForestClassifier(n_estimators=100, max_depth=10,
                             random_state=0)

X_train = X_train.T
Y_train = Y_train.T

clf.fit(X_train, Y_train)

importances = clf.feature_importances_
std = np.std([tree.feature_importances_ for tree in clf.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]
#column_select = ['vz','vzPull','vx','vy','vxPull','vyPull', 'uncM', 'eleZ0', 'posZ0', 'eleTrkD0', 'posTrkD0', 'projX', 'projY', 'projXPull', 'projYPull', 'uncP', 'eleP', 'posP', 'eleTrkTanLambda','eleTrkD0Err','eleTrkTanLambdaErr','eleTrkZ0Err','posTrkTanLambda','posTrkD0Err','posTrkTanLambdaErr','posTrkZ0Err']
#column_select = ['vx','vy','vxPull','vyPull', 'uncM', 'eleZ0', 'posZ0', 'eleTrkD0', 'posTrkD0', 'projX', 'projY', 'projXPull', 'projYPull', 'uncP', 'eleP', 'posP', 'eleTrkTanLambda','eleTrkD0Err','eleTrkTanLambdaErr','eleTrkZ0Err','posTrkTanLambda','posTrkD0Err','posTrkTanLambdaErr','posTrkZ0Err']
#column_select = ['vz','vzPull','vy','vyPull', 'uncM', 'eleZ0', 'posZ0', 'projY', 'projYPull', 'uncP', 'eleTrkTanLambda','eleTrkTanLambdaErr','eleTrkZ0Err','posTrkTanLambda','posTrkTanLambdaErr','posTrkZ0Err']
#column_select = ['vy','vyPull', 'uncM', 'eleZ0', 'posZ0', 'projY', 'projYPull', 'uncP', 'eleTrkTanLambda','eleTrkTanLambdaErr','eleTrkZ0Err','posTrkTanLambda','posTrkTanLambdaErr','posTrkZ0Err']
#column_select = ['vy','vyPull', 'uncM', 'eleZ0', 'posZ0', 'projY', 'eleTrkTanLambda','posTrkTanLambda']
#column_select = ['vz','vzPull','vy','vyPull', 'uncM', 'eleZ0', 'posZ0', 'projY', 'eleTrkTanLambda','posTrkTanLambda']
column_select = ['vz', 'vzPull', 'vxPull', 'vyPull', 'uncM', 'eleZ0', 'posZ0', 'projXPull', 'projYPull', 'eleTrkTanLambda','posTrkTanLambda', 'eleP', 'posP']

column_sort = []

for f in range(X_train.shape[1]):
    column_sort.append(column_select[indices[f]])

PNGname = "importances_final.png"

plt.figure(figsize=(20,16))
plt.title("Feature importances",fontsize=40)
plt.bar(range(X_train.shape[1]), importances[indices],
        color="r", align="center")
plt.xticks(range(X_train.shape[1]), column_sort)
plt.xlim([-1, X_train.shape[1]])
plt.savefig(PNGname)