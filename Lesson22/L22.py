import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, convolve, welch

# -----------------------------
# Parameters
# -----------------------------
num_bits = 200         # Number of BPSK symbols
sps = 8                # Samples per symbol
span = 6               # Filter span in symbols
noise_power = 0.001    # AWGN
pulse_type = "rrc"     # Options: "rect", "rrc"
matched = True          # Apply matched filter at receiver

# -----------------------------
# Generate BPSK symbols
# -----------------------------
bits = np.random.randint(0, 2, num_bits)
symbols = 2*bits - 1

# -----------------------------
# Generate pulse
# -----------------------------
if pulse_type == "rect":
    # Normalize rectangular pulse to unit symbol energy
    pulse = np.ones(sps) / np.sqrt(sps)
elif pulse_type == "rrc":
    num_taps = span*sps + 1
    pulse = firwin(num_taps, cutoff=1/sps, window='hamming')
    # Normalize to unit symbol energy
    pulse /= np.sqrt(np.sum(pulse**2))
else:
    raise ValueError("Unsupported pulse type")

# -----------------------------
# Upsample symbols
# -----------------------------
upsampled = np.zeros(len(symbols) * sps)
upsampled[::sps] = symbols

# -----------------------------
# Transmit signal
# -----------------------------
tx_signal = convolve(upsampled, pulse, mode='full')

# -----------------------------
# Add noise
# -----------------------------
rx_signal = tx_signal + np.sqrt(noise_power) * np.random.randn(len(tx_signal))

# -----------------------------
# Receiver: matched filter
# -----------------------------
if matched:
    rx_filtered = convolve(rx_signal, pulse[::-1], mode='full')
else:
    rx_filtered = rx_signal.copy()

# -----------------------------
# Compute symbol centers (skip filter transients)
# -----------------------------
# Use filter center instead of full length to align symbols correctly
tx_center = (len(pulse) - 1) // 2
rx_center = (len(pulse) - 1) // 2 if matched else 0
total_delay = tx_center + rx_center
first_symbol_center = total_delay
symbol_centers = first_symbol_center + np.arange(num_bits) * sps

# Skip the first and last few symbols affected by filter transients
transient_symbols = span  # number of symbols to skip at start/end
symbol_centers_clean = symbol_centers[transient_symbols : num_bits - transient_symbols]

# -----------------------------
# Eye diagram: zoomed around middle symbols
# -----------------------------
# Choose a middle range of symbols to avoid transients
start_symbol = 75
end_symbol = 125
symbol_centers_middle = symbol_centers_clean[start_symbol:end_symbol]

num_traces = len(symbol_centers_middle)  # 50 traces in this example
zoom_range = 2 * sps  # 2-symbol window per trace
half_range = zoom_range // 2
eye_data = []

for idx in symbol_centers_middle:
    start = idx - half_range
    end = idx + half_range
    if start >= 0 and end <= len(rx_filtered):
        eye_data.append(rx_filtered[start:end])
eye_data = np.array(eye_data)

# -----------------------------
# Samples at decision points (middle symbols)
# -----------------------------
symbol_samples = rx_filtered[symbol_centers_middle]

# -----------------------------
# PSD calculation
# -----------------------------
f, Pxx = welch(rx_signal, fs=sps, nperseg=512)

# -----------------------------
# Plot results
# -----------------------------
plt.figure(figsize=(14,8))

# -----------------------------
# Time-domain signal with aligned PCM overlay (no pre-delay)
# -----------------------------

# Compute total delay
tx_center = (len(pulse)-1)//2
rx_center = (len(pulse)-1)//2 if matched else 0
total_delay = tx_center + rx_center  # center of first received pulse

# Upsampled PCM waveform
ideal_pcm = np.repeat(symbols, sps)

# Only start the waveform at total_delay - sps//2
start_idx = total_delay - sps//2
end_idx = start_idx + len(ideal_pcm)

aligned_pcm = np.full_like(rx_filtered, np.nan)  # fill with NaN so it doesn't plot before start
# Assign values where it fits
if start_idx >= 0 and end_idx <= len(rx_filtered):
    aligned_pcm[start_idx:end_idx] = ideal_pcm
elif start_idx < 0:
    aligned_pcm[:end_idx] = ideal_pcm[-start_idx:]
else:
    aligned_pcm[start_idx:] = ideal_pcm[:len(rx_filtered)-start_idx]

# Plot
plt.subplot(2,2,1)
plt.plot(rx_filtered[:200], label='Received Signal')
plt.plot(aligned_pcm[:200], 'r', linewidth=1.5, label='Original Bits (PCM)')
plt.title(f"Received Signal (Time) [{pulse_type.upper()}, Matched={matched}]")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend(loc='upper left')

# Eye diagram (zoomed)
plt.subplot(2,2,2)
for trace in eye_data:
    plt.plot(trace, color='blue', alpha=0.6)
plt.axvline(zoom_range/2, color='red', linestyle='--', label='Sampling Instant')
plt.title(f"Eye Diagram (Zoomed) [{pulse_type.upper()}, Matched={matched}]")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.grid(True)

# Samples at decision points
plt.subplot(2,2,3)
symbol_indices = np.arange(start_symbol, end_symbol)  # 75, 76, ..., 124
plt.stem(symbol_indices, symbol_samples)
plt.title("Samples at Symbol Centers")
plt.xlabel("Symbol Index")
plt.ylabel("Amplitude")
plt.grid(True)

# PSD
plt.subplot(2,2,4)
plt.semilogy(f, Pxx)
plt.title(f"Power Spectral Density [{pulse_type.upper()}]")
plt.xlabel("Normalized Frequency")
plt.ylabel("PSD")
plt.grid(True)

plt.tight_layout()
plt.show()