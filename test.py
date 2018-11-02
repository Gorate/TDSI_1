import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy import signal




gain = 1/41
file = open("C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015100136_wfdb_chan_0.csv", "r")
cr = csv.reader(file,delimiter = ',')
liste = []
i=0
for row in cr :
        liste.append(float((int(row[0])-128)*gain))


#plt.axis([0, 5000, -20, 300])
#plt.plot(liste)

N = int(len(liste))  # nombre d'element dans la liste
T = (1/170.667)  # periode d'échantillonage du signal

x = np.linspace(0.0, N*T, N)
xf = np.linspace(0, 1/(2*T), N/2)


fl = 1  # Cut-off frequency of the filter
fh = 1.2
w1 = fl / (1 /(T*2)) # Normalize the frequency
w2= fh/ (1 /(T*2))
b, a = signal.butter(6, [w1, w2],'band')



output = signal.filtfilt(b, a, liste)

plt.subplot(2, 1, 1)
plt.plot(x,output)

plt.ylabel('mV')
plt.xlabel('Time [ms]')
plt.subplot(2, 1, 2)
ft = fft(output)
plt.plot((xf[1:]), 2.0/N * np.abs(ft[int(0):int(N/2)][1:]))
#plt.plot(x,output)
plt.grid()
plt.show()
