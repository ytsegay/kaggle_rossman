import numpy
import csv
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
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
    temp = []
    with open("c.csv", "rb") as f:
            reader = csv.reader(f)
            for row in reader:
                temp.append(row)


    data = numpy.array(temp)
    data[:,6] = LabelEncoder().fit_transform(data[:,6]) #state holiday
    data[:,8] = LabelEncoder().fit_transform(data[:,8]) #storetype
    data[:,9] = LabelEncoder().fit_transform(data[:,9]) #assortment

    # label
    y = data[:,2]
    # training
    x = numpy.delete(data, 2, 1)

    #thus far the data is in string format
    y = y.astype(float)
    x = x.astype(int)

    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.33, random_state=42)

    from sklearn import linear_model
    clf = linear_model.LinearRegression()

    clfs = {"RandomForestRegressor": RandomForestRegressor(n_estimators=150),
            "GradientBoostingRegressor": GradientBoostingRegressor(n_estimators=150),
            "SVR_RBF": SVR(kernel='rbf', C=1e3, gamma=0.1),
            "SVR_LINEAR": SVR(kernel='linear', C=1e3),
            "SVR_POLY": SVR(kernel='poly', C=1e3, degree=2)}

    for k,clf in clfs.iteritems():
        clf.fit(xTrain, yTrain)
        pred = clf.predict(xTest)

        print k,RMSPE(yTest, pred)


runEVal()
