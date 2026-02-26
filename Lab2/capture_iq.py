"""
capture_iq.py

Capture IQ data from a HackRF One or USRP B205 SDR.

Instructions:
- Set center frequency, sample rate, gain, and capture duration.
- Run the script to capture IQ samples.
- Output will be saved as 'lab2_iq.bin'.
"""

from python_hackrf import pyhackrf
import numpy as np
import time

CENTER_FREQ = 
SAMPLE_RATE = 
LNA_GAIN = 
VGA_GAIN = 
DURATION = 
OUTPUT_FILE = "lab2_iq.bin"
BASEBAND_FILTER = 

def capture_iq():
    pyhackrf.pyhackrf_init()
    sdr = pyhackrf.pyhackrf_open()

    bw = pyhackrf.pyhackrf_compute_baseband_filter_bw_round_down_lt(
        BASEBAND_FILTER
    )

    sdr.pyhackrf_set_sample_rate(SAMPLE_RATE)
    sdr.pyhackrf_set_baseband_filter_bandwidth(bw)
    sdr.pyhackrf_set_freq(CENTER_FREQ)
    sdr.pyhackrf_set_lna_gain(LNA_GAIN)
    sdr.pyhackrf_set_vga_gain(VGA_GAIN)
    sdr.pyhackrf_set_amp_enable(False)
    sdr.pyhackrf_set_antenna_enable(False)

    num_samples = int(DURATION * SAMPLE_RATE)
    samples = np.zeros(num_samples, dtype=np.complex64)
    last_idx = 0

    def rx_callback(device, buffer, buffer_length, valid_length):
        nonlocal samples, last_idx

        accepted = valid_length // 2
        remaining = len(samples) - last_idx
        if remaining <= 0:
            return 0

        accepted = min(accepted, remaining)

        iq = buffer[:2*accepted].astype(np.int8)
        iq = iq[0::2] + 1j * iq[1::2]
        iq /= 128.0

        samples[last_idx:last_idx + accepted] = iq
        last_idx += accepted
        return 0

    sdr.set_rx_callback(rx_callback)
    sdr.pyhackrf_start_rx()
    time.sleep(DURATION)
    sdr.pyhackrf_stop_rx()

    sdr.pyhackrf_close()
    pyhackrf.pyhackrf_exit()

    samples = samples[:last_idx]
    samples.tofile(OUTPUT_FILE)

    print(f"Saved {last_idx} complex samples to {OUTPUT_FILE}")

if __name__ == "__main__":
    capture_iq()
