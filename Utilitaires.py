import os
import csv
import random
from ECG import ECG
from CPR import CPR
import numpy as np
# Just disables the warning, doesn't enable AVX/FMA
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
##################################################
#      Utilitaires pour étude de la base 2       #
##################################################

## car ca me gave d'appuyer sur mes touches
def select_animal():
   # return int(input("\nChoisir le numéro d'animal : (1 à 17 sauf 2)\n"))
    return 1

def select_ecg():
  #  return int(input("\nChoisir le numéro d'ECG : \n"))
    return 1


def load_animal_datas(): #Recuperation des ECG d'un animal

    listECG = []
    nbEchAvShock = 600
    #numAnimal = select_animal()

    # Variables utiles pour récupération correct des données (résultant de leur acquisition)
    gain = 41
    offset = 128
    sample_rate = 170.667

    # Récupération automatique des chemins des fichiers à ouvrir
    file_to_open = []
    indexData = 1
    lastDirectoy = os.getcwd()
    for num in range(0,7):
        indexData =1
        numAnimal = 1
        if num == 0 :
            numAnimal = 1
        elif num == 1 :
            numAnimal = 3
        elif num == 2 :
            numAnimal = 6
        elif num == 3 :
            numAnimal = 7
        elif num == 4 :
            numAnimal = 10
        elif num == 5 :
            numAnimal = 12
        elif num == 6 :
            numAnimal = 14

        os.chdir(lastDirectoy)
        os.chdir(os.getcwd() + "\\DataSources\\Base2\\Animal_" + str(numAnimal) + "\\")
        print(os.getcwd())
        while os.path.isfile("A" + str(numAnimal) + "_Data" + str(indexData) + ".csv"):
            file_to_open.append(os.getcwd() + "\\A" + str(numAnimal) + "_Data" + str(indexData) + ".csv")
     #       print(indexData)
            indexData += 1


        os.chdir(lastDirectoy)
    #  print ("indexdata %d",indexData)
    # Récupération des données

        for i in range(indexData-1):

            data = []
            file = open(file_to_open[i], "r")
            cr = csv.reader(file, delimiter=',')

            for row in cr:
                data.append(float((int(row[0]) - offset) * gain))


            ecg = ECG("Animal_" + str(numAnimal) + "_ECG_" + str(i), data, sample_rate)
            rescueindex = i
            if (rescueindex == 0) :
                rescueindex +=1
            ecg.find_rescue(numAnimal , rescueindex)
            ecg.find_shock()
            ecg.delete_before_shock(nbEchAvShock)
            ecg.apply_filter(5,10,3)
            ecg.get_EMA(10)


            listECG.append(ecg)


        # Retour au chemin de travail original
    os.chdir(lastDirectoy)

    return listECG


def afficher_un_ECG(listeECG : list):

    numEcg = select_ecg()
   # listeECG[numEcg - 1].apply_filter(0.5,15,3)
    listeECG[(numEcg-1)].plot()
    #listeECG[(numEcg - 1)].plot_shock()

def afficher_all_ECG(listeECG : list):

    for i in range(len(listeECG)):
        listeECG[i].plot_data_and_EMA(10)


#def create_train(listeECG: list):
#    x_train = []
#    y_train = []
#
#    for i in range(round(len(listeECG) / 3), round(len(listeECG) *2 / 3)):
#        trainx = {}
#        trainx["SMA"] = listeECG[i].SMA
#        trainx["EMA"] = listeECG[i].EMA
#        trainx["FFT"] = listeECG[i].get_frequency_value()
#        x_train.append(trainx)
#
#        y_train.append(listeECG[i].rescue)
#    return x_train, y_train

