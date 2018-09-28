import csv
import os
import matplotlib.pyplot as plt
file = open("C:\\Users\\gorat\\Documents\\GitHub\\TDSI_1\\Challenge_TDSI\\Documentation\\PAD50911289121015100136_wfdb_chan_0.csv", "r")
cr = csv.reader(file,delimiter = ',')
liste = []
i=0
for row in cr :
        print (row[0])
        i = i+1
        liste.append(row[0])

print(i)
plt.axis([0, 5000, 0, 255])
plt.plot(liste)

plt.show()