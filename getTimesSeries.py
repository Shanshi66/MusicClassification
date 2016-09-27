import librosa as rosa
import os
import csv
import math
import random
import shutil
from matplotlib import pyplot as plt

EMOTION_SONGS = 'data/EmotionSongs'
EMOTION_SONGS_ANGRY = EMOTION_SONGS + '/Angry_all'
EMOTION_SONGS_HAPPY = EMOTION_SONGS + '/Happy_all'
EMOTION_SONGS_RELAX = EMOTION_SONGS + '/Relax_all'
EMOTION_SONGS_SAD   = EMOTION_SONGS + '/Sad_all'

LENGTH = 100

category = ['Angry', 'Happy', 'Relax', 'Sad']

def song2CSV(dir, category):
    cnt = 0
    mp3_dir = os.path.join(dir, '%s_all' % category)
    csv_dir = os.path.join(dir, '%s_CSV' % category)
    for song in os.listdir(mp3_dir):
        wf = open(os.path.join(csv_dir, "%s.csv" % song), 'w')
        cnt += 1
        print '%5d\t%10s\t%s' % (cnt, category, song)
        y, sr = rosa.load('%s/%s_all/%s' % (dir, category, song), sr = 22500)
        # length = len(y)
        # seg_num = length / LENGTH
        # for i in range(0, seg_num):
        #     tmp = [x * x for x in y[i * LENGTH : (i + 1) * LENGTH]]
        #     tmp = math.sqrt(sum(tmp)/ len(tmp))
        #     wf.write('%f\n' % tmp)
        for item in y:
            wf.write('%f\n' % item)
        wf.close() 

def split():
    for c in category:
        source_dir = EMOTION_SONGS + '/%s_CSV' % c
        train_dir = EMOTION_SONGS + '/Train/%s' % c
        test_dir = EMOTION_SONGS + '/Test/%s' % c

        if not os.path.exists(train_dir): os.mkdir(train_dir)
        if not os.path.exists(test_dir): os.mkdir(test_dir)

        song_list = os.listdir(EMOTION_SONGS + '/%s_CSV' % c)
        random.shuffle(song_list)
        bandary =  int(len(song_list) / 3)
        bandary = 10
        for song in song_list[0 : bandary]:
            shutil.copy(source_dir + '/%s' % song, '%s/%s' % (train_dir, song))
        for song in song_list[bandary : ]:
            shutil.copy(source_dir + '/%s' % song, '%s/%s' % (test_dir, song))

if __name__ == '__main__': 
    for c in category:
        song2CSV(EMOTION_SONGS, c)
    split()


