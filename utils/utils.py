import numpy as np
import scipy.io


def read_header(path):
    """ Reads the header and return the number of frames recorded.
    """

    with open(path, 'rb') as f:
        header = np.fromfile(f, dtype=np.uintc, count = 6)

    n_frames = header[3]
    return n_frames

def calibrate(ADC_samples, config):
    """ Calibrates the measurements to standardized recording found in config[calibrationfilePath]
    """

    calibration_parameters = scipy.io.loadmat(config['calibrationfilePath'])
    range_calibration = calibration_parameters['calibResult']['RangeMat'][0][0]
    peaks = calibration_parameters['calibResult']['PeakValMat'][0][0]

    transmitter_order = list(map(lambda x:x-1, config['TxToEnable']))
    Tx_ref = transmitter_order[0]

    calibrated_data = []
    for i_Tx, Tx in enumerate(transmitter_order):

        # Calculate frequency correction matrix
        frequency_calibration = ((range_calibration[Tx,:] - range_calibration[Tx_ref, 2]) * \
            config['fs_calib']/config['Sampling_Rate_sps'] * \
            config['chirpSlope']/config['Slope_calib'] *\
            2*np.pi / (config['numSamplePerChirp'] * config['calibrationInterp']))[np.newaxis, :]

        sample_indices = (np.array(range(config['numSamplePerChirp'])))[:, np.newaxis]
        correction = np.exp(1j * sample_indices @ frequency_calibration ).transpose((1,0))
        correction = correction[:,:, np.newaxis].repeat(config['nchirp_loops'], axis=2).transpose((1,2,0))

        # Calibrate data
        corrected_data = ADC_samples[:,:,:, i_Tx] * correction

        # Calculate phase correction matrix
        phase_calibration = peaks[Tx_ref, 0] / peaks[Tx,:]
        phase_calibration = (phase_calibration/np.abs(phase_calibration))[:,np.newaxis,np.newaxis]
        phase_calibration = phase_calibration.repeat(config['numSamplePerChirp'], axis=1).repeat(config['nchirp_loops'], axis=2).transpose((1,2,0))

        calibrated_data.append(corrected_data*phase_calibration)

    calibrated_array = np.stack(calibrated_data, axis = 3)
    return calibrated_array
