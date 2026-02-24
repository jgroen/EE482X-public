"""
analyze_external_iq.py - Student Version

Load and visualize an external IQ dataset.

Instructions:
- Set INPUT_FILE to your downloaded .bin file.
- Fill in parameters and implement plotting functions as desired.
- You may reuse previous lab code or explore new visualizations.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from numpy.fft import fft, fftshift, fftfreq
from scipy.signal import welch

# ===== User parameters =====
INPUT_FILE = ''       # Path to downloaded .bin file
FS = None             # Sample rate in Hz
CENTER_FREQ = None    # Center frequency of the capture (Hz)
IQ_DTYPE = None       # Data type of IQ samples (e.g., np.complex64)
# ==========================

# ===== Load IQ data =====
# Hint: use np.fromfile with dtype=IQ_DTYPE
iq_data = np.fromfile(INPUT_FILE, dtype=IQ_DTYPE)
print(f"Loaded {len(iq_data)} complex samples from {INPUT_FILE}")

# ===== Implement visualization functions =====

def plot_fft(iq, fs, center_freq):
    """
    Frequency-domain spectrum (magnitude in dB), centered on CENTER_FREQ.
    """
    # TODO: Implement FFT plotting
    pass

def plot_spectrogram(iq, fs, center_freq, nfft=1024, overlap=512):
    """
    Time-frequency spectrogram (PSD in dB), y-axis labeled relative to center frequency.
    """
    # TODO: Implement spectrogram plotting
    pass

def plot_histogram(iq, bins=100):
    """
    Histogram of IQ amplitudes.
    """
    # TODO: Implement histogram plotting
    pass

def plot_constellation(iq, num_samples=5000):
    """
    IQ constellation plot (scatter I vs Q).
    """
    # TODO: Implement IQ constellation plotting
    pass

def plot_amplitude_envelope(iq, window_size=1024):
    """
    Amplitude envelope over time with optional moving average.
    """
    # TODO: Implement amplitude envelope plotting
    pass

def plot_psd(iq, fs, center_freq=None, nperseg=16384):
    """
    Power Spectral Density (PSD) using Welch's method.
    """
    # TODO: Implement PSD plotting
    pass

def plot_autocorr(iq, max_lags=2000):
    """
    Autocorrelation of IQ amplitude.
    """
    # TODO: Implement autocorrelation plotting
    pass

# ===== Generate plots =====
# Students can call any combination of the above functions
# Example usage (replace with your own implementations):
# plot_fft(iq_data, FS, CENTER_FREQ)
# plot_spectrogram(iq_data, FS, CENTER_FREQ)
# plot_histogram(iq_data)
# plot_constellation(iq_data)
# plot_amplitude_envelope(iq_data)
# plot_psd(iq_data, FS)
# plot_autocorr(iq_data)
