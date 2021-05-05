import numpy as np
from scipy.fft import fft, fftshift
from scipy.signal import hann


def beamforming(frame):
    """ Perform basic digital beamforming.
    """
    # range FFT
    window = hann(frame.shape[0])
    window = np.expand_dims(window, axis = (1, 2)).repeat(frame.shape[1], axis=1).repeat(frame.shape[2], axis=2)
    frequencies_cube = fft(frame * window, axis=0)

    # Doppler FFT
    window = hann(frame.shape[1])
    window = np.expand_dims(window, axis = (0, 2)).repeat(frame.shape[0], axis=0).repeat(frame.shape[2], axis=2)
    frequencies_cube = fftshift(fft(frequencies_cube * window, axis=1), axes=(1,))

    # DOA FFT
    window = hann(frame.shape[2])
    window = np.expand_dims(window, axis = (0, 1)).repeat(frame.shape[0], axis=0).repeat(frame.shape[1], axis=1)
    frequencies_cube = fftshift(fft(frequencies_cube * window, axis=2), axes=(2,))

    return frequencies_cube