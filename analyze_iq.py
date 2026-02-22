"""
analyze_iq.py

Replay and visualize your recorded IQ data.

Instructions:
- Load 'capture_iq.bin'.
- Implement plotting functions below.
"""

import numpy as np
import matplotlib.pyplot as plt

INPUT_FILE = 'capture_iq.bin'
FS = 1e6  # sample rate in Hz

# ===== Load IQ data =====
iq_data = np.fromfile(INPUT_FILE, dtype=np.complex64)

# ===== Implement visualization functions =====

def plot_time_domain(iq):
    """
    Plot I and Q components over time.
    """
    # TODO: implement function
    plt.figure()
    plt.plot(np.real(iq), label='I')
    plt.plot(np.imag(iq), label='Q')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.title('Time-Domain IQ')
    plt.legend()
    plt.show()

def plot_fft(iq, fs):
    """
    Plot frequency-domain spectrum.
    """
    # TODO: implement FFT visualization
    N = len(iq)
    freq_axis = np.fft.fftfreq(N, 1/fs)
    spectrum = np.fft.fftshift(np.fft.fft(iq))
    plt.figure()
    plt.plot(freq_axis/1e6, 20*np.log10(np.abs(spectrum)))
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Magnitude (dB)')
    plt.title('Frequency-Domain Spectrum')
    plt.show()

def plot_spectrogram(iq, fs, nfft=1024, overlap=512):
    """
    Plot spectrogram of IQ data.
    """
    # TODO: implement spectrogram
    plt.figure()
    plt.specgram(iq, NFFT=nfft, Fs=fs, noverlap=overlap, scale='dB')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Spectrogram')
    plt.show()

# ===== Generate plots =====
plot_time_domain(iq_data)
plot_fft(iq_data, FS)
plot_spectrogram(iq_data, FS)
