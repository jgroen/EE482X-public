import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# PARAMETERS (students can read these)
# -------------------------------
N = 64              # Number of subcarriers (FFT size)
CP_len = 16         # Cyclic prefix length
num_symbols = 200   # Number of OFDM symbols
SNR_dB = 0          # Try changing this later!

# -------------------------------
# STEP 1: Generate QPSK Symbols
# -------------------------------
data = (2*np.random.randint(0, 2, (num_symbols, N)) - 1) + \
       1j*(2*np.random.randint(0, 2, (num_symbols, N)) - 1)
data /= np.sqrt(2)  # Normalize power

# IFFT to create OFDM symbols
ofdm_symbols = np.fft.ifft(data, axis=1)

# -------------------------------
# STEP 2: Add Cyclic Prefix
# -------------------------------
ofdm_with_cp = np.hstack([
    ofdm_symbols[:, -CP_len:],   # CP (copy of end)
    ofdm_symbols
])

# Serialize into 1D signal
tx_signal = ofdm_with_cp.flatten()

# -------------------------------
# STEP 3: Add Noise
# -------------------------------
signal_power = np.mean(np.abs(tx_signal)**2)
noise_power = signal_power / (10**(SNR_dB/10))

noise = np.sqrt(noise_power/2) * (
    np.random.randn(len(tx_signal)) + 1j*np.random.randn(len(tx_signal))
)

rx_signal = tx_signal + noise

# -------------------------------
# STEP 4: PSD (should look wideband)
# -------------------------------
plt.figure()
plt.psd(rx_signal, NFFT=1024)
plt.title("Power Spectral Density (PSD)")
plt.xlabel("Frequency")
plt.ylabel("Power")
plt.show()


# -------------------------------
# STEP 5: Targeted Cyclic Autocorrelation
# -------------------------------

# -------------------------------
# STUDENT TASK 1:
# Based on OFDM structure:
# What lag should produce a strong correlation?
# -------------------------------
target_lag = 64   # <-- STUDENTS FILL THIS IN


# Compute correlation at that lag
caf_value = np.abs(np.mean(
    rx_signal[:len(rx_signal)-target_lag] *
    np.conj(rx_signal[target_lag:])
))

print(f"Correlation at lag {target_lag}: {caf_value:.4f}")


# -------------------------------
# OPTIONAL: Check a small window around it
# -------------------------------
window = 5
lags = np.arange(target_lag - window, target_lag + window + 1)
caf_vals = []

for tau in lags:
    val = np.abs(np.mean(
        rx_signal[:len(rx_signal)-tau] *
        np.conj(rx_signal[tau:])
    ))
    caf_vals.append(val)

plt.figure()
plt.stem(lags, caf_vals)
plt.title("Cyclic Autocorrelation Around Target Lag")
plt.xlabel("Lag")
plt.ylabel("Correlation Magnitude")
plt.show()

# -------------------------------
# STEP 6: Targeted Alpha Detection
# -------------------------------

fs = 1.0  # normalized sampling rate

# -------------------------------
# STUDENT TASK 2:
# Convert lag -> cyclic frequency
# -------------------------------
alpha_est = 1/target_lag   # <-- STUDENTS FILL THIS IN


# Convert small lag window into alpha values
window = 5
lags = np.arange(target_lag - window, target_lag + window + 1)

alphas = fs / lags
caf_vals = []

for tau in lags:
    val = np.abs(np.mean(
        rx_signal[:len(rx_signal)-tau] *
        np.conj(rx_signal[tau:])
    ))
    caf_vals.append(val)

# Plot: correlation vs alpha
plt.figure()
plt.plot(alphas, caf_vals, marker='o')
plt.axvline(alpha_est, linestyle='--', label='Predicted α')
plt.title("Targeted Cyclostationary Detection (α Domain)")
plt.xlabel("Cyclic Frequency (alpha)")
plt.ylabel("Correlation Magnitude")
plt.legend()
plt.grid()
plt.show()
