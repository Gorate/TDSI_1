from ECG import ECG
import csv
import matplotlib.pyplot as plt

import numpy as np
from scipy.fftpack import fft
from scipy import signal

#declaration global

sample_rate = 170.667
gain = 1/41
fl = 1  # Cut-off frequency of the filter
fh = 1.2   # frequence cardiaque d'un cochon 70 bpm

file = open("C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015100136_wfdb_chan_0.csv", "r")
cr = csv.reader(file,delimiter = ',')
data_tmp = []
for row in cr :
        data_tmp.append(float((int(row[0])-128)*gain))                  # on charge les donnée et on convertit les valeur en mv depuis le file info :  41 bits/mV Offset : 128

ecg = ECG("data1", data_tmp, sample_rate)                                     # on cree notre objet

ecg.apply_filter(fl,fh,4)   #on cree un filtre passe bande d'ordre 4
ecg.plot_data_and_fft()
freq = ecg.get_frequency_value()

print(freq)





