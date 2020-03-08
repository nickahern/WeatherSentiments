from datetime import datetime, timedelta
import time
from collections import namedtuple
import requests

import csv
import pandas
import scipy
import matplotlib
import numpy
import sklearn


url = "https://www.ncei.noaa.gov/orders/cdo/2069751.csv"


dataset = pandas.read_csv(url)
dataset = dataset.drop(['STATION', 'NAME'], axis = 1)
dataset = dataset.dropna()
print(dataset.shape)

def prepareDataset(data):
#Keep track of the features
    headers = list(data)

#Store the revenues of movies separately in a list
    snowIndex = headers.index('SNOW')

    datasetMatrix = data.as_matrix()
#Make the train and test splits
    datasetTrain = datasetMatrix[0:1500]
    datasetTrainWithoutLabels = np.delete(datasetTrain,YIndex,1)

    labels = datasetTrain[:,YIndex]

    datasetTest = datasetMatrix[1500:datasetMatrix.shape[0]]
    datasetTestWithoutLabels = np.delete(datasetTest,YIndex,1)

    trueLabels = datasetTest[:,YIndex]
    
    return headers,datasetMatrix,datasetTrainWithoutLabels,labels,datasetTest,datasetTestWithoutLabels,trueLabels