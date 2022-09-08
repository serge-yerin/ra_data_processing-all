import numpy as np


def jds_header_new_channels_numbers(file_header, ifmin, ifmax, fft_size=None, n_avr=None):
    """
    returns .jds file header with correctly stored numbers of frequency channels
    usually is useful when while processing the last 4 channels where time info is stored are deleted
        file_header - input file header read from file (bytes)
        ifmin - number of the lowest frequency channel (int)
        ifmax - number of the highest frequency channel (int)
    returns:
        file_header - corrected file header (bytes)
    """

    file_header = bytearray(file_header)
    if fft_size is not None:
        file_header[574:578] = np.int32(fft_size).tobytes()  # FFT size place in header
    file_header[624:628] = np.int32(ifmin).tobytes()
    file_header[628:632] = np.int32(ifmax).tobytes()
    file_header[632:636] = np.int32(ifmax - ifmin).tobytes()
    if n_avr is not None:
        file_header[636:640] = np.int32(n_avr).tobytes()  # n_avr place in header
    file_header = bytes(file_header)
    return file_header
