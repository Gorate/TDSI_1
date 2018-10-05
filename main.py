from ECG import ECG
from CPR import CPR
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy import signal

#declaration global
# Choix du mode d'utilisation  2 on ouvre les matlabs 1 on ouvre les excels
mode =4

#c'est hardcode c'est moche mais c'est commme ca pour le moment
file_to_open = ["C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015103652_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015104106_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015104452_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015105028_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015105415_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015105742_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015110106_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015110431_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015110757_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015111142_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015111541_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015111929_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015112300_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015100136_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015101340_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015101715_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015102101_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015102908_wfdb_chan_0.csv",
"C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015103315_wfdb_chan_0.csv"]
file_to_open2 = "CPR.csv"
onefile = "C:\\Users\\gorat\\Documents\\Challenge_TDSI\\Code\\TDSI_1-master\\Animal 01 - ID 953\\PAD50911289121015103652_wfdb_chan_0.csv"
file_to_open_m = "ecg_1.csv"
file_to_open_oled = "Case01.txt"



def check_str(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def open_cpr_data(file_to_open):            # on charge le fichier en entier de cpr on verrra ce qu'on en fait en traitement de donnée mais ca ca l'ouvvre
        thrust_data = []
        start_data  = []
        stop_data = []
        cpr_list = []
        first = True;
        switch = 0
        file = open(file_to_open, "r")
        cr = csv.reader(file, delimiter=',')
        for row in cr:
                for i in range(len(row)):
                        if (check_str(row[i]) == True ):
                            if switch == 1 :
                                thrust_data.append(int(row[i]))
                            elif switch == 2 :
                                start_data.append(int(row[i]))
                            elif switch == 3 :
                                stop_data.append(int(row[i]))
                        else:
                            if (row[i] == "Thrust (kgs)" ):
                                switch = 1
                                if first:
                                    first = False
                                else:
                                    name = "cpr"+str(i)
                                    cpr_list.append(CPR(name, thrust_data[:], start_data[:], stop_data[:]))
                                    thrust_data[:] = []
                                    start_data[:]  = []
                                    stop_data[:]   = []
                            elif (row[i] == "Start Time"):
                                switch = 2
                            elif (row[i] == "End Time" ) :
                                switch = 3
        return cpr_list

def animal_create(file_to_open, name, sample):

        data = []
        for i in range(len(file_to_open)):
                file = open(file_to_open[i], "r")
                cr = csv.reader(file, delimiter=',')
                for row in cr:
                        data.append(float((int(row[0]) - 128) * gain))

        return ECG(name, data, sample)

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

    delay = 227
    ecg.filtre_peigne(1.1, delay)
    ecg.apply_filter(fl, fh, 3)  # on cree un filtre passe bande d'ordre 4

if mode == 3:
    sample_rate = 170.667
    gain = 1/41
    fl = 1  # Cut-off frequency of the filter
    fh = 1.2   # frequence cardiaque d'un cochon 70 bpm
    data = []
    file = open(onefile, "r")
    cr = csv.reader(file, delimiter=',')
    for row in cr:
            data.append(float((int(row[0]) - 128) * gain))
    ecg = ECG("ecg1", data, sample_rate)
    #ecg.apply_filter(fl, fh, 4)  # on cree un filtre passe bande d'ordre 4


if mode == 4:
    sample_rate = 170
    gain = 1/41
    fl = 1  # Cut-off frequency of the filter
    fh = 1.2   # frequence cardiaque d'un cochon 70 bpm
    file = open(file_to_open_oled, "r")
    cr = csv.reader(file ,delimiter = '\n')
    data_tmp = []
    for row in cr:
         data_tmp.append(float(row[0]))              # on charge les donnée et on convertit les valeur en mv depuis le file info :  41 bits/mV Offset : 128
    ecg = ECG("data1", data_tmp, sample_rate)                                     # on cree notre objet
    ecg.apply_filter(fl, fh, 2*1)  # on cree un filtre passe bande d'ordre 4



cpr = open_cpr_data(file_to_open2)

#cpr[0].get_time_rigth()


ecg.plot_data_and_fft()

#ecg.plot_data_and_cpr(cpr[0])
#freq = ecg.get_frequency_value()
#print(freq)





