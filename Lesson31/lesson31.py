import numpy as np
import matplotlib.pyplot as plt

# ================================
# EXPERIMENT CONTROLS (EDIT THESE)
# ================================

N = 10000          # EDIT: try 200 (covariance breakdown)
noise_scale = 0.05 # EDIT: try 0.2 (more noise)
interference_scale = 0.1  # EDIT: try 5 (strong jammer)

theta1_deg = 20    # signal 1
theta2_deg = 25    # signal 2 (EDIT: try 22 for closer spacing)
theta3_deg = -40   # interferer

# ================================

sample_rate = 1e6

# Create time vector
t = np.arange(N)/sample_rate

d = 0.5 # half wavelength spacing
Nr = 8  # number of elements

# Convert to radians
theta1 = np.deg2rad(theta1_deg)
theta2 = np.deg2rad(theta2_deg)
theta3 = np.deg2rad(theta3_deg)

# Steering vectors
s1 = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(theta1)).reshape(-1,1)
s2 = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(theta2)).reshape(-1,1)
s3 = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(theta3)).reshape(-1,1)

# Tones
tone1 = np.exp(2j*np.pi*0.01e6*t).reshape(1,-1)
tone2 = np.exp(2j*np.pi*0.02e6*t).reshape(1,-1)
tone3 = np.exp(2j*np.pi*0.03e6*t).reshape(1,-1)

# Received signal
X = s1 @ tone1 + s2 @ tone2 + interference_scale * s3 @ tone3

# Noise
n = np.random.randn(Nr, N) + 1j*np.random.randn(Nr, N)
X = X + noise_scale * n

# ================================
# MVDR POWER FUNCTION
# ================================
def power_mvdr(theta, X):
    Nr = X.shape[0]
    s = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(theta)).reshape(-1,1)

    R = (X @ X.conj().T)/X.shape[1]
    Rinv = np.linalg.pinv(R)

    return 1/(s.conj().T @ Rinv @ s).squeeze()

# ================================
# OPTIONAL: CONVENTIONAL BF (for comparison)
# ================================
def power_conventional(theta, X):
    Nr = X.shape[0]
    s = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(theta)).reshape(-1,1)
    return np.abs((s.conj().T @ X).var())

# ================================
# SCAN
# ================================
theta_scan = np.linspace(-np.pi/2, np.pi/2, 1000)

results_mvdr = []
results_conv = []

for theta_i in theta_scan:
    power = power_mvdr(theta_i, X)
    results_mvdr.append(10*np.log10(np.abs(power)))

    # Uncomment for comparison
    power_c = power_conventional(theta_i, X)
    results_conv.append(10*np.log10(power_c))

# Normalize
results_mvdr = np.array(results_mvdr)
results_mvdr -= np.max(results_mvdr)

results_conv = np.array(results_conv)
results_conv -= np.max(results_conv)

# ================================
# PLOTS
# ================================

plt.plot(theta_scan*180/np.pi, results_mvdr, label="MVDR")

# EDIT: uncomment to compare
plt.plot(theta_scan*180/np.pi, results_conv, '--', label="Conventional")

plt.xlabel("Theta [Degrees]")
plt.ylabel("DOA Metric (dB)")
plt.legend()
plt.grid()
plt.title("MVDR vs Conventional Beamforming")
plt.show()
