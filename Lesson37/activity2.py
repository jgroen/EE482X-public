import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# STEP 1: Load Mystery Signal
# -------------------------------
rx_signal = np.load("mystery_signal.npy")

# -------------------------------
# STEP 2: PSD (Looks like noise)
# -------------------------------
plt.figure()
plt.psd(rx_signal, NFFT=1024)
plt.title("PSD of Mystery Signal")
plt.xlabel("Frequency")
plt.ylabel("Power")
plt.show()


# -------------------------------
# STEP 3: Cyclostationary Detection (Alpha Sweep)
# -------------------------------
fs = 1.0
max_lag = 200

lags = np.arange(1, max_lag)
caf_vals = []

for tau in lags:
    val = np.abs(np.mean(
        rx_signal[:len(rx_signal)-tau] *
        np.conj(rx_signal[tau:])
    ))
    caf_vals.append(val)

alphas = fs / lags

# -------------------------------
# Plot: Does structure exist?
# -------------------------------
plt.figure()
plt.plot(alphas, caf_vals)
plt.title("Cyclostationary Detection (Alpha Domain)")
plt.xlabel("Cyclic Frequency (alpha)")
plt.ylabel("Correlation Magnitude")
plt.grid()
plt.show()
