import matplotlib.pyplot as plt
import numpy as np

# Array params
center_freq = 3.3e9
sample_rate = 30e6
d = 0.045 * center_freq / 3e8
print("d:", d)

# Includes all three signals, we'll call C our SOI
filename = '3p3G_A_B_C.npy'
X = np.load(filename)
Nr = X.shape[0]

# ================================
# WIDEBAND INTERFERER MODELING (KEY ADDITION)
# ================================
# Fractional bandwidth controls how "spread out" interference is
fractional_bw = 0.1   # <-- STUDENTS CHANGE THIS (try 0.01, 0.2)

# Create colored noise to simulate wideband interferer
R = np.cov(X)
U, S, V = np.linalg.svd(R)
A = U @ np.diag(np.sqrt(S))

N = X.shape[1]
white_noise = (np.random.randn(Nr, N) + 1j*np.random.randn(Nr, N)) / np.sqrt(2)
wideband_interferer = A @ white_noise

# Inject wideband interferer into received signal
X = X + fractional_bw * wideband_interferer

# ================================
# DOA (MVDR)
# ================================
theta_scan = np.linspace(-1*np.pi/2, np.pi/2, 10000)
results = []

R = X @ X.conj().T
Rinv = np.linalg.pinv(R)

for theta_i in theta_scan:
    a = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(theta_i)).reshape(-1,1)
    power = 1/(a.conj().T @ Rinv @ a).squeeze()
    power_dB = 10*np.log10(np.abs(power))
    results.append(power_dB)

results = np.array(results)
results -= np.max(results)

# ================================
# SOI ANGLE ESTIMATION (MASKING SAME AS BEFORE)
# ================================
results_temp = np.array(results)
results_temp[int(len(results)*0.4):] = -9999*np.ones(int(len(results)*0.6))
max_angle = theta_scan[np.argmax(results_temp)]
print("max_angle:", max_angle)

# ================================
# MVDR WEIGHTS
# ================================
s = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(max_angle)).reshape(-1,1)
w = (Rinv @ s)/(s.conj().T @ Rinv @ s)

# ================================
# BEAM PATTERN
# ================================
w = w.squeeze()
N_fft = 2048
w_padded = np.concatenate((w, np.zeros(N_fft - Nr)))

w_fft_dB = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(w_padded)))**2)
w_fft_dB -= np.max(w_fft_dB)

theta_bins = np.arcsin(np.linspace(-1, 1, N_fft))

# ================================
# PLOT
# ================================
plt.plot(theta_bins * 180 / np.pi, w_fft_dB, label="Beam Pattern")
plt.plot(theta_scan * 180 / np.pi, results, 'r', label="DOA Spectrum")

plt.vlines(x=max_angle*180/np.pi,
           ymin=np.min(results),
           ymax=np.max(results),
           color='g', linestyle='--')

plt.xlabel("Angle [deg]")
plt.ylabel("Magnitude [dB]")
plt.title("Wideband Interferers: MVDR Degradation Effect")
plt.legend()
plt.grid()
plt.show()
