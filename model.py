import math
import random
import numpy
import csv
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import ShuffleSplit
from sklearn.linear_model import Ridge
from sklearn.svm import NuSVR


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

def shuffleSplitTimeOrdered(x):
    i = 0
    trainIndex = []
    testIndex = []
    for row in x:
        if row[23] == 2015 and row[24] >= 5:
            testIndex.append(i)
        else:
            trainIndex.append(i)
        i += 1
    random.shuffle(trainIndex)
    random.shuffle(testIndex)

    return [trainIndex, testIndex]

def runEVal():
    nTrees = 1900

    temp = []
    counter = 0
    with open("c2.csv", "rb") as f:
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
    #data[:, 5] = LabelEncoder().fit_transform(data[:,6]) #state holiday
    #data[:, 7] = LabelEncoder().fit_transform(data[:,8]) #storetype
    #data[:, 8] = LabelEncoder().fit_transform(data[:,9]) #assortment


    # labels minus the title
    y = data[1:, 2]
    # training
    x = numpy.delete(data, 2, 1)
    # headers
    headers = x[0,:]

    # remove headers
    x = numpy.delete(x, 0, 0)

    print headers
    print x[1:2,:]

    #thus far the data is in string format
    y = numpy.log1p(y.astype(float))
    #y = y.astype(float)
    x = x.astype(int)

    del data

    clfs = {#"RF" : ExtraTreesRegressor(n_estimators=nTrees, n_jobs=5, verbose=1)
            "GBT" : GradientBoostingRegressor(n_estimators=nTrees, verbose=1, max_depth=10)
	        }

    #cv = ShuffleSplit(len(y), n_iter=1, test_size=0.1)
    cv = shuffleSplitTimeOrdered(x)
    trainIndex = cv[0]
    testIndex = cv[1]

    xTrain = x[trainIndex,:]
    yTrain = y[trainIndex]
    xTest = x[testIndex,:]
    yTest = y[testIndex]

    print "Train: ",len(yTrain)
    print "Test: ",len(yTest)

    for key, clf in clfs.iteritems():
        print "Processing ",key
        clf.fit(xTrain, yTrain)
        pred = clf.predict(xTest)
        #predBase10 = numpy.expm1(pred)
        print "RMSPE: ", RMSPE(yTest, pred)

        feature_importance = clf.feature_importances_
        # make importances relative to max importance
        feature_importance = 100.0 * (feature_importance / feature_importance.max())
        sorted_idx = numpy.argsort(feature_importance)

        print "feature importance: \n\n"
        for idx in sorted_idx:
            print headers[idx], feature_importance[idx]



import time

start = time.time()
runEVal()
end = time.time()
print end - start
