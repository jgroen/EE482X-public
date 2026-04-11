import numpy as np
import matplotlib.pyplot as plt

# ================================
# PARAMETERS (students will edit one line)
# ================================
sample_rate = 1e6
N = 4000
d = 0.5
Nr = 8

mu = 0.01   # <-- STUDENTS CHANGE THIS (try 0.001, 0.05, 0.1)

theta_sig = 20 / 180 * np.pi     # desired signal
theta_int = -30 / 180 * np.pi    # interferer

# ================================
# SIGNAL GENERATION
# ================================
t = np.arange(N)/sample_rate

s_sig = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(theta_sig)).reshape(-1,1)
s_int = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(theta_int)).reshape(-1,1)

tone_sig = np.exp(2j*np.pi*0.02e6*t).reshape(1,-1)
tone_int = np.exp(2j*np.pi*0.025e6*t).reshape(1,-1)

X = s_sig @ tone_sig + 2 * s_int @ tone_int  # strong interferer

n = np.random.randn(Nr, N) + 1j*np.random.randn(Nr, N)
X = X + 0.05*n

# Desired reference (what we want to recover)
d_ref = tone_sig.flatten()

# ================================
# LMS ADAPTIVE BEAMFORMING
# ================================
w = np.zeros(Nr, dtype=complex)
y = np.zeros(N, dtype=complex)
e = np.zeros(N, dtype=complex)

for i in range(N):
    x = X[:, i]

    y[i] = np.conj(w) @ x        # output
    e[i] = d_ref[i] - y[i]       # error

    w = w + mu * x * np.conj(e[i])  # LMS update

# ================================
# PERFORMANCE METRIC
# ================================
mse = np.abs(e)**2

# ================================
# PLOTS
# ================================
plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
plt.plot(10*np.log10(mse + 1e-12))
plt.title("Error (MSE) vs Iteration")
plt.xlabel("Sample")
plt.ylabel("Error (dB)")
plt.grid()

plt.subplot(1,2,2)
plt.plot(np.real(d_ref[:500]), label="Desired")
plt.plot(np.real(y[:500]), label="Output", alpha=0.7)
plt.title("Signal Tracking (first 500 samples)")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
