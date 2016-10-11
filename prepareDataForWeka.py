# #coding = utf8

EMOTION = 'data/EmotionSongs/Dataset'
# feature_types = ['mvd', 'rh', 'rp', 'ssd', 'trh', 'tssd']

# rf = open(EMOTION + '/labels.csv', 'r')

# names = []

# for line in rf:
#     line = line.split("####")
#     name, label, category = [item.strip() for item in line]
#     name = name.split()
#     name = '_'.join(name)
#     names.append(name)

# rf.close()

# for f in feature_types:
#     rf = open(EMOTION + '/%s_rank.csv' % f, 'r')
#     wf = open(EMOTION + '/Weka/%s.arff' % f, 'w')

#     wf.write("@relation '%s_rank'\n" % f)

#     for i in xrange(len(names)):
#         wf.write("@attribute %d {F, T}\n" % i)
#     wf.write('@data\n')
#     for line in rf:
#         line = line.split(',')
#         line = [int(item.strip()) for item in line]
#         line = sorted(line[0 : 50])
#         item = []
#         for each in line:
#             item.append('%s T' % each)
#         item = ', '.join(item)
#         wf.write('{%s}\n' % item)

#     wf.close()
#     rf.close()

rf = open(EMOTION + '/corel-1k.txt', 'r')
wf = open(EMOTION + '/Weka/corel.arff', 'w')

wf.write("@relation 'corel_rank'\n")

for i in xrange(1000):
    wf.write("@attribute %d {F, T}\n" % i)
wf.write('@data\n')
for line in rf:
    line = line.split()
    line = [int(item.strip()) for item in line[1 : 51]]
    line = sorted(line)
    item = []
    for each in line:
        item.append('%s T' % each)
    item = ', '.join(item)
    wf.write('{%s}\n' % item)

wf.close()
rf.close()

