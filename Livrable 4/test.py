import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

# Parameters
fs = 1000      # Sampling frequency
T = 5          # Duration in seconds
t = np.linspace(0, T, int(fs * T), endpoint=False)

# Message signal (5Hz sine wave)
fm = 5         # Message frequency
A_m = 1        # Message amplitude
m_t = (np.sin(2 * np.pi * fm * t) + np.sin(2 * np.pi * fm * t * 2))/2

# Carrier signal (50Hz)
fc = 50        # Carrier frequency

# Modulation index (β = 5)
beta = 1

# Frequency Modulation (FM)
# ---------------------------
# 1. Compute integral of message signal
dt = 1/fs
integral_m = np.cumsum(m_t) * dt

# 2. Calculate frequency sensitivity (k_f = Δf/A_m)
k_f = (beta * fm) / A_m

print(k_f)

# 3. Create phase argument for FM
phi = 2 * np.pi * fc * t + 2 * np.pi * k_f * integral_m

# 4. Generate FM signal
fm_signal = np.cos(phi)

# FM Demodulation
# -----------------
# 1. Compute analytic signal using Hilbert transform
analytic_signal = hilbert(fm_signal)

# 2. Extract instantaneous phase
instantaneous_phase = np.unwrap(np.angle(analytic_signal))

# 3. Remove carrier frequency component
residual_phase = instantaneous_phase - 2 * np.pi * fc * t

# 4. Differentiate to recover message
demodulated_derivative = np.gradient(residual_phase, t)

# 5. Scale by frequency sensitivity
demodulated = demodulated_derivative / (2 * np.pi * k_f)

# Plotting
plt.figure(figsize=(12, 8))

plt.subplot(7, 1, 1)
plt.plot(t, m_t)
plt.title('Original Message Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(7, 1, 2)
plt.plot(t, fm_signal)
plt.title('FM Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')


plt.subplot(7, 1, 3)
plt.plot(t, analytic_signal)

plt.subplot(7, 1, 4)
plt.plot(t, instantaneous_phase)

plt.subplot(7, 1, 5)
plt.plot(t, residual_phase)

plt.subplot(7, 1, 6)
plt.plot(t, demodulated_derivative)

plt.subplot(7, 1, 7)
plt.plot(t, demodulated, label='Demodulated')
plt.plot(t, m_t, label='Original', linestyle='--')
plt.title('Demodulated Signal vs Original')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()

plt.tight_layout()
plt.show()