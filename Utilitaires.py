import os
import csv
from ECG import ECG
from CPR import CPR

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

    numAnimal = select_animal()

    # Variables utiles pour récupération correct des données (résultant de leur acquisition)
    gain = 41
    offset = 128
    sample_rate = 170.667

    # Récupération automatique des chemins des fichiers à ouvrir
    file_to_open = []
    indexData = 1
    lastDirectoy = os.getcwd()
    os.chdir(os.getcwd() + "\\DataSources\\Base2\\Animal_" + str(numAnimal) + "\\")
    while os.path.isfile("A" + str(numAnimal) + "_Data" + str(indexData) + ".csv"):
        file_to_open.append(os.getcwd() + "\\A" + str(numAnimal) + "_Data" + str(indexData) + ".csv")
        indexData += 1

    # Récupération des données
    for i in range(len(file_to_open)):

        data = []
        file = open(file_to_open[i], "r")
        cr = csv.reader(file, delimiter=',')

        for row in cr:
            data.append(float((int(row[0]) - offset) * gain))
            ecg = ECG("Animal_" + str(numAnimal) + "_ECG_" + str(i), data, sample_rate)

        listECG.append(ecg)

    # Retour au chemin de travail original
    os.chdir(lastDirectoy)

    return listECG


def afficher_un_ECG(listeECG : list):

    numEcg = select_ecg()
    listeECG[numEcg - 1].find_rescue(1,numEcg)
    listeECG[numEcg-1].find_shock()
    listeECG[numEcg - 1].delete_after_shock()
    listeECG[numEcg - 1].apply_filter(0.5,15,3)
    listeECG[(numEcg-1)].plot_data_and_fft()
    #listeECG[(numEcg - 1)].plot_shock()

def afficher_all_ECG(listeECG : list):

    for i in range(len(listeECG)):
        listeECG[i].plot_data_and_EMA(10)


def create_train(listeEcg: list):
    train = []
    for i in range (round(len(listeEcg) / 3)):
        train.append(listeEcg[i])
    return train

def create_test(listeEcg:list):
    test = []
    for i in range(round(len(listeEcg) / 3),round(len(listeEcg) *2 / 3)):
        test.append(listeEcg[i])
    return test
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