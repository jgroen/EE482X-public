"""
analyze_iq.py - Student Version

Replay and visualize your recorded IQ data.

Instructions:
- Fill in the parameters at the top.
- Implement missing code for the time-domain and FFT plots.
- Spectrogram is provided fully working.
"""

import numpy as np
import matplotlib.pyplot as plt

# ===== Parameters (fill these in) =====
INPUT_FILE = ''       # e.g., 'lab2_iq.bin'
FS = 0                # sample rate in Hz
CENTER_FREQ = 0       # SDR center frequency in Hz
IQ_DTYPE = None       # Data type of IQ samples in the file, e.g., np.complex64

# ===== Load IQ data =====
iq_data = np.fromfile(INPUT_FILE, dtype=IQ_DTYPE)
print(f"Loaded {len(iq_data)} complex samples from {INPUT_FILE} (dtype={IQ_DTYPE})")

# ===== Visualization functions =====

def plot_time_domain(iq, num_samples=10000):
    """
    Plot I and Q components over time.
    """
    plt.figure(figsize=(10, 4))

    # TODO: Plot the real (I) and imaginary (Q) parts of iq
    # Hint: use np.real(iq) and np.imag(iq)
    # STUDENT FILL IN BELOW
    # plt.plot(...)
    # plt.plot(...)

    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.title('Time-Domain IQ')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_fft(iq, fs, center_freq):
    """
    Plot frequency-domain spectrum (magnitude in dB), centered on center_freq.
    """
    N = len(iq)

    # TODO: Compute FFT and shift zero frequency to center
    # STUDENT FILL IN BELOW
    # spectrum = ...

    # TODO: Create frequency axis and shift by center_freq
    # freq_axis = ...

    # TODO: Plot magnitude in dB
    # STUDENT FILL IN BELOW
    # plt.plot(...)

    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Magnitude (dB)')
    plt.title('Frequency-Domain Spectrum')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_spectrogram(iq, fs, center_freq, nfft=1024, overlap=512):
    """
    Plot spectrogram of IQ data with y-axis relabeled relative to center_freq.
    This function is fully working — no edits needed.
    """
    plt.figure(figsize=(10, 4))
    Pxx, freqs, bins, im = plt.specgram(
        iq,
        NFFT=nfft,
        Fs=fs,
        noverlap=overlap,
        scale='dB',
        mode='psd',
        cmap='viridis'
    )

    yticks = plt.yticks()[0]
    ytick_labels = [f"{(tick + center_freq)/1e6:.3f}" for tick in yticks]
    plt.yticks(yticks, ytick_labels)

    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (MHz)')
    plt.title('Spectrogram')
    plt.colorbar(label='Power (dB)')
    plt.tight_layout()
    plt.show()


# ===== Generate plots =====
plot_time_domain(iq_data)
plot_fft(iq_data, FS, CENTER_FREQ)
plot_spectrogram(iq_data, FS, CENTER_FREQ)
