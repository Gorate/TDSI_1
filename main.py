from ECG import ECG
import csv
import matplotlib.pyplot as plt

import numpy as np
from scipy.fftpack import fft
from scipy import signal

#declaration global


def animal_create(file_to_open, name, sample):

        data = []
        for i in range(len(file_to_open)):
                file = open(file_to_open[i], "r")
                cr = csv.reader(file, delimiter=',')
                for row in cr:
                        data.append(float((int(row[0]) - 128) * gain))

        return ECG(name, data, sample)


#c'est hardcode c'est moche mais c'est commme ca pour le moment
file_to_open = ["C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015110106_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015110431_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015110757_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015111142_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015111541_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015111929_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015112300_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015100136_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015101340_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015101715_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015102101_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015102908_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015103315_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015103652_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015104106_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015104452_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015105028_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015105415_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\Animal 01 - ID 953\\PAD50911289121015105742_wfdb_chan_0.csv"]






sample_rate = 170.667
gain = 1/41
fl = 1  # Cut-off frequency of the filter
fh = 1.2   # frequence cardiaque d'un cochon 70 bpm

#file = open(file_to_open[8], "r")

# print(file_to_open[8])
# cr = csv.reader(file,delimiter = ',')
# data_tmp = []
# for row in cr :
#         data_tmp.append(float((int(row[0])-128)*gain))                  # on charge les donnée et on convertit les valeur en mv depuis le file info :  41 bits/mV Offset : 128
#ecg = ECG("data1", data_tmp, sample_rate)                                     # on cree notre objet



ecg = animal_create(file_to_open,"annimal_1",sample_rate)
ecg.apply_filter(fl,fh,5)   #on cree un filtre passe bande d'ordre 4
ecg.plot_data_and_fft()
freq = ecg.get_frequency_value()
d
print(freq)





