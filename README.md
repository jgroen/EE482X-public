# EE482X: EW Lab 2 — Recording, Replaying, and Analyzing IQ Data

This repository contains all files for **EW Lab 2** in EE482X. The lab focuses on capturing, replaying, and analyzing IQ data using HackRF One or USRP B205 SDRs, as well as comparing your own captures with real-world IQ datasets.

## Lab Overview

Students will:
1. Complete pre-lab reading and answer questions from pysdr.org, Chapter 14.
2. Record IQ samples from an SDR using Python.
3. Replay and visualize IQ data in time and frequency domains.
4. Download and analyze a real-world IQ dataset (Gent, Belgium).
5. Compare your recordings with the external dataset and interpret results in an EW context.

**Total points:** 60

## Files in this Repository

- `capture_iq.py` — Capture IQ samples from an SDR.
- `analyze_iq.py` — Replay and visualize your recorded IQ data.
- `analyze_external_iq.py` — Visualize an external IQ dataset (Gent dataset).

These scripts contain **clearly marked sections** for implementing new functions (e.g., FFT, spectrogram, time-domain plots). Students are expected to implement some functions but not write the entire pipeline from scratch.

## Instructions

1. Clone or download the repository:
   ```bash
   git clone https://github.com/jgroen/EE482X-public.git
