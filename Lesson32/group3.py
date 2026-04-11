import numpy as np
import matplotlib.pyplot as plt

# ================================
# PARAMETERS (students will edit one line)
# ================================
sample_rate = 1e6
N = 10000
d = 0.5
Nr = 8

theta1 = 20 / 180 * np.pi   # interferer
theta2 = 25 / 180 * np.pi   # interferer
theta3 = -40 / 180 * np.pi  # signal of interest (SOI)

mask_fraction = 0.4   # <-- STUDENTS CHANGE THIS (try 0.2, 0.6, etc.)

# ================================
# SIGNAL GENERATION
# ================================
t = np.arange(N)/sample_rate

s1 = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(theta1)).reshape(-1,1)
s2 = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(theta2)).reshape(-1,1)
s3 = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(theta3)).reshape(-1,1)

tone1 = np.exp(2j*np.pi*0.01e6*t).reshape(1,-1)
tone2 = np.exp(2j*np.pi*0.02e6*t).reshape(1,-1)
tone3 = np.exp(2j*np.pi*0.03e6*t).reshape(1,-1)

# Interferers are stronger than SOI
X = 2*s1 @ tone1 + 2*s2 @ tone2 + 0.5*s3 @ tone3

n = np.random.randn(Nr, N) + 1j*np.random.randn(Nr, N)
X = X + 0.05*n

# ================================
# MVDR FUNCTION
# ================================
def power_mvdr(theta, X):
    s = np.exp(2j * np.pi * d * np.arange(X.shape[0]) * np.sin(theta)).reshape(-1,1)
    R = (X @ X.conj().T)/X.shape[1]
    Rinv = np.linalg.pinv(R)
    return 1/(s.conj().T @ Rinv @ s).squeeze()

# ================================
# SCAN (DOA ESTIMATION)
# ================================
theta_scan = np.linspace(-np.pi/2, np.pi/2, 1000)

results = []
for theta in theta_scan:
    p = power_mvdr(theta, X)
    results.append(10*np.log10(np.abs(p)))

results = np.array(results)
results -= np.max(results)

# ================================
# TRAINING DATA SELECTION (MASKING)
# ================================
results_temp = np.array(results)

cutoff = int(len(results) * mask_fraction)
results_temp[cutoff:] = -9999  # mask out part of angle space

# Estimate SOI angle
theta_est = theta_scan[np.argmax(results_temp)]

print("Estimated SOI angle (deg):", theta_est * 180 / np.pi)

# ================================
# PLOTS
# ================================
plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
plt.plot(theta_scan*180/np.pi, results)
plt.axvline(theta_est*180/np.pi, color='r', linestyle='--', label="Estimated SOI")
plt.title("DOA Spectrum")
plt.xlabel("Theta [Degrees]")
plt.ylabel("Power (dB)")
plt.legend()
plt.grid()

plt.subplot(1,2,2)
plt.plot(theta_scan*180/np.pi, results_temp)
plt.title("Masked Spectrum (Training Data Selection)")
plt.xlabel("Theta [Degrees]")
plt.grid()

plt.tight_layout()
plt.show()
