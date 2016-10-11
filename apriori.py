#coding=utf-8

import sys

EMOTION = 'data/EmotionSongs/Dataset'

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return set(map(frozenset, C1))

def scanD(D, Ck, minSupport):
    ssCnt = {}
    for transaction in D:
        for can in Ck:
            if can.issubset(transaction):
                ssCnt[can] = ssCnt.get(can, 0) + 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData

def apriori(dataset, minSup, maxk = 5):
    dataset = map(set, dataset)
    L = []; k = 1
    while True:
        if k == 1: Ck = createC1(dataset)
        Lk, supK = scanD(dataset, Ck, minSup)
        print '%10d\t%d' % (len(Lk), k)
        if not Lk: break
        if k == maxk: break;
        L.append(Lk)
        Ck = aprioriGen(L[-1], k)
        k += 1
    return L

def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in xrange(lenLk):
        for j in xrange(i + 1, lenLk):
            ret = Lk[i] | Lk[j]
            if len(ret) == k + 1: retList.append(frozenset(sorted(list(ret))))
    
    return set(retList)

print 'corel'
dataset = []
rf = open(EMOTION + '/corel-1k.txt', 'r')
for line in rf:
    line = line.split()[1:50]
    line = [int(item.strip()) for item in line]
    dataset.append(line)
rf.close()

# D = [['A','B','C','D'],['B','C','E'],['A','B','C','E'],['B','D','E'],['A','B','C','D']]
freqent_set = apriori(dataset, 0.1, 5)

wf = open(EMOTION + '/corel_freq.txt', 'w')
for item in freqent_set:
    item = list(item)
    item = [list(it) for it in item]
    for it in item:
        wf.write('%s\n' % (' '.join([str(i) for i in it])))
wf.close()

feature_types = ['mvd', 'rh', 'rp', 'ssd', 'trh', 'tssd']

for f in feature_types:
    print f
    dataset = []
    rf = open(EMOTION + '/%s_rank.csv' % f, 'r')
    for line in rf:
        line = line.split(',')[0:50]
        line = [int(item.strip()) for item in line]
        dataset.append(line)
    rf.close()
    freqent_set = apriori(dataset, 0.1, 5)
    wf = open(EMOTION + '/%s_freq.txt' % f, 'w')
    for item in freqent_set:
        item = list(item)
        item = [list(it) for it in item]
        for it in item:
            wf.write('%s\n' % (' '.join([str(i) for i in it])))
    wf.close()