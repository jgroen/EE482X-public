import numpy as np
import matplotlib.pyplot as plt

# ================================
# PARAMETERS (students will edit one line)
# ================================
sample_rate = 1e6
N = 10000
d = 0.5
Nr = 8

theta1 = 20 / 180 * np.pi
theta2 = 25 / 180 * np.pi   # <-- STUDENTS CHANGE THIS
theta3 = -40 / 180 * np.pi

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

X = s1 @ tone1 + s2 @ tone2 + 0.1 * s3 @ tone3

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
# MUSIC SETUP
# ================================
R = (X @ X.conj().T)/X.shape[1]
eigvals, eigvecs = np.linalg.eig(R)

# Sort eigenvalues (largest first)
idx = np.argsort(eigvals)[::-1]
eigvecs = eigvecs[:, idx]

# Assume 2 signals → noise subspace is remaining vectors
En = eigvecs[:, 2:]

# ================================
# SCAN
# ================================
theta_scan = np.linspace(-np.pi/2, np.pi/2, 1000)

results_mvdr = []
results_music = []

for theta in theta_scan:
    # MVDR
    p_mvdr = power_mvdr(theta, X)
    results_mvdr.append(10*np.log10(np.abs(p_mvdr)))

    # MUSIC
    s = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(theta)).reshape(-1,1)
    p_music = 1 / (s.conj().T @ En @ En.conj().T @ s)
    results_music.append(10*np.log10(np.abs(p_music)))

results_mvdr = np.array(results_mvdr)
results_mvdr -= np.max(results_mvdr)

results_music = np.array(results_music)
results_music -= np.max(results_music)

# ================================
# PLOT
# ================================
plt.plot(theta_scan*180/np.pi, results_mvdr, label="MVDR")
plt.plot(theta_scan*180/np.pi, results_music, label="MUSIC")
plt.xlabel("Theta [Degrees]")
plt.ylabel("DOA Metric (dB)")
plt.title("MVDR vs MUSIC")
plt.legend()
plt.grid()
plt.show()
