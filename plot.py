# coding = utf8

from matplotlib import pyplot as plt

f = open('data/EmotionSongs/Angry_CSV/Amnesia.mp3.csv', 'r')
x = []
for line in f:
    x.append(float(line))

f.close()
plt.plot(x)
plt.show()