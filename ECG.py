import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy import signal


class ECG:

    def __init__(self, name, data, sample):
        self.name = name
        self.data = data
        self.sample = sample

    def add_data(self, data_ecg):
        self.data.append(data_ecg)

    def write_data(self, data):
        self.data = [data]

    def write_name(self, name):
        self.name = name

    def write_sample(self, sample):
        self.sample = sample

    def plot(self):
        N = int(len(self.data))  # nombre d'element dans la liste
        T = (1 / self.sample)  # periode d'échantillonage du signal
        x = np.linspace(0.0, N * T, N)
        plt.ylabel('mV')
        plt.xlabel('Time [ms]')
        plt.grid()
        plt.plot(x, self.data,color='r',)
        plt.show()

    def apply_filter(self, fl, fh, order):

        T = (1 / self.sample)
        w1 = fl / (1 / (T * 2))  # Normalize the frequency
        w2 = fh / (1 / (T * 2))
        b, a = signal.butter(order, [w1, w2], 'band')
        self.data = signal.filtfilt(b, a, self.data)

    def apply_fft(self):
        self.data = fft(self.data)

    def plot_fft(self):
        N = int(len(self.data))  # nombre d'element dans la liste
        T = (1 / self.sample)  # periode d'échantillonage du signal
        xf = np.linspace(0, 1 / (2 * T), N / 2)
        plt.plot((xf[1:]), 2.0 / N * np.abs(self.data[int(0):int(N / 2)][1:]))
        plt.ylabel('Amplitude')
        plt.xlabel('Frequency')
        plt.grid()
        plt.show()

    def plot_data_and_fft(self):
        plt.subplot(2, 1, 1)
        N = int(len(self.data))  # nombre d'element dans la liste
        T = (1 / self.sample)  # periode d'échantillonage du signal
        x = np.linspace(0.0, N * T, N)
        plt.ylabel('mV')
        plt.xlabel('Time [ms]')
        plt.grid()
        plt.plot(x, self.data, color='r', )
        plt.subplot(2, 1, 2)
        self.apply_fft()
        self.plot_fft()


    def get_frequency_value(self):
        N = int(len(self.data))  # nombre d'element dans la liste
        T = (1 / self.sample)  # periode d'échantillonage du signal
        freq = []
        xf = np.linspace(0, 1 / (2 * T), N / 2)
        threshold = 0.2 * max(abs(self.data))
        mask = abs(self.data) > threshold
        i=0
        for i in range(int(len(mask)/2)) :
            if mask[i]:
                freq.append(xf[i])
        return freq











