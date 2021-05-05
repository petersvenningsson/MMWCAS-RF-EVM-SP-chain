import os
import json

import numpy as np

from utils import calibrate

def read_binary(i_frame, path, config):
    """ Reads IQ sampled data from one cascade capture device.
        Returns ADC_samples: shape (chirp_samples, n_chirps, n_capture_transmitters, n_receivers)
    """

    factors = [config['numSamplePerChirp'], config['numChirpsPerFrame'], config['NumRXPerDevice']]
    samples_per_frame = np.prod(factors) * 2

    with open(path, 'rb') as f:
        f.seek(i_frame * samples_per_frame * np.uint16(1).nbytes)
        ADC_data = np.fromfile(f, dtype=np.int16, count = samples_per_frame)
    real = ADC_data[0::2]
    imaginary = ADC_data[1::2]
    ADC_complex = real + 1j*imaginary 

    n_chirps_per_loop = int(config['numChirpsPerFrame']/config['nchirp_loops'])
    shape = (config['NumRXPerDevice'], config['numSamplePerChirp'], n_chirps_per_loop, config['nchirp_loops'])
    data_cube = np.reshape(ADC_complex, shape, order='F').transpose((1, 3, 0, 2))

    return data_cube


def process_ADC(i_frame, files, path, config):
    """ Returns time domain data cube of i_frame. Antenna and cascade capture board parameters are 
    defined by config. 
        Returns ADC_samples: shape (chirp_samples, n_chirps, n_virtual_antennas)
    """

    ADC_samples = []
    for chip in config['Primary/Replica']:
        filename = next(filter(lambda x: 'data' in x, files[chip]))
        ADC_samples.append(read_binary(i_frame, os.path.join(path, filename), config))
    ADC_samples = np.concatenate(ADC_samples, axis = 2)

    # Calibration
    if config["adcCalibrationOn"]:
        ADC_samples = calibrate(ADC_samples, config)
    
    # Rx ordering
    channel_order = list(map(lambda x:x-1, config['RxForMIMOProcess']))
    ADC_samples = ADC_samples[:,:, channel_order,:]

    # Virtual array channel ordering
    virtual_array_shape = (config['numSamplePerChirp'], config['nchirp_loops'], config['numRxToEnable'] * config['numTxToEnable'])
    ADC_samples = ADC_samples.reshape((virtual_array_shape), order='F')
    channel_order = list(map(lambda x:x-1, config['ChannelOrder']))
    ADC_samples = ADC_samples[:,:, channel_order]

    return ADC_samples


def get_frame(i_frame, path, path_config):
    """ Returns one frame from the data capture stored in directory path.
    """

    with open (path_config) as f:
        config = json.load(f)
    
    content = os.listdir(path)
    files = {}
    for chip in config['Primary/Replica']:
        files[chip] = list(filter(lambda x: chip in x, content))
    
    data_cube = process_ADC(i_frame, files, path, config)
    return data_cube


if __name__ == '__main__':
    path = './cascade_capture_raw'
    path_config = './config/config.json'
    i_frame = 1
    get_frame(i_frame, path, path_config)
    