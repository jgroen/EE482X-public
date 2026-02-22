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
   ```
2. Complete the **pre-lab reading** (pysdr.org, Chapter 14, skip MIDAS Blue file format) before your lab session.

3. Follow the steps in the Python scripts to **capture and analyze IQ data**:
   - `capture_iq.py` – record IQ samples from your SDR.
   - `analyze_iq.py` – replay and visualize your recorded IQ data.
   - `analyze_external_iq.py` – visualize an external Gent IQ dataset.

4. Download **one external IQ `.bin` file** from the Gent Technology Recognition Dataset:
   [Gent Technology Recognition Dataset](https://github.com/JaronFontaine/Technology-Recognition-dataset-of-real-life-LTE-WiFi-and-DVB-T)

5. Record the filename and metadata from the downloaded file (technology, sample rate, gain, center frequency, location, capture instance) in your lab report.

6. Implement additional visualization functions in `analyze_iq.py` or `analyze_external_iq.py` (e.g., FFT, spectrogram, histograms) as instructed in the lab.

7. Submit the following:
   - `capture_iq.bin`
   - Modified Python scripts (`analyze_iq.py`, `analyze_external_iq.py`)
   - All plots labeled by deliverable letter
   - Written answers to all lab questions

## Notes for Students

- All Gent IQ files are raw binary `.bin` in complex64 format.
- Metadata is encoded in the filename; no separate `.sigmf` file is required.
- Focus on interpreting patterns in the plots and comparing with your own recordings.
- Keep all plots and answers **clearly labeled** for easy grading.
- Use Python packages `numpy` and `matplotlib` (or install via `pip install numpy matplotlib`).
