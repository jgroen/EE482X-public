"""
capture_iq.py

Capture IQ data from a HackRF One or USRP B205 SDR.

Instructions:
- Set center frequency, sample rate, gain, and capture duration.
- Run the script to capture IQ samples.
- Output will be saved as 'capture_iq.bin'.
"""

import numpy as np

# ====== User parameters ======
CENTER_FREQ = 2.4e9   # Hz
SAMPLE_RATE = 1e6     # Hz
GAIN = 40             # dB
DURATION = 5          # seconds
OUTPUT_FILE = 'capture_iq.bin'
SDR_TYPE = 'HackRF'   # or 'USRP'
# =============================

def capture_iq(center_freq, sample_rate, gain, duration, output_file, sdr_type):
    """
    Placeholder function to capture IQ samples.
    Implement SDR capture here using PyHackRF or UHD for USRP.
    """
    print(f"Capturing {duration}s of IQ data at {center_freq/1e6} MHz...")
    # Example placeholder: generate random complex samples
    num_samples = int(sample_rate * duration)
    iq_data = (np.random.randn(num_samples) + 1j*np.random.randn(num_samples)).astype(np.complex64)
    
    # Save to file
    iq_data.tofile(output_file)
    print(f"Saved {num_samples} samples to {output_file}")

if __name__ == "__main__":
    capture_iq(CENTER_FREQ, SAMPLE_RATE, GAIN, DURATION, OUTPUT_FILE, SDR_TYPE)
