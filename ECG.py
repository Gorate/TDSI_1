import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy import signal
from CPR import CPR
import os
import csv
class ECG:

    def __init__(self, name: str, data, sample):
        self.name = name
        self.data = data
        self.sample = sample
        self.rescue = 1
        self.shock = 0
        self.SMA = []
        self.EMA = [0]

    def set_rescue(self,rescue):
        self.rescue = rescue

    def find_shock(self):
        for i in range (len(self.data)):
            if (abs(self.data[i]) > abs(0.5*max(self.data))):
                self.shock = i-1
                return

    def find_rescue(self,numAnimal : int,num_ecg : int):
        file_to_open = []
        data=[]
        os.chdir(os.getcwd())
        file_name = "Rescue"+(str(numAnimal)+".txt")
        file = open(file_name,"r")
        read = file.read()
        self.rescue = read[(num_ecg-1)*2]
        if self.rescue == 'R':
            self.rescue = 0
        if self.rescue == '1':
            self.rescue = 1

        return True

    def delete_after_shock(self):
        data = []
        # for i in range (self.shock+5):
        for i in range(self.shock):
            data.append(self.data[i])
        self.data = data
        return

    def delete_before_shock(self, nbEchToSaveBeforeShock: int):
        data = []
        for i in range(self.shock):
            if i >= self.shock - nbEchToSaveBeforeShock:
                data.append(self.data[i])
            # else:
            #   data.append(0)
        self.data = data
        return

    def plot_shock(self):
        N = int(len(self.data))  # nombre d'element dans la liste
        T = (1/self.sample)  # periode d'échantillonage du signal
        x = np.linspace(0.0, N * T, N)
        plt.ylabel('mV')
        plt.xlabel('Time [s]')
        plt.grid()
        plt.plot(x, self.data,color='r')
        plt.bar(x[self.shock], 1.25 * max(self.data), width=0.1, color='b')
        plt.show()

    def add_data(self, data_ecg):
        self.data.append(data_ecg)

    def write_data(self, data : list):
        self.data = data

    def write_name(self, name):
        self.name = name

    def write_sample(self, sample):
        self.sample = sample

    def plot(self):
        N = int(len(self.data))  # nombre d'element dans la liste
        T = (1/self.sample)  # periode d'échantillonage du signal
        x = np.linspace(0.0, N * T, N)
        plt.ylabel('mV')
        plt.xlabel('Time [s]')
        plt.grid()
        plt.plot(x, self.data,color='r',)
        plt.show()

    def apply_filter(self, fl, fh, order):

        T = ( 1/self.sample)
        w1 = fl / (1 / (T * 2))  # Normalize the frequency
        w2 = fh / (1 / (T * 2))
        b, a = signal.butter(order, [w1], 'highpass')
        self.data = signal.filtfilt(b, a, self.data)

    def apply_fft(self):
        self.data = fft(self.data)

    def plot_fft(self):
        N = int(len(self.data))  # nombre d'element dans la liste
        T = (1/self.sample)  # periode d'échantillonage du signal
        xf = np.linspace(0, 1 / (2 * T), N / 2)
        plt.plot((xf[1:]), 2.0 / N * np.abs(self.data[int(0):int(N / 2)][1:]))
        plt.ylabel('Amplitude')
        plt.xlabel('Frequency')
        plt.grid()
        plt.show()

    def plot_data_and_fft(self):
        plt.subplot(2, 1, 1)
        N = int(len(self.data))  # nombre d'element dans la liste
        T = (1/self.sample)  # periode d'échantillonage du signal
        x = np.linspace(0.0, N * T, N)
        plt.ylabel('mV')
        plt.xlabel('Time [s]')
        plt.grid()
        plt.plot(x, self.data, color='r', )
        plt.subplot(2, 1, 2)
        self.apply_fft()
        self.plot_fft()

    def get_frequency_value(self):
        N = int(len(self.data))  # nombre d'element dans la liste
        T = ( 1/self.sample)  # periode d'échantillonage du signal
        freq = []
        xf = np.linspace(0, 1 / (2 * T), N / 2)
        threshold = 0.5 * max((self.data))
        for i in range(int(len(self.data)/2)):
            if (self.data[i]>threshold):
                freq.append(xf[i])
        freq_max= max(freq)
        return freq_max

    def plot_data_and_cpr(self, cpr : CPR ):
        N = int(len(self.data))  # nombre d'element dans la liste
        T = (1/self.sample)  # periode d'échantillonage du signalç
        data_plot = []

        x = np.linspace(0.0, N * T, N)
        plt.ylabel('mV')
        plt.xlabel('Time [s]')
        plt.grid()
        plt.plot(x, self.data,color='b',)
        print(cpr.start_time)
        print(cpr.stop_time)
        plt.bar(cpr.start_time,1.25*max(self.data),width=5,color='r')
        plt.bar(cpr.stop_time, 1.25*max(self.data),width=5, color='g')
        plt.show()

    def filtre_peigne(self, x : int, K : int):
        if len(self.data) > K:
            for i in range(K, len(self.data)):
                self.data[i] = self.data[i] + self.data[i-K] * x
        return

    def remove_dc(self):
        average = sum(self.data) / len(self.data)
        print(average)
        for i in range(len(self.data)):
            self.data[i] = self.data[i] - average

    def get_sma(self, period : int ):
        for i in range(0,len(self.data),period):
            sum = 0
            for y in range (i,i+period,1):
                sum = sum + abs(self.data[y])
            self.SMA.append(sum/period)
        return self.SMA

    def get_EMA(self , period : int):
        error = self.get_sma(period)
        multiplier = (2 / (period + 1))
        for i in range(len(self.SMA)):
            if i == 0 :
                self.EMA[0] = (abs(self.data[i*period])-self.SMA[0])*multiplier + self.SMA[0]
            else :
                self.EMA.append( abs(self.data[i*period]) - self.EMA[i-1] *multiplier + self.SMA[i-1] )
        return self.EMA

    def get_size(self):
        shape = [len(self.SMA), len(self.EMA), 1]
        return shape

    def plot_data_and_EMA(self,period : int):
        EMA = self.get_EMA(period)

        N = int(len(self.data))  # nombre d'element dans la liste
        T = (1/self.sample)  # periode d'échantillonage du signalç
        x = np.linspace(0.0, N * T, N)
        plt.ylabel('mV')
        plt.xlabel('Time [s]')
        plt.grid()
        plt.plot(x, self.data,color='b')
        x = np.linspace(0.0, N*T, len(EMA))
        plt.plot(x, EMA, color='r')
        plt.plot(x,self.get_sma(period),color='g')
        plt.show()












