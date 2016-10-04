# coding = utf8

GTZAN = 'data/GTZAN'

import os
import librosa as rosa
from pydub import AudioSegment

for folder in os.listdir(GTZAN):
    if len(folder.split('_')) > 1: continue
    count = 0
    wav_dir = GTZAN + '/%s_wav' % folder
    if not os.path.exists(wav_dir): os.mkdir(wav_dir)
    for song in os.listdir(GTZAN + '/%s' % folder):
        count += 1
        print "%s\t%d" % (folder, count)
        song_path = GTZAN + '/%s/%s' % (folder, song)
        song_name = song.split('.')
        song_name = "%s%s.mp3"  % (song_name[0], song_name[1])
        song = AudioSegment.from_file(song_path)
        song.export(wav_dir + '/%s' % song_name, format = 'mp3')


