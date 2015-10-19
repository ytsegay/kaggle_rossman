__author__ = 'ytsegay'

import csv
from time import strptime
import numpy

def main():
    stores = {}

    # read training file and match it to the stores file
    with open("data/store.csv", "rb") as f:
        reader = csv.reader(f)
        for row in reader:
            stores[row[0]] = row

    counter = 0

    # read training file and match it to the stores file
    with open("data/train.csv", "rb") as f:
        reader = csv.reader(f)
        for row in reader:
            joined = [entry.replace(",", "-") for entry in row + stores[row[0]][1:]]
            if counter > 0:

                compOpenDateTransformer(joined)
                promo2DateTransformer(joined)
                joined = oneHotEncPromoInterval(joined)
                joined = transformDate(joined)
                fillMissingValues(joined)

                #joined += oneHotEncode(joined[10], ['a', 'b', 'c'])
                #joined += oneHotEncode(joined[9], ['a', 'b', 'c', 'd'])
                #joined += oneHotEncode(joined[7], ['a', 'b', 'c', '0'])

                del joined[17]  # promoIntervals
                del joined[4]   # customers count
                del joined[2]   # date

                print ",".join(joined)
            #else:
            #    print ",".join(joined)
            counter += 1


def fillMissingValues(parts):
    for i in xrange(len(parts)):
        if parts[i].strip() == "":
            parts[i] = "-1"

# convert the year to a relative quantity, relative to min
def compOpenDateTransformer(parts):
    minYear = 1900
    if parts[13].strip() != "" and parts[12].strip() != "":
        parts[13] = str(int(parts[13])-minYear)
    else:
        parts[13] = "-1"
        parts[12] = "-1"

# same as compOpenDateTransformer
def promo2DateTransformer(parts):
    minYear = 2000
    if parts[15].strip() != "" and parts[15].strip() != "":
        parts[16] = str(int(parts[16])-minYear)
        #return [parts[15], str(int(parts[16])-minYear)]
    else:
        parts[16] = "-1"
        parts[15] = "-1"

# one hot encode the promo interval and remove the textual representation
def oneHotEncPromoInterval(parts):
    numMonths = ['0','0','0','0','0','0','0','0','0','0','0','0','0']
    if parts[17].strip() != "":
        months = parts[17].strip().split("-")

        for month in months:
            numMonths[monthToNum(month)] = '1'
    # remove the month column
    #del parts[-1]
    return parts + numMonths[1:]

def oneHotEncode(value, allPossibleValues):
    # construct a map of category to index
    mp = {}
    index = 0
    for val in allPossibleValues:
        mp[val] = index
        index += 1

    ret = ['0'] * index
    ret[mp[value]] = '1'
    return ret


def transformDate(parts):
    dateParts = parts[2].strip().split("-")
    #del parts[2]
    return parts + dateParts

def monthToNum(date):
    return{
            'Jan' : 1,
            'Feb' : 2,
            'Mar' : 3,
            'Apr' : 4,
            'May' : 5,
            'Jun' : 6,
            'Jul' : 7,
            'Aug' : 8,
            'Sept' : 9,
            'Oct' : 10,
            'Nov' : 11,
            'Dec' : 12
    }[date]

if __name__ == "__main__":
    main()
