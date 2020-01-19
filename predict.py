import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor

def createRandomForest():
    clf = RandomForestRegressor(n_estimators=50)
    return clf

def createExtraTree():
    clf = ExtraTreesRegressor(n_estimators=50)
    return clf

def classify(clf, train, features, target, test, filePath):

    clf.fit(train[features], train[target])

    with open(filePath, "w") as outfile:
        outfile.write("Id,Prediction\n")
        for index, value in enumerate(list(clf.predict(test[features]))):
            outfile.write("%s,%s\n" % (test['Id'].loc[index], value))

def splitSampleTime(data):

    sub = pd.DataFrame(data.sample_time.str.split(' ').tolist(), columns="date time".split())
    date = pd.DataFrame(sub.date.str.split('-').tolist(), columns="year month day".split())
    time = pd.DataFrame(sub.time.str.split(':').tolist(), columns="hour minute second".split())
    
    data['year'] = date['year']
    data['month'] = date['month']
    data['day'] = date['day']

    data['hour'] = time['hour']
    data['minute'] = time['minute']

    return data

def mapID(data):
    
    coded = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7}
    data['m_id'] = data['m_id'].astype(str).map(coded)
    
    return data

train=pd.read_csv("./input/train.csv")
test=pd.read_csv("./input/test.csv")

train = splitSampleTime(train)
train = mapID(train)

test = splitSampleTime(test)
test = mapID(test)

target = 'cpu_01_busy'
features = [col for col in train.columns if col not in ['cpu_01_busy', 'sample_time']]

clf = createExtraTree()
classify(clf, train, features, target, test, "./output/extratree.csv")

clf = createRandomForest()
classify(clf, train, features, target, test, "./output/randomforest.csv")