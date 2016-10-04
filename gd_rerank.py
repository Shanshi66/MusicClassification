import numpy
import cPickle
import re
import os
import csv

feature_types = ['mvd', 'rh', 'rp', 'ssd', 'trh', 'tssd']
# DATASET = 'data/EmotionSongs/Dataset'
DATASET = 'data/GTZAN/Dataset'
CLASS = 10

############################## Load data ##############################

def load_data(rank_file):
    print "Load data"
    rank_file = open(rank_file, 'r')
    reader = csv.reader(rank_file)
    lables = []
    features = []
    for line in reader:
        line = map(int, line)
        lables.append(line[0])
        features.append(line[1 : ])

    rank_file.close()
    return lables, features, len(features)

############################## Reciprocal neighbors ###################

def find_reciprocal_neighbors(lables, features, music_amount,
                              rerank_file, graph_folder,
                              search_region, kNN, retri_amount, f):

    print "Find reciprocal neighbors"

    rerank_file = open(rerank_file, 'w')
    writer = csv.writer(rerank_file)

    # build a reciprocal neighbor graph for each image
    for i in range(music_amount):
        # print '%s\t%d' % (f, i)
        result_graph = {}
        # 1st layer: choose reciprocal neighbors only
        qualified_list = []
        result_graph[i] = []
        for j in range(search_region):
            cur_id = features[i][j]
            cur_id_kNN = features[cur_id][0 : kNN]
            if i in cur_id_kNN:
                qualified_list.append(cur_id)
                result_graph[i].append([cur_id, 1.0])
                if result_graph.has_key(cur_id):
                    result_graph[cur_id].append([i, 1.0])
                else:
                    result_graph[cur_id] = [[i, 1.0]]

        # 2nd layer: choose neighbors of reciprocal neighbors
        for j in range(len(qualified_list)):
            cur_id = qualified_list[j]
            cur_id_kNN = features[cur_id][0 : kNN]
            common_set = set(cur_id_kNN) & set(qualified_list)
            diff_set = set(cur_id_kNN) - set(qualified_list)
            union_set = set(cur_id_kNN) | set(qualified_list)
            # (rule 1: at least half of the close set) or (rule 2: bring less unknown)
            weight = float(len(common_set))/len(union_set)
            #if (len(common_set)-1) >= (len(qualified_list)-1)/2.0 or len(diff_set) <= (len(common_set)-1):
            if weight > 0.3: # works for 0.1-0.4
                for k in range(len(cur_id_kNN)):
                    if cur_id_kNN[k] not in result_graph.keys():
                        result_graph[cur_id_kNN[k]] = [[cur_id, weight]]
                    else:
                        result_graph[cur_id_kNN[k]].append([cur_id, weight])
                    if cur_id_kNN[k] not in qualified_list:
                        qualified_list.append(cur_id_kNN[k])

        # add more images if the candidates are less than the threshold. store them in results_graph[-1]
        if len(qualified_list) <= retri_amount:
            for j in range(retri_amount):
                cur_id = features[i][j]
                if cur_id not in qualified_list:
                    qualified_list.append(cur_id)
                    if -1 not in result_graph.keys():
                        result_graph[-1] = [cur_id]
                    else:
                        result_graph[-1].append(cur_id)

        # save the reranking results, same format as the input
        
        writer.writerow([i] + qualified_list)

        # save graph files for each image

        fn_graph = graph_folder + '/%d.%s' % (i, f)
        cPickle.dump(result_graph, open(fn_graph, 'wb'))

    rerank_file.close()


name2label = {}
categories = {}
def loadLabel():
    label_file = open(DATASET + '/labels.csv', 'r')
    for line in label_file:
        line = line.split('####')
        line  = [item.strip() for item in line]

        name = line[0]
        label = int(line[1])
        category = int(line[2])

        name2label[name] = label
        categories[label] = category
    label_file.close()

def evaluate(predict):
    count = 0
    for song in predict:
        if predict[song] == categories[song]: count += 1
    return float(count) / len(predict)

def knnBeforeRerank(feature, K):
    rank_file = open(DATASET + '/%s_rank.csv' % feature, 'r')
    reader = csv.reader(rank_file)
    vote = {}
    predict = {}
    for line in reader:
        line = map(int, line)
        vote[line[0]] = [0] * CLASS
        for i in range(1, K + 1):
            vote[line[0]][categories[line[i]]] += 1
        predict[line[0]] = vote[line[0]].index(max(vote[line[0]]))
    rank_file.close()
    return predict

def knnAfterRerank(feature, K):
    rerank_file = open(DATASET + '/%s_rerank.csv' % feature, 'r')
    reader = csv.reader(rerank_file)
    vote = {}
    predict = {}
    for line in reader:
        line = map(int, line)
        vote[line[0]] = [0] * CLASS
        for i in range(1, K + 1):
            vote[line[0]][categories[line[i]]] += 1
        predict[line[0]] = vote[line[0]].index(max(vote[line[0]]))
    rerank_file.close()
    return predict

if __name__=='__main__':
    loadLabel()
    for f in feature_types:
        rank_file = DATASET + '/%s_rank.csv' % f
        rerank_file = DATASET + '/%s_rerank.csv' % f
        # fn_label = data_directory + '/ukbench_list_images_labels.txt'
        graph_folder = DATASET + '/Graph'

        search_region = 6
        kNN = 5
        retri_amount = 15

        # Load data (retrieval results for all images)
        lables, features, music_amount = load_data(rank_file)

        find_reciprocal_neighbors(lables, features, music_amount,
                                rerank_file, graph_folder,
                                search_region, kNN, retri_amount, f)

        # Evaluate the accuracy
        print "Before:"
        predict = knnBeforeRerank(f, kNN)
        # predict = knnBeforeRerank(f, 1)
        print evaluate(predict)
        print "After:"
        predict = knnAfterRerank(f, kNN)
        print evaluate(predict)