def create_test_semi_random(listeECG:list):
    listeECG_Success = []
    listeECG_Failed = []
    x_test = []
    y_test = []
    cptZero = 0

    for i in range(len(listeECG)):
        if listeECG[i].rescue == 1:
            listeECG_Success.append(listeECG[i])
        elif listeECG[i].rescue == 0:
            listeECG_Failed.append(listeECG[i])

    for i in range(round(len(listeECG) / 3)):
        toogle = random.getrandbits(1)
        if (toogle and cptZero < 2) or (cptZero >= 2) :
            j = random.randrange(0, len(listeECG_Success))
            testx = {}
            testx["SMA"] = listeECG_Success[j].SMA
            testx["EMA"] = listeECG_Success[j].EMA
            testx["FFT"] = listeECG_Success[j].get_frequency_value()
            x_test.append(testx)
            y_test.append(listeECG_Success[j].rescue)
        else:
            cptZero += 1
            j = random.randrange(len(listeECG_Failed) - 2, len(listeECG_Failed))
            testx = {}
            testx["SMA"] = listeECG_Failed[j].SMA
            testx["EMA"] = listeECG_Failed[j].EMA
            testx["FFT"] = listeECG_Failed[j].get_frequency_value()
            x_test.append(testx)
            y_test.append(listeECG_Failed[j].rescue)

    return x_test, y_test

def create_train_homogene(listeECG : list):
    listeECG_Success = []
    listeECG_Failed = []
    x_train = []
    y_train = []

    for i in range(len(listeECG)):
        if listeECG[i].rescue == 1:
            listeECG_Success.append(listeECG[i])
        elif listeECG[i].rescue == 0:
            listeECG_Failed.append(listeECG[i])

    for i in range(round(len(listeECG)*2/3)):
        toogle = random.getrandbits(1)
        if toogle:
            j = random.randrange(0,len(listeECG_Success))
            trainx = {}
            trainx["SMA"] = listeECG_Success[j].SMA
            trainx["EMA"] = listeECG_Success[j].EMA
            trainx["FFT"] = listeECG_Success[j].get_frequency_value()
            x_train.append(trainx)
            y_train.append(listeECG_Success[j].rescue)
        else:
            j = random.randrange(0, len(listeECG_Failed)-2)
            trainx = {}
            trainx["SMA"] = listeECG_Failed[j].SMA
            trainx["EMA"] = listeECG_Failed[j].EMA
            trainx["FFT"] = listeECG_Failed[j].get_frequency_value()
            x_train.append(trainx)
            y_train.append(listeECG_Failed[j].rescue)

    return x_train, y_train

def create_train_homogene_2(listeECG : list):
    listeECG_Success = []
    listeECG_Failed = []
    x_train = []
    y_train = []
    cptZero = 0

    for i in range(len(listeECG)):
        if listeECG[i].rescue == 1:
            listeECG_Success.append(listeECG[i])
        elif listeECG[i].rescue == 0:
            listeECG_Failed.append(listeECG[i])

    for i in range(round(len(listeECG)*2/3)):
        toogle = random.getrandbits(1)
        if (toogle and cptZero < len(listeECG_Failed)-2) or (cptZero >= len(listeECG_Failed)-2) :
            j = random.randrange(0,len(listeECG_Success))
            trainx = {}
            trainx["SMA"] = listeECG_Success[j].SMA
            trainx["EMA"] = listeECG_Success[j].EMA
            trainx["FFT"] = listeECG_Success[j].get_frequency_value()
            x_train.append(trainx)
            y_train.append(listeECG_Success[j].rescue)
        else:
            trainx = {}
            trainx["SMA"] = listeECG_Failed[cptZero].SMA
            trainx["EMA"] = listeECG_Failed[cptZero].EMA
            trainx["FFT"] = listeECG_Failed[cptZero].get_frequency_value()
            x_train.append(trainx)
            y_train.append(listeECG_Failed[cptZero].rescue)
            cptZero += 1

    return x_train, y_train

#def create_test(listeECG:list):
#
#    x_test =[]
#    y_test = []
#
#    for i in range(round(len(listeECG) *2 / 3), round(len(listeECG) *3 / 3),1):
#        testx = {}
#        testx["SMA"] = listeECG[i].SMA
#        testx["EMA"] = listeECG[i].EMA
#        testx["FFT"] = listeECG[i].get_frequency_value()
#        x_test.append(testx)
#        y_test.append(listeECG[i].rescue)
#    return x_test,y_test

