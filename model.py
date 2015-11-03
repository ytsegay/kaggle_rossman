from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.svm import NuSVR
import pandas as pd
import numpy as np
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
            diffPercentage = (truth[i] - predict[i]) / truth[i]
            total += (diffPercentage * diffPercentage)
            counter += 1
    # print total, counter
    return math.sqrt(total / counter)


def runEVal():
    nTrees = 1900

    df = pd.read_csv("c2.csv", parse_dates=True)

    # how many days had a zero sale
    zeroSalesDays = df[df.Sales <= 0]

    # remove zero sales
    dfNoZeroSales = df.drop(df[df.Sales <= 0].index)

    # all data after may 2015 (including may) is considered for testing
    dfTrain = dfNoZeroSales[(dfNoZeroSales.trainYear < 2015)]
    dfTest = dfNoZeroSales[((dfNoZeroSales.trainYear >= 2015) & (dfNoZeroSales.trainMonth >= 5))]

    yTrain = dfTrain.Sales
    yTest = dfTest.Sales

    xTrain = dfTrain.drop('Sales', axis=1)
    xTest = dfTest.drop('Sales', axis=1)

    # given the skewed nature of the labels, lets take a log
    yTestlog = yTest.apply(lambda x: np.log1p(x))
    yTrainlog = yTrain.apply(lambda x: np.log1p(x))

    # TODO: need to shuffle data

    clfs = {
        "RF" : RandomForestRegressor(n_estimators=nTrees, n_jobs=5, verbose=1)#
        #"GBT" : GradientBoostingRegressor(n_estimators=nTrees, verbose=1, max_depth=10)
        #"LR": LinearRegression(),
    }

    # TODO: need to shuffle
    print "Train: ", len(yTrain)
    print "Test: ", len(yTest)
    print xTrain.columns

    for key, clf in clfs.iteritems():
        print "Processing ", key
        clf.fit(xTrain, yTrainlog)
        pred = clf.predict(xTest)
        print "RMSPE: ", RMSPE(yTestlog, pred)

        feature_importance = clf.feature_importances_
        # make importances relative to max importance
        feature_importance = 100.0 * (feature_importance / feature_importance.max())
        sorted_idx = np.argsort(feature_importance)

        print "feature importance: \n\n"
        for idx in sorted_idx:
            print xTrain.columns[idx], feature_importance[idx]


import time

start = time.time()
runEVal()
end = time.time()
print end - start
