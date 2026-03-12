import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


# ----------------------------
# 1. Generate pulse train
# ----------------------------
def generate_pulse_train(num_symbols, sps):

    bits = np.random.randint(0, 2, num_symbols)
    pulse_train = np.array([])

    for bit in bits:
        pulse = np.zeros(sps)
        pulse[0] = bit*2 - 1   # BPSK: ±1
        pulse_train = np.concatenate((pulse_train, pulse))

    return bits, pulse_train


# ----------------------------
# 2. Raised cosine filter
# ----------------------------
def raised_cosine_filter(pulse_train, sps, beta=0.35, num_taps=101):

    t = np.arange(-(num_taps//2), num_taps//2 + 1)

    h_rc = np.sinc(t/sps) * np.cos(np.pi*beta*t/sps) / (1 - (2*beta*t/sps)**2)

    samples = np.convolve(pulse_train, h_rc)

    return samples, h_rc


# ----------------------------
# 3. Fractional delay
# ----------------------------
def fractional_delay(samples, delay=0.4, N=21):

    n = np.arange(-(N-1)//2, N//2+1)

    h_fd = np.sinc(n - delay)
    h_fd *= np.hamming(N)
    h_fd /= np.sum(h_fd)

    delayed = np.convolve(samples, h_fd)

    return delayed


# ----------------------------
# 4. Frequency offset
# ----------------------------
def apply_frequency_offset(samples, fs=1e6, fo=1000):

    Ts = 1/fs
    t = np.arange(0, Ts*len(samples), Ts)

    samples_complex = samples.astype(np.complex128)

    shifted = samples_complex * np.exp(1j*2*np.pi*fo*t)

    return shifted


# ----------------------------
# 5. Mueller & Muller timing recovery
# ----------------------------
def mueller_muller(samples, sps):

    samples_interpolated = signal.resample_poly(samples, 16, 1)
    samples = samples_interpolated.copy()

    mu = 0
    out = np.zeros(len(samples) + 10, dtype=np.complex64)
    out_rail = np.zeros(len(samples) + 10, dtype=np.complex64)

    track_mu = np.zeros(len(out))

    i_in = 0
    i_out = 2

    while i_out < len(out) and i_in*16 + int(mu*16) < len(samples):

        out[i_out] = samples[i_in*16 + int(mu*16)]

        out_rail[i_out] = (
            int(np.real(out[i_out]) > 0)
            + 1j*int(np.imag(out[i_out]) > 0)
        )

        x = (out_rail[i_out] - out_rail[i_out-2]) * np.conj(out[i_out-1])
        y = (out[i_out] - out[i_out-2]) * np.conj(out_rail[i_out-1])

        mm_val = np.real(y - x)

        mu += sps + 0.3 * mm_val

        i_in += int(np.floor(mu))
        track_mu[i_in] = mu

        mu = mu - np.floor(mu)

        i_out += 1

    out = out[2:i_out]

    return out, track_mu


# ----------------------------
# 6. Plot results
# ----------------------------
def plot_results(bits, samples_rx, recovered_symbols, track_mu, sps):

    plt.figure()

    plt.subplot(3,1,1)
    plt.plot(bits)
    plt.title("Bit Stream")
    plt.ylabel("Bit")

    plt.subplot(3,1,2)
    plt.plot(np.real(samples_rx[60:-60]))
    plt.plot(np.imag(samples_rx[60:-60]))
    plt.title("RX Signal")
    plt.ylabel("Amplitude")

    plt.subplot(3,1,3)
    plt.plot(np.real(recovered_symbols[8:108]))
    plt.title("Recovered Symbols")
    plt.ylabel("Symbol Value")

    plt.tight_layout()
    plt.show()

    plt.figure()
    plt.plot(np.real(samples_rx[60:-60]))
    plt.scatter(
        np.arange(len(recovered_symbols[8:108]))*sps,
        np.real(recovered_symbols[8:108]),
        color='red'
    )
    plt.title("Timing Recovery Sampling Points")
    plt.show()

    nonzero_indices = np.where(track_mu != 0)[0]
    nonzero_mu = track_mu[nonzero_indices]

    plt.figure()
    plt.plot(nonzero_indices, nonzero_mu)
    plt.xlabel("Iteration")
    plt.ylabel("mu")
    plt.title("Timing Recovery: mu over Iterations")
    plt.grid(True)
    plt.show()


# ----------------------------
# Main pipeline
# ----------------------------
def main():

    num_symbols = 100
    sps = 8

    bits, pulse_train = generate_pulse_train(num_symbols, sps)

    tx_samples, _ = raised_cosine_filter(pulse_train, sps)

    delayed_samples = fractional_delay(tx_samples)

    freq_offset_samples = apply_frequency_offset(delayed_samples)

    recovered_symbols, track_mu = mueller_muller(freq_offset_samples, sps)

    plot_results(
        bits,
        freq_offset_samples,
        recovered_symbols,
        track_mu,
        sps
    )


if __name__ == "__main__":
    main()