def create_test_true(listeECG:list):
    x_test = []
    y_test = []

    for i in range(round(len(listeECG) *2 / 3), round(len(listeECG) *3 / 3),1):
        if listeECG[i].rescue == 1:
            testx = {}
            testx["SMA"] = listeECG[i].SMA
            testx["EMA"] = listeECG[i].EMA
            testx["FFT"] = listeECG[i].get_frequency_value()
            x_test.append(testx)
            y_test.append(listeECG[i].rescue)

    return x_test,y_test

def create_test_false(listeECG: list):
    x_test = []
    y_test = []

    for i in range(round(len(listeECG) *2 / 3), round(len(listeECG) *3 / 3), 1):
        if listeECG[i].rescue == 0:
            testx = {}
            testx["SMA"] = listeECG[i].SMA
            testx["EMA"] = listeECG[i].EMA
            testx["FFT"] = listeECG[i].get_frequency_value()
            x_test.append(testx)
            y_test.append(listeECG[i].rescue)

    return x_test, y_test

#def create_test_homogene(listeECG : list):
#    listeECG_Success = []
#    listeECG_Failed = []
#    x_test = []
#    y_test = []
#
#    for i in range(len(listeECG)):
#        if listeECG[i].rescue == 1:
#            listeECG_Success.append(listeECG[i])
#        elif listeECG[i].rescue == 0:
#            listeECG_Failed.append(listeECG[i])
#            testx = {}
#            testx["SMA"] = listeECG[i].SMA
#            testx["EMA"] = listeECG[i].EMA
#            testx["FFT"] = listeECG[i].get_frequency_value()
#            x_test.append(testx)
#            y_test.append(listeECG[i].rescue)
#
#    for i in range((round(len(listeECG)*2 / 3) - len(listeECG_Failed))):
#        j = random.randrange(0,len(listeECG_Success))
#        testx = {}
#        testx["SMA"] = listeECG_Success[j].SMA
#        testx["EMA"] = listeECG_Success[j].EMA
#        testx["FFT"] = listeECG_Success[j].get_frequency_value()
#        x_test.append(testx)
#        y_test.append(listeECG_Success[j].rescue)
#
#    return x_test, y_test

def get_epoch(x,output):
    epoch_x = [[0 for i in range(121)] for j in range(len(x[:]))] ###" attention hardcode faut le bouger un jour
    epoch_y = [[0 for i in range(1)] for j in range(len(x[:]))]

    for y in range (len(x)):
        sma = x[y]['SMA']
        ema = x[y]['EMA']
        fft = x[y]['FFT']

        for i in range (len (sma)*2):
            if i < len(sma)-1:
                epoch_x[y][i] = sma[i]
            else :
                epoch_x[y][i] = ema[i-len(sma)]

        epoch_x[y][i+1] = fft
        epoch_y[y][0] = output[y]

    return epoch_x,epoch_y

def get_shape(listeEcg: list):
    shape = listeEcg[0].get_size()
    return shape

def get_size_batch(listeEcg : list):
    size = round(len(listeEcg) / 3)
    return size

##################################################
# A garder mais pas util pour étude de la base 2 #
##################################################

def select_mode():
    return int(input("Choisir un mode : \n   Mode 1 : Base 1\n   Mode 2 : Base 2 - Animaux\n   Mode 3 : Base 3 - Matlab\n\nSaisie : "))

def load_base1_data():  #Chargement des données base 1
    sample_rate = 170.667
    numEcg = int(input("\nChoisir le numéro d'animal : (1 à 17 sauf 2)\n"))
    lastDirectoy = os.getcwd()
    os.chdir(os.getcwd() + "\\DataSources\\Base1\\")
    file_to_open = os.getcwd() + "\\Case" + str(numEcg) + ".csv"

    # Récupération des données
    file = open(file_to_open, "r")
    cr = csv.reader(file, delimiter='\n')
    data = []
    for row in cr:
        data.append(float(row[0]))

    # Retour au chemin de travail original
    os.chdir(lastDirectoy)
    return ECG("Case" + str(numEcg), data, sample_rate)

