#coding = utf8

DATASET = 'data/EmotionSongs/Dataset'

def removeImageName():
    with open(DATASET + '/corel-1k_rank_cnn.txt', 'r') as rf, \
    open(DATASET + '/corel-1k_rank_cnn_1.txt', 'w') as wf:
         for line in rf:
            line = line.split()[1:]
            wf.write('\t'.join(line))
            wf.write('\n')

removeImageName()