import os
import csv
from ECG import ECG

class Individu:

    def __init__(self):
        self.numIndividu = self.selectIndividu()
        self.ecgs_individu = self.load_ecgs_individu(self.numIndividu)
        self.results_shocks = self.load_result_expe(self.numIndividu)


    def selectIndividu(self):
        return int(input("\nChoisir le numéro d'individu : (1 à 17 sauf 2)\n"))


    def select_ecg(self):
        return int(input("\nChoisir le numéro d'ECG (1 à " + str(len(self.ecgs_individu)) + ") : \n"))


    def select_plot_mode(self):
        return int(input("\nChoisir le type de tracé : \n     1 - ECG Simple\n     2 - ECG + fft ECG\n=> "))


    def load_ecgs_individu(self, numIndividu:int):

        listECG = []

        # Variables de mise à l'échelle des données (résultant de leur acquisition)
        gain = 41
        offset = 128
        sample_rate = 170.667

        # Récupération automatique des chemins des fichiers à ouvrir
        file_to_open = []
        indexData = 1
        lastDirectoy = os.getcwd()
        os.chdir(os.getcwd() + "\\DataSources\\Base2\\Animal_" + str(numIndividu) + "\\")
        while os.path.isfile("A" + str(numIndividu) + "_Data" + str(indexData) + ".csv"):
            file_to_open.append(os.getcwd() + "\\A" + str(numIndividu) + "_Data" + str(indexData) + ".csv")
            indexData += 1

        # Récupération des données
        for i in range(len(file_to_open)):

            data = []
            file = open(file_to_open[i], "r")
            cr = csv.reader(file, delimiter=',')

            for row in cr:
                data.append(float((int(row[0]) - offset) * gain))
                ecg = ECG("Individu_" + str(numIndividu) + "_ECG_" + str(i), data, sample_rate)

            listECG.append(ecg)

        # Retour au chemin de travail original
        os.chdir(lastDirectoy)

        return listECG


    def load_result_expe(self,numIndividu:int):
        file_to_open = os.getcwd() + "\\DataSources\\Base2\\Animal_" + str(numIndividu) + "\\ShocksResults.csv"
        data = []
        file = open(file_to_open, "r")
        cr = csv.reader(file, delimiter=',')
        for row in cr:
            data.append(bool(int(row[0])))
        return data


    def plot_ecg(self, numEcg:int):
        mode = self.select_plot_mode()

        if mode == 1:
            self.ecgs_individu[(numEcg-1)].plot(str(self.numIndividu), str(numEcg), str(self.results_shocks[numEcg-1]))
        elif mode == 2:
            self.ecgs_individu[(numEcg-1)].plot_data_and_fft(str(self.numIndividu), str(numEcg), str(self.results_shocks[numEcg-1]))