def load_animal_data(): #Chargement des données Base 2

    # Variables utiles pour récupération correct des données (résultant de leur acquisition)
    sample_rate = 170.667
    #gain = 1 / 41
    gain = 41
    offset = 128

    # Selection des données à récupérer
    numAnimal = int(input("\nChoisir le numéro d'animal : (1, 3, 6, 7, 10, 12, 14)\n"))
    numECG = int(input("\nChoisir le numéro d'ECG : "))

    # Récupération automatique des chemins des fichiers à ouvrir
    file_to_open = []
    indexData = 1
    lastDirectoy = os.getcwd()
    os.chdir(os.getcwd() + "\\DataSources\\Base2\\Animal_" + str(numAnimal) + "\\")
    while os.path.isfile("A" + str(numAnimal) + "_Data" + str(indexData) + ".csv"):
        file_to_open.append(os.getcwd() + "\\A" + str(numAnimal) + "_Data" + str(indexData) + ".csv")
        indexData += 1

    # Récupération des données
    data = []
    #for i in range(len(file_to_open)):
    file = open(file_to_open[numECG], "r")
    cr = csv.reader(file, delimiter=',')
    for row in cr:
        data.append(float((int(row[0]) - offset) * gain))

    # Retour au chemin de travail original
    os.chdir(lastDirectoy)

    return ECG("Animal_" + str(numAnimal) + "_ECG_" + str(numECG), data, sample_rate)

def load_m_data(): #Chargement des données Base 3

    # Variables utiles pour récupération correct des données (résultant de leur acquisition)
    sample_rate = 250

    # Selection des données à récupérer
    numEcg = int(input("\nChoisir le numéro d'ECG : (1 à 11)\n"))

    # Récupération automatique des chemins des fichiers à ouvrir
    lastDirectoy = os.getcwd()
    os.chdir(os.getcwd() + "\\DataSources\\Base3\\")
    file_to_open = os.getcwd() + "\\ecg_" + str(numEcg) + ".csv"

    # Récupération des données
    file = open(file_to_open, "r")
    cr = csv.reader(file, delimiter='\n')
    data = []
    for row in cr:
        data.append(float(row[0]))

    # Retour au chemin de travail original
    os.chdir(lastDirectoy)

    return ECG("Data" + str(numEcg), data, sample_rate)

def load_cpr_data():  # on charge le fichier en entier de cpr on verrra ce qu'on en fait en traitement de donnée mais ca ca l'ouvvre

    file_to_open = os.getcwd() + "\\DataSources\\Base1\\CPR.csv"

    thrust_data = []
    start_data = []
    stop_data = []
    cpr_list = []
    first = True;
    switch = 0
    file = open(file_to_open, "r")
    cr = csv.reader(file, delimiter=',')
    for row in cr:
        for i in range(len(row)):
            if (check_str(row[i]) == True):
                if switch == 1:
                    thrust_data.append(int(row[i]))
                elif switch == 2:
                    start_data.append(int(row[i]))
                elif switch == 3:
                    stop_data.append(int(row[i]))
            else:
                if (row[i] == "Thrust (kgs)"):
                    switch = 1
                    if first:
                        first = False
                    else:
                        name = "cpr" + str(i)
                        cpr_list.append(CPR(name, thrust_data[:], start_data[:], stop_data[:]))
                        thrust_data[:] = []
                        start_data[:] = []
                        stop_data[:] = []
                elif (row[i] == "Start Time"):
                    switch = 2
                elif (row[i] == "End Time"):
                    switch = 3
    return cpr_list

def check_str(s):
    try:
        int(s)
        return True
    except ValueError:
        return False