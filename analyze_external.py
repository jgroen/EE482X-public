"""
analyze_external_iq.py

Load and visualize an external IQ dataset (Gent dataset).

Instructions:
- Set INPUT_FILE to your downloaded .bin file.
- Implement at least one new visualization function (FFT, spectrogram, histogram).
"""

import numpy as np
import matplotlib.pyplot as plt

# ===== User parameters =====
INPUT_FILE = 'wf10Msps_g76_rabot_f5240MHz_r1.bin'
FS = 10e6  # Sample rate (from filename metadata)
# ==========================

# ===== Load IQ data =====
iq_data = np.fromfile(INPUT_FILE, dtype=np.complex64)

# ===== Implement visualization functions =====

def plot_fft(iq, fs):
    """
    Frequency-domain spectrum.
    """
    # TODO: implement
    N = len(iq)
    freq_axis = np.fft.fftfreq(N, 1/fs)
    spectrum = np.fft.fftshift(np.fft.fft(iq))
    plt.figure()
    plt.plot(freq_axis/1e6, 20*np.log10(np.abs(spectrum)))
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Magnitude (dB)')
    plt.title('External Dataset FFT')
    plt.show()

def plot_spectrogram(iq, fs, nfft=1024, overlap=512):
    """
    Time-frequency spectrogram.
    """
    # TODO: implement
    plt.figure()
    plt.specgram(iq, NFFT=nfft, Fs=fs, noverlap=overlap, scale='dB')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('External Dataset Spectrogram')
    plt.show()

def plot_histogram(iq):
    """
    Histogram of IQ amplitudes.
    """
    # TODO: implement
    plt.figure()
    plt.hist(np.abs(iq), bins=100)
    plt.xlabel('Amplitude')
    plt.ylabel('Count')
    plt.title('IQ Amplitude Histogram')
    plt.show()

# ===== Generate plots =====
plot_fft(iq_data, FS)
plot_spectrogram(iq_data, FS)
plot_histogram(iq_data)
