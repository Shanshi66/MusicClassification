#coding = utf8

EMOTION_DATASET = 'data/EmotionSongs/Dataset'
feature_types = ['mvd', 'rh', 'rp', 'ssd', 'trh', 'tssd']

rf = open(EMOTION_DATASET + '/labels.csv', 'r')
wf = open(EMOTION_DATASET + '/dashen_mp3names.txt', 'w')

label2name = {}

for line in rf:
    line = line.split("####")
    name, label, category = [item.strip() for item in line]
    name = name.split()
    name = '_'.join(name)
    label2name[label] = name
    wf.write('%s Emotion_%s\n' % (name, category))

rf.close()
wf.close()


for f in feature_types:
    rf = open(EMOTION_DATASET + '/%s_rank.csv' % f, 'r')
    wf = open(EMOTION_DATASET + '/dasheng_%s_rank.txt' % f, 'w')

    for line in rf:
        line = line.split(',')
        line = [item.strip() for item in line]
        line = [label2name[line[0]]] + line[0:51]
        wf.write('%s\n' % (' '.join(line)))

    wf.close()
    rf.close()