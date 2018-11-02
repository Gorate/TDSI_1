from Utilitaires import *

#mode = select_mode()
#if mode == 1:
#    ecg = load_base1_data()
#    ecg.plot()
#elif mode == 2:
#    ecg_animal = load_animal_data()
#    ecg_animal.plot()
#elif mode == 3:
#    ecg_m = load_m_data()
#    ecg_m.plot()

listeECG = load_animal_datas()
test = create_test(listeECG)
train = create_train(listeECG)
afficher_un_ECG(listeECG)


