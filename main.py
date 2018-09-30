from ECG import ECG
import csv
import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
from scipy.fftpack import fft
from scipy import signal

#declaration global
# Choix du mode d'utilisation  2 on ouvre les matlabs 1 on ouvre les excels
mode = 1


def check_str(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def open_cpr_data(file_to_open):            # on charge le fichier en entier de cpr on verrra ce qu'on en fait en traitement de donnée mais ca ca l'ouvvre
        data = [0]
        file = open(file_to_open, "r")
        cr = csv.reader(file, delimiter=',')
        for row in cr:
                for i in range(len(row)):
                        if (check_str(row[i]) == True ):
                                data.append(int(row[i]))
                        else :
                            if (data[0] !=0 ):
                                    data.append(row[i])
                            else :
                                data[0] = row[i]
        # debugger
        # for i in range(len(data)):
        #     print(data[i])


        print("hello")


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


file_to_open2 = "C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\CPR.csv"


file_to_open_m = "C:\\Users\\gorat\\Documents\\Ecole_ing\\TDSI\\Project1\\challenge\\data_matlab\\ecg_1.csv"


sample_rate = 170.667
gain = 1/41
fl = 1  # Cut-off frequency of the filter
fh = 1.2   # frequence cardiaque d'un cochon 70 bpm

if mode == 1:
    sample_rate = 170.667
    gain = 1/41
    fl = 1  # Cut-off frequency of the filter
    fh = 1.2   # frequence cardiaque d'un cochon 70 bpm
    ecg = animal_create(file_to_open, "annimal_1",sample_rate)
    ecg.apply_filter(fl, fh, 4)  # on cree un filtre passe bande d'ordre 4

if mode == 2:
    open_cpr_data(file_to_open2)
    sample_rate = 250
    gain = 1/41
    fl = 1  # Cut-off frequency of the filter
    fh = 1.2   # frequence cardiaque d'un cochon 70 bpm
    file = open(file_to_open_m, "r")
    cr = csv.reader(file,delimiter = '\n')
    data_tmp = []
    for row in cr:
         data_tmp.append(float(row[0]))              # on charge les donnée et on convertit les valeur en mv depuis le file info :  41 bits/mV Offset : 128
    ecg = ECG("data1", data_tmp, sample_rate)                                     # on cree notre objet
    ecg.apply_filter(fl, fh, 3)  # on cree un filtre passe bande d'ordre 4


ecg.plot_data_and_fft()
freq = ecg.get_frequency_value()
print(freq)





