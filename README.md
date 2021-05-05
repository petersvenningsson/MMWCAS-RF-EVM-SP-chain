# MMWCAS-RF-EVM-SP-chain
![](https://img.shields.io/badge/python-v3.7-blue) ![](https://shields.io/badge/license-Apache-blue) ![](https://img.shields.io/badge/SP-Radar-brightgreen)


Utilities for the SP chain on the TI MMWCAS-RF cascade MIMO evaluation module.

Entry points are generators `iterframes()` and `iterframes_processed` in process.py which returns the frames of the virtual array.

Example data is found in 

    ./cascade_capture_raw/

### Configuration

The configuration of the radar and capture boards are found in

    ./config/config.json

### Calibration

The radar is calibrated with regards to the test case stored in

    ./config/calibration

More information on the calibration process can be found in the [user manual](https://software-dl.ti.com/ra-processors/esd/MMWAVE-STUDIO/latest/exports/mmwave_studio_cascade_user_guide.pdf).
