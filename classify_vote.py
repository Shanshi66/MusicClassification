from sklearn import metrics
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split, KFold
from sklearn.svm import SVC
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import os, csv

EMOTION_DATASET = 'data/EmotionSongs/Dataset'
feature_types = ['mvd', 'rh', 'rp', 'ssd', 'trh', 'tssd', 'mfcc']

def title(name):
    print '*' * 20
    print name
    print '*' * 20

def loadData(filename):
    data = []
    rf = open(filename, 'r')
    reader = csv.reader(rf)
    for line in reader:
        data.append([line[0]] + map(float, line[1: -1]) + [int(line[-1])])
    rf.close()
    return data

def SVM(X, y):
    # title('SVM')
    svm = SVC(kernel = 'rbf')
    svm.fit(X, y)
    return svm

def LR(X, y):
    # title('LR')
    from sklearn.linear_model import LogisticRegression
    lr = LogisticRegression(C = 0.5, penalty = 'l1', tol = 0.001, max_iter = 20000)
    lr.fit(X, y)
    return lr

def multiNB(X, y):
    from sklearn.naive_bayes import MultinomialNB
    # title('Multinomial NB')
    mnb = MultinomialNB(alpha = 0.01)
    mnb.fit(X, y)
    return mnb

def KNN(X, y):
    # title('KNN')
    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier()
    knn.fit(X, y)
    return knn

def RF(X, y):
   from sklearn.ensemble import RandomForestClassifier
   rf = RandomForestClassifier() 
   rf.fit(X, y)
   return rf
    

def evaluate(predict, test_y):
    print metrics.accuracy_score(predict, test_y)

if __name__ == '__main__':
    mp3names = [[], [], [], []]
    mp3_category = {}
    names_file = open(EMOTION_DATASET + '/mp3names.csv', 'r')

    for name in names_file: 
        name = name.split('####')
        name = [ item.strip() for item in name]
        mp3names[int(name[1])].append(name[0])
        mp3_category[name[0]] = int(name[1])
    
    # train_names , test_names = train_test_split(mp3names, test_size = 0.33)
    train_names = []; test_names = [];
    for i in range(4):
        tmp_x, tmp_y = train_test_split(mp3names[i], test_size = 0.3)
        train_names = train_names + tmp_x
        test_names = test_names + tmp_y
    
    print len(train_names), len(test_names)

    vote = {}
    for name in test_names:
        vote[name] = [0] * 4

    for feature in feature_types:
        print feature
        songs = loadData(EMOTION_DATASET + '/%s.csv' % feature)
        test_order = []; X_train = []; X_test = []; y_train = []; y_test = []
        for index, song in enumerate(songs):
            if song[0] in train_names:
                X_train.append(song[1 : -1])
                y_train.append(song[-1])
            if song[0] in test_names: 
                X_test.append(song[1 : -1])
                y_test.append(song[-1])
                test_order.append(song[0])
        
        min_len = 30000
        for sample in X_train:
            min_len = min(min_len, len(sample))
        
        for sample in X_test:
            min_len = min(min_len, len(sample))
        
        X_train = [sample[0 : min_len] for sample in X_train]
        X_test  = [sample[0 : min_len] for sample in X_test]

        scalar = StandardScaler()
        X_train = scalar.fit_transform(X_train)
        X_test = scalar.transform(X_test)
        # model = LR(X_train, y_train)
        # model = SVM(X_train, y_train)
        # model = multiNB(X_train, y_train)
        model = KNN(X_train, y_train)
        # model = RF(X_train, y_train)
        
        predict = model.predict(X_test)

        evaluate(predict, y_test)

        for index, name in enumerate(test_order):
            vote[name][predict[index]] += 1
        
    final_result = {}
    for song in vote:
        final_result[song] = vote[song].index(max(vote[song]))
    print len(final_result), len(mp3_category)
    count = 0
    for song in final_result:
        if final_result[song] == mp3_category[song]: count += 1
    
    print 'after voting'
    print float(count) / len(final_result)



    
    

