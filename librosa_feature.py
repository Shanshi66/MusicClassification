#coding = utf8

import librosa as rosa
import csv
import os

EMOTION_SONGS = 'data/EmotionSongs'
FEATURE_DIR = EMOTION_SONGS + '/Features'

category = ['Angry', 'Happy', 'Relax', 'Sad']


## mfcc
def mfcc():
    for c in category:
        mp3_dir = EMOTION_SONGS + '/%s_all' % c
        feature_file = FEATURE_DIR + '/%s.mfcc' % c
        wf = open(feature_file, 'w')
        writer = csv.writer(wf)
        for song in os.listdir(mp3_dir):
            print '%10s\t%10s' % (c, song)
            y, sr = rosa.load(mp3_dir + '/' + song)
            mfcc = rosa.feature.mfcc(y = y, sr = sr, n_mfcc = 1)
            mfcc = list(mfcc)
            mfcc = map(list, mfcc)
            f = sum(list(mfcc), [])
            writer.writerow([song] + f)
        wf.close()

## rmse
def rmse():
    for c in category:
        mp3_dir = EMOTION_SONGS + '/%s_all' % c
        feature_file = FEATURE_DIR + '/%s.rmse' % c
        wf = open(feature_file, 'w')
        writer = csv.writer(wf)
        for index, song in enumerate(os.listdir(mp3_dir)):
            print '%d\t%10s\t%10s' % (index, c, song)
            y, sr = rosa.load(mp3_dir + '/' + song)
            rmse = rosa.feature.rmse(y = y)
            writer.writerow([song] + list(rmse[0]))
        wf.close()

if __name__ == '__main__':
    mfcc()
    # rmse()

    