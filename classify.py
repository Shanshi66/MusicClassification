from sklearn import metrics
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split, KFold
from sklearn.svm import SVC
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import os, csv


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

def title(name):
    print '*' * 20
    print name
    print '*' * 20

def loadData(filename):
    X = []; y = []
    rf = open(filename, 'r')
    reader = csv.reader(rf)
    for line in reader:
        X.append(map(float, line[0 : -1]))
        y.append(int(line[-1]))
    rf.close()
    return X, y

def evaluate(model, test_X, test_y):
    predict = model.predict(test_X)
    print metrics.accuracy_score(predict, test_y)

EMOTION_DATASET = 'data/EmotionSongs/Dataset'
feature_types = ['mvd', 'rh', 'rp', 'ssd', 'trh', 'tssd']

if __name__ == '__main__':
    X, y = loadData(EMOTION_DATASET + '/sunmuxin5.csv')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

    scalar = StandardScaler()
    X_train = scalar.fit_transform(X_train)
    X_test = scalar.transform(X_test)

    model = SVM(X_train, y_train)
    # model = KNN(X_train, y_train)
    # model = RF(X_train, y_train)
    # model = LR(X_train, y_train)
    # model = multiNB(X_train, y_train)
    evaluate(model, X_test, y_test)



    
    

