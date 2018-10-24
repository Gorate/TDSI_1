from IndividuIHM import Individu
from tkinter import *




def initIndividu():
    monIndividu.initIndividu(int(listeSelecteur.get()))
    ECGs.config(from_=1, to=monIndividu.getNbrEcgs())


def resetIndividu():
    monIndividu.resetindividu()
    listeSelecteur.set(listeIndividus[0])
    ECGs.config(from_=0, to=0)


def plot_ecg():
    monIndividu.plot_ecg(int(ECGs.get()), 1)


def plot_fft():
    monIndividu.plot_ecg(int(ECGs.get()), 2)


def plot_ecg_fft():
    monIndividu.plot_ecg(int(ECGs.get()), 3)





monIndividu = Individu()

# -------------------------------------------------------------------------------
# Gestion/Paramètrage de l'interface
# -------------------------------------------------------------------------------

UserPanel = Tk()
UserPanel.title("IHM ECG")

BtnQuit = Button(UserPanel, text="Exit", command=UserPanel.quit)
BtnQuit.pack(side=BOTTOM, pady=10)

# -------------------------------------------------------------------------------
# Gestion des individus
# -------------------------------------------------------------------------------

frmGestionIndividu = LabelFrame(UserPanel, text="Gestion des individus", borderwidth=2, relief=GROOVE, width=400, height=200)
frmGestionIndividu.pack(padx=10, pady=10)

labelSelectionIndividu = Label(frmGestionIndividu, text="Selection de l'individu")
labelSelectionIndividu.pack(side=LEFT, padx=10, pady=10)

listeIndividus = ["-", 1, 3, 6, 7, 10, 12, 14]
listeSelecteur = StringVar()
listeSelecteur.set(listeIndividus[0])
Individus = OptionMenu(frmGestionIndividu, listeSelecteur, *listeIndividus)
Individus.pack(side=LEFT, padx=10)

BtnChargeIndividu = Button(frmGestionIndividu, text="Charger", command=initIndividu)
BtnChargeIndividu.pack(side=LEFT, padx=10)

BtnResetIndividu = Button(frmGestionIndividu, text="Reset", command=resetIndividu)
BtnResetIndividu.pack(side=LEFT, padx=10)


# -------------------------------------------------------------------------------
# Gestion des tracés
# -------------------------------------------------------------------------------
frmGestionTraces = LabelFrame(UserPanel, text="Gestion des tracés", borderwidth=2, relief=GROOVE, width=400, height=200)
frmGestionTraces.pack(padx=10, pady=10)

labelSelectionECG = Label(frmGestionTraces, text="Selection de l'ECG")
labelSelectionECG.pack(side=LEFT, padx=10, pady=10)

ECGs = Spinbox(frmGestionTraces, from_=0, to=0)
ECGs.pack(side=LEFT, padx=10)

BtnTraceECG = Button(frmGestionTraces, text="Trace ECG", command=plot_ecg)
BtnTraceECG.pack(side=LEFT, padx=10)

BtnTraceFFT = Button(frmGestionTraces, text="Trace FFT", command=plot_fft)
BtnTraceFFT.pack(side=LEFT, padx=10)

BtnTraceECG_FFT = Button(frmGestionTraces, text="Trace ECG & FFT", command=plot_ecg_fft)
BtnTraceECG_FFT.pack(side=LEFT, padx=10)


UserPanel.mainloop()