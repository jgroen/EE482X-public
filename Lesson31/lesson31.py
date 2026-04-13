import numpy as np
import matplotlib.pyplot as plt

# ================================
# EXPERIMENT CONTROLS (EDIT THESE)
# ================================

N = 10000          # EDIT: try 200 (covariance breakdown)
noise_scale = 0.05 # EDIT: try 0.2 (more noise)
interference_scale = 1  # EDIT: try 5 (strong jammer)

theta1_deg = 20    # signal 1
theta2_deg = 25    # signal 2 (EDIT: try 22 for closer spacing)
theta3_deg = 15   # interferer

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



# ================================
# BEAMFORMING (APPLY WEIGHTS)
# ================================

# 1. Pick look direction (strongest MVDR peak)
theta_look = theta_scan[np.argmax(results_mvdr)]
print("Steering to angle (deg):", theta_look * 180 / np.pi)

Nr = X.shape[0]

# Steering vector
s = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(theta_look)).reshape(-1,1)

# Covariance
R = (X @ X.conj().T)/X.shape[1]
Rinv = np.linalg.pinv(R)

# ================================
# 2. Compute Weights
# ================================

# MVDR weights
w_mvdr = (Rinv @ s)/(s.conj().T @ Rinv @ s)

# Conventional weights
w_conv = s / Nr

# ================================
# 3. Apply Beamformers
# ================================

y_mvdr = w_mvdr.conj().T @ X
y_conv = w_conv.conj().T @ X

# Flatten for plotting
y_mvdr = y_mvdr.flatten()
y_conv = y_conv.flatten()

# ================================
# 4. BEAM PATTERN (ANGLE DOMAIN)
# ================================

theta_plot = np.linspace(-np.pi/2, np.pi/2, 1000)

pattern_mvdr = []
pattern_conv = []

for theta in theta_plot:
    s_theta = np.exp(2j * np.pi * d * np.arange(Nr) * np.sin(theta)).reshape(-1,1)

    # Array response (beam pattern)
    resp_mvdr = np.abs(w_mvdr.conj().T @ s_theta)**2
    resp_conv = np.abs(w_conv.conj().T @ s_theta)**2

    pattern_mvdr.append(10*np.log10(resp_mvdr.squeeze()))
    pattern_conv.append(10*np.log10(resp_conv.squeeze()))

pattern_mvdr = np.array(pattern_mvdr)
pattern_conv = np.array(pattern_conv)

# Normalize
pattern_mvdr -= np.max(pattern_mvdr)
pattern_conv -= np.max(pattern_conv)

# ================================
# 5. PLOT (THIS IS THE MONEY PLOT)
# ================================

plt.figure(figsize=(10,5))

plt.plot(theta_plot*180/np.pi, pattern_conv, '--', label="Conventional")
plt.plot(theta_plot*180/np.pi, pattern_mvdr, label="MVDR")

# Mark true angles
plt.axvline(theta1_deg, color='g', linestyle=':', label="Signal 1")
plt.axvline(theta2_deg, color='g', linestyle=':')
plt.axvline(theta3_deg, color='r', linestyle=':', label="Jammer")

plt.xlabel("Angle [Degrees]")
plt.ylabel("Array Response (dB)")
plt.title("Beam Pattern: MVDR vs Conventional")
plt.legend()
plt.grid()
plt.show()