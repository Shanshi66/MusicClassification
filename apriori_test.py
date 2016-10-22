#coding = utf8

DATASET = 'data/EmotionSongs/Dataset'

freqent_set = {}

def loadFreq(freq_file):
    rf = open(freq_file, 'r')
    _max = -1
    _min = 1000
    for line in rf:
        line = line.split()
        items = map(int, line[:-1])
        prob = float(line[-1])
        for item in items:
            freqent_set.get(item, {})
            if not freqent_set.has_key(item): freqent_set[item] = {}
            for it in items:
                if not freqent_set[item].has_key(it): freqent_set[item][it] = 0
                freqent_set[item][it] = max(freqent_set[item][it], prob)
            # if not freqent_set.has_key(item): freqent_set[item] = set(line)
            # else: freqent_set[item] = freqent_set[item] | set(line)
            _max = max(_max, len(freqent_set[item]))
            _min = min(_min, len(freqent_set[item]))
    print _max, _min
    rf.close()

def accuracyBeforeAprori(rank_file, k = 20):
    rf = open(rank_file, 'r')
    accuracy = []
    for line in rf:
        line = map(int, line.split()[1:])
        count = 0
        for i in xrange(k):
            if line[i] / 100 == line[0] / 100: count += 1
        accuracy.append(float(count) / k)
    rf.close()
    return sum(accuracy) / len(accuracy)

def accuracyAfterAprori(rank_file, k = 20):
    rf = open(rank_file, 'r')
    accuracy = []
    for line in rf:
        line = map(int, line.split()[1:])
        count = 0
        current_knn = set()
        if line[0] in freqent_set:
            # if len(freqent_set[line[0]]) > k:
            #     for item in freqent_set[line[0]]:
            #         if len(current_knn) >= k: break
            #         if item != line[0]: current_knn.add(item)
            # else:
            # if len(freqent_set[line[0]]) > k / 2:
            # bias = k / 2
            bias = k
            # bias = 2
            if len(freqent_set[line[0]]) > bias:
                freq_list = sorted(freqent_set[line[0]].iteritems(), key = lambda it : it[1] , reverse = True)
                freq_list = [ x[0] for x in freq_list]
                current_knn = current_knn | set(freq_list[0 : bias])
            else:
                current_knn = current_knn | set(freqent_set[line[0]])
        for item in line:
            if len(current_knn) >= k: break
            current_knn = current_knn | set([item])
        for item in current_knn:
            if item / 100 == line[0] / 100: count += 1
        accuracy.append(float(count) / k)
    rf.close()
    return sum(accuracy) / len(accuracy)

def evaluate(rank_file, freq_file):
    loadFreq(freq_file)
    print '%10s %10s %10s %10s' % ('id', 'before', 'after', 'improvement')
    for i in range(1, 21):
        improvement = accuracyAfterAprori(rank_file, i) - accuracyBeforeAprori(rank_file, i)
        print '%10d %10f %10f %10f' % (i, 
                                       round(accuracyBeforeAprori(rank_file,i), 4), 
                                       round(accuracyAfterAprori(rank_file,i), 4), 
                                       round(improvement, 4))

if __name__ == '__main__':
    # freq_file  = DATASET + '/corel_cnn_freq.txt'
    # rank_file = DATASET + '/corel-1k_rank_cnn.txt'
    rank_file = DATASET + '/corel-1k.txt'
    freq_file = DATASET + '/corel_freq.txt'

    # rank_file = DATASET + '/corel-10k_graph_fusion_results.txt'
    # freq_file = DATASET + '/corel-10k_freq.txt'
    evaluate(rank_file, freq_file)

