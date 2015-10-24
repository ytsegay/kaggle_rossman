library(gbm)
library (ROCR)
library(randomForest)

splitData <- function(data, testRatio=0.2) {
  retList = list()
  len <- nrow(data)
  testSize = as.integer(len*testRatio);
  
  # shuffle the data input ...
  shuffledData <- data #data[sample(nrow(data)),]
  
  retList[['testData']] <- shuffledData[1:testSize,]
  retList[['trainData']] <- shuffledData[testSize:len,]
  
  return (retList)
}


trainFile = "s:\\dataProjects\\kaggle_rossman\\c.csv"
training <- read.csv(trainFile, header=F, sep=",")
dataList <- splitData(training, 0.0)

trainData <- dataList["trainData"]$trainData
testData <- dataList["testData"]$testData

isStoreOpen = trainData[,4]
hist(isStoreOpen, breaks=3, col="red")

# remove closed stores 
trainData = trainData[trainData[,4] == 1,]

scoreDistrib <- trainData[,3]
#yTest <- testData[,3]

xTrain <- trainData[-c(3)]
#xTest <- testData[-c(3)]

hist(scoreDistrib, breaks=100, col="red")

