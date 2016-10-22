#coding = utf-8

import pickle

DATASET = 'data/EmotionSongs/Dataset'

def loadGraph(fusion_graph):
    with open(fusion_graph, 'rb') as f:
        graph = pickle.load(f)
    return graph

def loadFreq(freq_file):
    freqent_set = {}
    rf = open(freq_file, 'r')
    for line in rf:
        line = line.split()
        items = map(int, line[:-1])
        prob = float(line[-1])
        for item in items:
            if not freqent_set.has_key(item): freqent_set[item] = {}
            freqent_set[item][frozenset(items)] = prob

    for item in freqent_set:
        freq_list = sorted(freqent_set[item].iteritems(), key = lambda it : it[1], reverse = True)
        freqent_set[item] = freq_list[0][0]
    rf.close()

    return freqent_set

def rerank(graph, freqent_set, K = 20):
    cur_knn = []
    for index, g in enumerate(graph):
        cur_knn.append([index])
        if freqent_set.has_key(index):
            for item in freqent_set[index]:
                if item not in cur_knn[index]:
                    cur_knn[index].append(item)
        while len(cur_knn[index]) <= K:
            maxNode = -1; maxWeight = -1;
            for candidate in g:
                if candidate in cur_knn[index]: continue
                weight_sum = 0
                for haveSelect in cur_knn[index]:
                    if graph[haveSelect].has_key(candidate):
                        weight_sum += graph[haveSelect][candidate]
                    if graph[candidate].has_key(haveSelect):
                        weight_sum += graph[candidate][haveSelect]
                if weight_sum > maxWeight:
                    maxWeight = weight_sum
                    maxNode = candidate
            cur_knn[index].append(maxNode)
    return cur_knn

def accuracyAfterAprori(rerank, k):
    accuracy = []
    for index, knn in enumerate(rerank):
        count = 0
        for i in range(k):
            if knn[i] / 100 == index / 100: count += 1
        accuracy.append(float(count) / k)
    return sum(accuracy) / len(accuracy)

def evaluate(rerank, rank_file, K):
    from apriori_test import accuracyBeforeAprori
    print '%10s %10s %10s %10s' % ('id', 'before', 'after', 'improvement')
    for i in range(1, K + 1):
        improvement = accuracyAfterAprori(rerank, i) - accuracyBeforeAprori(rank_file, i)
        print '%10d %10f %10f %10f' % (i, 
                                       round(accuracyBeforeAprori(rank_file,i), 5), 
                                       round(accuracyAfterAprori(rerank,i), 5), 
                                       round(improvement, 5))

if __name__ == '__main__':
    fusion_graph = DATASET + '/graphs/corel-1k-graph.pickle'
    graph = loadGraph(fusion_graph)

    rank_file = DATASET + '/corel-1k_graph_fusion_results.txt'
    freq_file = DATASET + '/corel-1k_graph_fusion_freq.txt'

    # rank_file = DATASET + '/corel-1k_graph_fusion_results.txt'
    # freq_file = DATASET + '/corel_freq.txt'

    freqent_set = loadFreq(freq_file)
    K = 60
    rerank = rerank(graph, freqent_set, K)
    evaluate(rerank, rank_file, K)


