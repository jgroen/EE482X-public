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

# Perform DOA to find angle of arrival of C
theta_scan = np.linspace(-1*np.pi/2, np.pi/2, 10000)
results = []

R = X @ X.conj().T
Rinv = np.linalg.pinv(R)

for theta_i in theta_scan:
    a = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(theta_i))
    a = a.reshape(-1,1)
    power = 1/(a.conj().T @ Rinv @ a).squeeze()
    power_dB = 10*np.log10(np.abs(power))
    results.append(power_dB)

results = np.array(results)
results -= np.max(results)

# Pull out angle of C (THIS IS THE STUDENT MODIFICATION POINT)
results_temp = np.array(results)
results_temp[int(len(results)*0.4):] = -9999*np.ones(int(len(results)*0.6))
max_angle = theta_scan[np.argmax(results_temp)]
print("max_angle:", max_angle)

# Calc MVDR weights (NO TRAINING DATA)
s = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(max_angle))
s = s.reshape(-1,1)
w = (Rinv @ s)/(s.conj().T @ Rinv @ s)

# Calc beam pattern
w = w.squeeze()
N_fft = 2048
w_padded = np.concatenate((w, np.zeros(N_fft - Nr)))
w_fft_dB = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(w_padded)))**2)
w_fft_dB -= np.max(w_fft_dB)
theta_bins = np.arcsin(np.linspace(-1, 1, N_fft))

plt.plot(theta_bins * 180 / np.pi, w_fft_dB)
plt.plot(theta_scan * 180 / np.pi, results, 'r')
plt.vlines(ymax=np.max(results),
           ymin=np.min(results),
           x=max_angle*180/np.pi,
           color='g', linestyle='--')
plt.xlabel("Angle [deg]")
plt.ylabel("Magnitude [dB]")
plt.title("Beam Pattern and DOA Results, Without Training")
plt.grid()
plt.show()

# ================================
# TRAINING DATA (A + B ONLY)
# ================================
filename = '3p3G_A_B.npy'
X_A_B = np.load(filename)

R_training = X_A_B @ X_A_B.conj().T
Rinv_training = np.linalg.pinv(R_training)

# Calc MVDR weights using training covariance
s = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(max_angle))
s = s.reshape(-1,1)
w_training = (Rinv_training @ s)/(s.conj().T @ Rinv_training @ s)
