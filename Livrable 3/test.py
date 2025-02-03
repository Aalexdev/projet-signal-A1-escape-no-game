import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

# Paramètres
fs = 10000  # Fréquence d'échantillonnage
T = 1       # Durée du signal en secondes
t = np.linspace(0, T, fs*T, endpoint=False)

# Signal à moduler (somme de sinusoïdales)
f1, f2, f3 = 1500, 3000, 4500
m_t = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t) + np.sin(2 * np.pi * f3 * t)

# Modulation FM
fc = 100  # Fréquence porteuse
kf = 10   # Sensibilité en fréquence
s_t = np.cos(2 * np.pi * fc * t + 2 * np.pi * kf * np.cumsum(m_t) / fs)

# Démodulation FM avec PLL
# Nous allons utiliser un filtre passe-bande pour suivre la fréquence
analytic_signal = hilbert(s_t)  # Transformée de Hilbert pour obtenir la phase
instantaneous_phase = np.unwrap(np.angle(analytic_signal))  # Phase instantanée
demodulated_signal_PLL = np.diff(instantaneous_phase) * fs / (2 * np.pi * kf)  # Dérivée pour récupérer m(t)

# Affichage
plt.figure(figsize=(10,5))
plt.subplot(3,1,1)
plt.plot(t, m_t)
plt.title("Signal d'origine (message)")

plt.subplot(3,1,2)
plt.plot(t, s_t)
plt.title("Signal modulé FM")

plt.subplot(3,1,3)
plt.plot(t[:-1], demodulated_signal_PLL)
plt.title("Signal démodulé par PLL")

plt.tight_layout()

# Analyser les fréquences du signal démodulé
plt.figure(figsize=(10,5))
plt.specgram(demodulated_signal_PLL, NFFT=1024, Fs=fs, noverlap=512)
plt.title("Spectre du signal démodulé par PLL")

# Démodulation par Discriminateur de Fréquence
# Calcul de la variation de fréquence avec la dérivée de la phase

# Calcul de la variation de la phase
analytic_signal = hilbert(s_t)  # Transformation de Hilbert
instantaneous_phase = np.unwrap(np.angle(analytic_signal))  # Phase instantanée

# Dérivée de la phase pour obtenir la variation de fréquence
frequency_variation = np.diff(instantaneous_phase) * fs / (2 * np.pi)

# Appliquer une détection d'enveloppe pour récupérer le signal modulé
# Ce signal devrait être proportionnel à la fréquence de tes sinusoïdes
demodulated_signal_discrim = frequency_variation / kf

# Affichage
plt.figure(figsize=(10,5))
plt.subplot(3,1,1)
plt.plot(t, m_t)
plt.title("Signal d'origine (message)")

plt.subplot(3,1,2)
plt.plot(t, s_t)
plt.title("Signal modulé FM")

plt.subplot(3,1,3)
plt.plot(t[:-1], demodulated_signal_discrim)
plt.title("Signal démodulé par Discriminateur de Fréquence")

plt.tight_layout()

# Analyser les fréquences du signal démodulé
plt.figure(figsize=(10,5))
plt.specgram(demodulated_signal_discrim, NFFT=1024, Fs=fs, noverlap=512)
plt.title("Spectre du signal démodulé par Discriminateur de Fréquence")

plt.show()