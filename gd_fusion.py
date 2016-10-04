import numpy
import cPickle
import re
import copy
import os
import csv

feature_types = ['mvd', 'rh', 'rp', 'ssd', 'trh', 'tssd']
# DATASET = 'data/EmotionSongs/Dataset'
DATASET = 'data/GTZAN/Dataset'
CLASS = 10
# SAMPLE_NUM = 2852
SAMPLE_NUM = 1000

class GraphFusion:

    ########### Method 1: PageRank algorithm centered at the query image.###########
    def Fusion_Graph_Laplacian(self, graph_list, num_ranks, retri_amount, ground_truth):

        # merge all graphs
        initial_graph = graph_list[0]
        for i in range(1, num_ranks):
            cur_graph = graph_list[i]
            cur_keys = cur_graph.keys()
            initial_keys = initial_graph.keys()
            for j in cur_keys:
                if j not in initial_keys:
                    initial_graph[j] = cur_graph[j]
                else:
                    nodes = cur_graph[j]
                    for k in nodes:
                        initial_graph[j].append(k)

        # build Laplacian matrix
        all_keys = initial_graph.keys()
        sorted_keys = list(numpy.sort(all_keys))
        if -1 in sorted_keys:
            sorted_keys.remove(-1) # one key is -1
        matrix_size = numpy.size(sorted_keys)
        Laplacian = numpy.zeros([matrix_size, matrix_size])
        for cur_key in sorted_keys:
            if cur_key == -1:
                continue
            cur_weights = initial_graph[cur_key]
            neighbors = []
            neighbor_weights = []
            for weight in cur_weights:
                neighbors.append(weight[0])
                neighbor_weights.append(weight[1])
            #neighbors = numpy.unique(neighbors)
            for each_neighbor, each_weight in zip(neighbors, neighbor_weights):
                if sorted_keys.index(cur_key) != sorted_keys.index(each_neighbor):
                    # M[i,j], i is current index, j is i's neighbor
                    Laplacian[sorted_keys.index(cur_key), sorted_keys.index(each_neighbor)] += each_weight #1

        # normalize Laplacian matrix
        for i in range(matrix_size):
            if sum(Laplacian[i,:]) != 0:
            	Laplacian[i,:] = Laplacian[i,:] / sum(Laplacian[i,:])
        rank_vector = numpy.matrix([1.0/matrix_size] * matrix_size)
        rank_vector = numpy.transpose(rank_vector)
        Laplacian = numpy.transpose(Laplacian)
        for i in range(10):
            rank_vector = Laplacian * rank_vector
        rank_set = {}
        idx = 0
        for value in rank_vector:
            rank_set[idx] = value
            idx += 1

        # Solve pagerank, graph Laplacian
        selected_images_tmp = []
        for idx in sorted(rank_set, key=rank_set.get, reverse=True):
            selected_images_tmp.append(sorted_keys[idx])

        selected_images = []
        selected_images.append(ground_truth)
        selected_images_tmp.remove(ground_truth)
        selected_images.extend(selected_images_tmp)

        # Post-process. Add extra results if there is no enough candidate. use voc since it is usually better
        if len(selected_images) < retri_amount:
            voc_candidate = graph_list[1]
            voc_candidate = voc_candidate[-1]
            for i in voc_candidate:
                selected_images.append(i)

        return selected_images[0:retri_amount]


    ########### Method 2: find the weighted maximum density subgraph ###########
    def Fusion_Density_Subgraph(self, graph_list, num_ranks, retri_amount):

        # merge all graphs
        initial_graph = copy.deepcopy(graph_list[0])
        for i in range(1, num_ranks):
            cur_graph = graph_list[i]
            cur_keys = cur_graph.keys()
            initial_keys = initial_graph.keys()
            for j in cur_keys:
                if j not in initial_keys:
                    initial_graph[j] = cur_graph[j]
                else:
                    nodes = cur_graph[j]
                    for k in nodes:
                        initial_graph[j].append(k)

        # compute the sum of weights for each vertex
        all_keys = initial_graph.keys()
        weight_sum = {}
        for cur_key in all_keys:
            if cur_key == -1: continue
            cur_weights = initial_graph[cur_key]
            for weight in cur_weights:
                if cur_key not in weight_sum.keys():
                    weight_sum[cur_key] = weight[1]
                else:
                    weight_sum[cur_key] += weight[1]

        # select vertices as per the sum of weights
        selected_images = []
        for vertex in sorted(weight_sum, key=weight_sum.get, reverse=True):
            selected_images.append(vertex)

        # Post-process. Add extra results if there is no enough candidate.
        if len(selected_images) < retri_amount:
            voc_candidate = graph_list[1] # 0: hsv or 1000d. 1: voc
            voc_candidate = voc_candidate[-1]
            for i in voc_candidate:
                if i not in selected_images:
                    selected_images.append(i)

        return selected_images[0:retri_amount]


#########################################################

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

def knnAfterGraphFusion(K):
    rerank_file = open(DATASET + '/fusion_result.csv', 'r')
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


if __name__ == "__main__":
    graph_folder = DATASET + '/Graph'

    graphfusion = GraphFusion()
    retri_amount = 25
    kNN = 5

    fusion_result = DATASET + '/fusion_result.csv'
    fusion_result = open(fusion_result, 'w')
    writer = csv.writer(fusion_result)

    for i in range(SAMPLE_NUM):
        graph_list = []
        for f in feature_types:
            graph_list.append(cPickle.load(open(graph_folder + '/%d.%s' % (i, f), 'rb')))
        
        selected_music = graphfusion.Fusion_Density_Subgraph(graph_list, len(feature_types), retri_amount)
        
        if i in selected_music: selected_music.remove(i)
        # Uncomment the next line to use PageRank-based method, but keep the above line as well. We need "selected_images[0]" to define the center of the graph
        #selected_images = graphfusion.Fusion_Graph_Laplacian(graph_list, num_ranks, retri_amount, selected_images[0])

        writer.writerow([i] + selected_music)

    fusion_result.close()

    loadLabel()
    print "After fusion:"
    predict = knnAfterGraphFusion(kNN)
    print evaluate(predict)