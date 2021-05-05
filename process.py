import os

from utils import get_frame, read_header, beamforming


def iterframes(path, path_config):
    """ Returns a generator of frames in the time domain.
    """
    master_file = next(filter(lambda x: 'master' in x and 'idx' in x, os.listdir(path)))
    n_frames = read_header(os.path.join(path, master_file))
    for i_frame in range(n_frames):
        yield get_frame(i_frame, path, path_config)


def iterframes_processed(path, path_config):
    """ Returns a generator of frames in the frequency domain.
    """
    for frame in iterframes(path, path_config):
        yield beamforming(frame)


if __name__ == '__main__':
    path = './cascade_capture_raw/'
    path_config = './config/config.json'

    for f, processed_frame in enumerate(iterframes_processed(path, path_config)):
        print(f'Processed frame {f} of shape {processed_frame.shape}')
