# DATASET = 'data/EmotionSongs/Dataset'
DATASET = 'data/GTZAN/Dataset'
feature_types = ['mvd', 'rh', 'rp', 'ssd', 'trh', 'tssd']

names_file = open(DATASET + '/mp3names.csv', 'r')
label_file = open(DATASET + '/labels.csv', 'w')

count = 0
for name in names_file: 
    name = name.split('####')
    name = [ item.strip() for item in name]
    print count
    label_file.write('%s\t####\t%d\t####\t%s\n' % (name[0], count, name[1]))
    count += 1