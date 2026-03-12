import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import time


# ----------------------------
# 1. Generate pulse train
# ----------------------------
num_symbols = 100
sps = 8
bits = np.random.randint(0, 2, num_symbols)  # 1's and 0's
pulse_train = np.array([])

for bit in bits:
    pulse = np.zeros(sps)
    pulse[0] = bit*2-1  # BPSK: ±1
    pulse_train = np.concatenate((pulse_train, pulse))

# ----------------------------
# 2. Raised-cosine filter
# ----------------------------
num_taps = 101
beta = 0.35
Ts = sps
t = np.arange(-51, 52)
h_rc = np.sinc(t/Ts) * np.cos(np.pi*beta*t/Ts) / (1 - (2*beta*t/Ts)**2)

samples = np.convolve(pulse_train, h_rc)

# Save original for plotting
samples_before = samples.copy()

# # ----------------------------
# # 3. Fractional delay filter
# # ----------------------------
delay = 0.4
N = 21
n = np.arange(-(N-1)//2, N//2+1)
h_fd = np.sinc(n - delay)
h_fd *= np.hamming(N)
h_fd /= np.sum(h_fd)

samples_after = np.convolve(samples, h_fd)
samples = samples_after.copy()

# ----------------------------
# 5. Frequency offset
# ----------------------------
fs = 1e6
fo = 1000
Ts = 1/fs
t = np.arange(0, Ts*len(samples), Ts)

# Convert to complex signal (imag part = 0)
samples_complex = samples.astype(np.complex128)

# Apply frequency offset
samples_after = samples_complex * np.exp(1j*2*np.pi*fo*t)
samples = samples_after.copy()


# ----------------------------
# Mueller and Muller
# ----------------------------

samples_interpolated = signal.resample_poly(samples, 16, 1)
samples = samples_interpolated.copy()

mu = 0 # initial estimate of phase of sample
out = np.zeros(len(samples) + 10, dtype=np.complex64)
out_rail = np.zeros(len(samples) + 10, dtype=np.complex64) # stores values, each iteration we need the previous 2 values plus current value

track_mu = np.zeros(len(out))

i_in = 0 # input samples index
i_out = 2 # output index (let first two outputs be 0)
while i_out < len(out) and i_in*16 + int(mu*16) < len(samples):
    out[i_out] = samples[i_in*16 + int(mu*16)] # grab what we think is the "best" sample
    out_rail[i_out] = int(np.real(out[i_out]) > 0) + 1j*int(np.imag(out[i_out]) > 0)
    x = (out_rail[i_out] - out_rail[i_out-2]) * np.conj(out[i_out-1])
    y = (out[i_out] - out[i_out-2]) * np.conj(out_rail[i_out-1])
    mm_val = np.real(y - x)
    mu += sps + 0.3*mm_val
    i_in += int(np.floor(mu)) # round down to nearest int since we are using it as an index
    track_mu[i_in] = mu
    mu = mu - np.floor(mu) # remove the integer part of mu
    i_out += 1 # increment output index
out = out[2:i_out] # remove the first two, and anything after i_out (that was never filled out)
samples = out # only include this line if you want to connect this code snippet with the Costas Loop later on
track_mu = track_mu[:len(samples_before)]
print(f'final number of samples: {len(samples)}')

plt.figure()

plt.subplot(3,1,1)
plt.plot(bits)
plt.title("Bit Stream")
plt.ylabel("Bit")

plt.subplot(3,1,2)
plt.plot(np.real(samples_after[60:-60]))
plt.plot(np.imag(samples_after[60:-60]))
plt.title("RX Signal (Upsampled BPSK)")
plt.ylabel("Amplitude")

plt.subplot(3,1,3)
plt.plot(np.real(samples[8:108]))
plt.title("Recovered Symbols (M&M Output)")
plt.ylabel("Symbol Value")

plt.tight_layout()
plt.show()

plt.figure()
plt.plot(samples_after[60:-60])
plt.scatter(np.arange(len(samples[8:108]))*sps, np.real(samples[8:108]), color='red')
plt.title("Timing Recovery Sampling Points")
plt.show()


nonzero_indices = np.where(track_mu != 0)[0]
nonzero_mu = track_mu[nonzero_indices]
# print(f'nonzero mu: {nonzero_mu}')
# print(f'nonzero indices: {nonzero_indices}')
plt.figure()
plt.plot(nonzero_indices, nonzero_mu)
plt.xlabel("Iteration")
plt.ylabel("mu (fractional sample offset)")
plt.title("Timing Recovery: mu over Iterations")
plt.grid(True)
plt.show()
