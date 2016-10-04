# coding = utf8

import csv

# FEATURE = 'data/EmotionSongs/Features'
# DATASET = 'data/EmotionSongs/Dataset'

FEATURE = 'data/GTZAN/Features'
DATASET = 'data/GTZAN/Dataset'

feature_types = ['mvd', 'rh', 'rp', 'ssd', 'trh', 'tssd', 'mfcc', 'rmse']

# EMOTION
# feature_types = ['mvd', 'rh', 'rp', 'ssd', 'trh', 'tssd', 'mfcc', 'rmse']
# feature_types = ['mfcc']
# categories = {'Angry' : 0, 'Happy' : 1, 'Relax' : 2, 'Sad' : 3}

# GTZAN
feature_types = ['mvd', 'rh', 'rp', 'ssd', 'trh', 'tssd']
categories = {'blues' : 0, 'classical' : 1, 'country' : 2, 'disco' : 3, 'hiphop' : 4, 'jazz' : 5,
              'metal' : 6, 'pop' : 7, 'reggae' : 8, 'rock' : 9}

mp3names = {}

for ft in feature_types:
    wf = open(DATASET + '/%s.csv' % ft, 'w')
    writer = csv.writer(wf)
    for c in categories:
        rf = open(FEATURE + '/%s.%s' % (c, ft), 'r')
        reader = csv.reader(rf)
        for line in reader:
            if not mp3names.has_key(line[0]): mp3names[line[0]] = categories[c]
            feature = [line[0]] + map(float, line[1:]) + [categories[c]]
            writer.writerow(feature)
            print "%10s\t%10s\t%s" % (ft, c, line[0])
        rf.close()
    wf.close()

wf = open(DATASET + '/mp3names.csv', 'w')

for name in mp3names:
    wf.write("%s\t####\t%d\n" % (name, mp3names[name]))

wf.close()    

    