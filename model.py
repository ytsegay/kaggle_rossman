import numpy
import csv
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import ShuffleSplit
from sklearn.linear_model import Ridge
from sklearn.svm import NuSVR
import math


__author__ = 'ytsegay'

# compute root mean square percentage error
# a measure of deviation from the truth in percentage
def RMSPE(truth, predict):
    assert len(truth) == len(predict)
    total = 0.0
    counter = 0
    for i in xrange(len(truth)):
        if truth[i] > 0:
            diffPercentage = (truth[i] - predict[i])/truth[i]
            total += (diffPercentage*diffPercentage)
            counter += 1
    #print total, counter
    return math.sqrt(total/counter)


def runEVal():
    nTrees = 900

    temp = []
    counter = 0
    with open("c.csv", "rb") as f:
        reader = csv.reader(f)
        for row in reader:
            # remove days on which stores were closed.
            # it however might be usef
            if row[3] != '0':
                temp.append(row)
                counter += 1
            else:
                if row[3] == '0' and row[2] != '0':
                    print row[3], row[2]

    print counter

    data = numpy.array(temp)
    del temp
    data[:, 5] = LabelEncoder().fit_transform(data[:,6]) #state holiday
    data[:, 7] = LabelEncoder().fit_transform(data[:,8]) #storetype
    data[:, 8] = LabelEncoder().fit_transform(data[:,9]) #assortment

    # label
    y = data[:, 2]
    # training
    x = numpy.delete(data, 2, 1)

    #thus far the data is in string format
    #y = numpy.log(y.astype(float)+1)
    y = y.astype(float)
    x = x.astype(int)

#    cv = ShuffleSplit(len(y), n_iter=3, test_size=0.1)
#    for trainIndex, testIndex in cv:
#        xTrain = x[trainIndex,:]
#        yTrain = y[trainIndex]
#        xTest = x[testIndex,:]
#        yTest = y[testIndex]
    
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.1, random_state=42)
    print "Train: ",len(yTrain)
    print "Test: ",len(yTest)

    clfs = {"RF" : RandomForestRegressor(n_estimators=nTrees, n_jobs=2, verbose=1),
            "GBT" : GradientBoostingRegressor(n_estimators=nTrees, verbose=1)}

    for key, clf in clfs.iteritems():
        print "Processing ",key
        clf.fit(xTrain, yTrain)
        pred = clf.predict(xTest)
        #predBase10 = numpy.expm1(pred)
        print RMSPE(yTest, pred)


runEVal()
