import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import hilbert

# Parameters
fs = 100e6  # Sampling frequency (100 MHz)
T = 1.0 / fs  # Sampling period
t = np.arange(0, 0.01, T)  # Time vector (10 ms duration)

# Carrier signal
fc = 20e6  # Carrier frequency (20 MHz)
Ac = 1.0  # Carrier amplitude
carrier = Ac * np.cos(2 * np.pi * fc * t)

# Modulating signal (100 Hz)
fm = 100  # Modulating frequency (100 Hz)
Am = 1.0  # Modulating amplitude
modulating_signal = (np.sin(2 * np.pi * fm * t) + np.sin(3 * 2 * np.pi * fm * t) + np.sin(5 * 2 * np.pi * fm * t))

# Frequency Modulation (FM)
kf = 5000  # Frequency deviation constant
integrated_modulating_signal = np.cumsum(modulating_signal) * T  # Integral of modulating signal
FM_signal = Ac * np.cos(2 * np.pi * fc * t + 2 * np.pi * kf * integrated_modulating_signal)

# FM Demodulation (Differentiator-Based)
# Step 1: Compute the derivative of the FM signal
derivative_FM_signal = np.diff(FM_signal) / T

# Step 2: Use the Hilbert transform to extract the envelope
analytic_signal = hilbert(derivative_FM_signal)
envelope = np.abs(analytic_signal)

# Step 3: Remove DC offset and normalize
demodulated_signal = envelope - np.mean(envelope)
demodulated_signal = demodulated_signal / np.max(np.abs(demodulated_signal))

# Time vector for demodulated signal (shifted by 1 due to derivative)
t_demod = t[:-1]

# Plotting
plt.figure(figsize=(12, 10))

# Modulating signal
plt.subplot(4, 1, 1)
plt.plot(t, modulating_signal)
plt.title('Modulating Signal (100 Hz)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

# FM signal (time domain)
plt.subplot(4, 1, 2)
plt.plot(t, FM_signal)
plt.title('FM Signal (Carrier: 20 MHz, Modulating: 100 Hz)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

# Demodulated signal (time domain)
plt.subplot(4, 1, 3)
plt.plot(t_demod, demodulated_signal)
plt.title('Demodulated Signal (Recovered 100 Hz Signal)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

# Frequency spectrum of demodulated signal
N = len(demodulated_signal)
yf = fft(demodulated_signal)
xf = fftfreq(N, T)[:N // 2]

plt.subplot(4, 1, 4)
plt.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
plt.title('Frequency Spectrum of Demodulated Signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.xlim([0, 600])  # Zoom in to show the 100 Hz component
plt.grid()

plt.tight_layout()
plt.show()