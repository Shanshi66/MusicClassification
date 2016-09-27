EMOTION_DATASET = 'data/EmotionSongs/Dataset'
feature_types = ['mvd', 'rh', 'rp', 'ssd', 'trh', 'tssd', 'mfcc']

names_file = open(EMOTION_DATASET + '/mp3names.csv', 'r')
label_file = open(EMOTION_DATASET + '/labels.csv', 'w')

count = 0
for name in names_file: 
    name = name.split('####')
    name = [ item.strip() for item in name]
    count += 1
    print count
    label_file.write('%s\t####\t%d\n' % (name[0], count))