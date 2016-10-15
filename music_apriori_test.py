#coding = utf8

DATASET = 'data/EmotionSongs/Dataset'

def loadFreq():
    freqent_set = {}
    rf = open(DATASET + '/corel_freq.txt', 'r')
    for line in rf:
        line = map(int, line.split())
        for item in line:
            if not freqent_set.has_key(item): freqent_set[item] = set(line)
            else: freqent_set[item] = freqent_set[item] | set(line)
    rf.close()
    return freqent_set

def accuracyBeforeAprori(k = 20):
    rf = open(DATASET + '/corel-1k.txt', 'r')
    accuracy = []
    for line in rf:
        line = map(int, line.split()[1:])
        count = 0
        for i in xrange(k):
            if line[i] / 100 == line[0] / 100: count += 1
        accuracy.append(float(count) / k)
    print sum(accuracy) / len(accuracy)
    rf.close()

def accuracyAfterAprori(k = 20):
    rf = open(DATASET + '/corel-1k.txt', 'r')
    accuracy = []
    for line in rf:
        line = map(int, line.split()[1:])
        count = 0
        current_knn = set()
        if line[0] in freqent_set:
            current_knn = current_knn | freqent_set[line[0]]
        for item in line:
            if len(current_knn) >= k: break
            current_knn = current_knn | set([item])
        for item in current_knn:
            if item / 100 == line[0] / 100: count += 1
        accuracy.append(float(count) / k)
    print sum(accuracy) / len(accuracy)
    rf.close()

accuracyBeforeAprori(2)
accuracyAfterAprori(2)
