# Remcom Ray-Tracing RIS Channel Analysis Scripts

## Overview

Here are a bunch of utils that aim to streamline and automate the process of modelling and running reconfigurable intelligent surfaces (RIS) scenarios using Remcom's ray-tracer. The process involves RIS radiation pattern design, creation and setup of Wireless InSite (WI) study areas, running simulations over multiple parameters, reading and storing path-traces, and analyzing certain outputs.

## Features

The utils included in here are:

1. **MCGCst2UanConverter.py**: Converts the CST pattern format into a UAN (Optional). Can also use the MCGCst2UanConverter.m script to convert a single file.

2. **MCGRemcom.py**: Automates the design and creation of a WI study area and setup file for a given model (only X3D is supported). Runs the simulation using `wibatch.exe`.

3. **MCGReadRemcomPaths.py**: Has methods for reading path-related information and received power from the output files of the simulations.

## Limitations

- Check dependencies.
- Only X3D models are supported.
- License for WI is required. 
- Check the version of WI you're using. The scripts were tested with WI 3.3.5, and 3.4.4.11.
- Only specific variables can be swept over for automation. Check the `MCGRemcom.py` script for more details.

## Usage

### MCGCst2UanConverter.py

You can skip this step if you already have UAN files or if your use case does not involve modelling RIS or any other antenna type radiation patterns. 

Example usage:

```python
from MCGCst2UanConverter import MCGConvert_multiple_files

input_files = ['file1.txt', 'file2.txt']
output_files = ['file1.uan', 'file2.uan']

MCGConvert_multiple_files(input_files, output_files)
```

### MCGRemcom.py
WI study area and setup file for a given model, runs the simulation using wibatch.exe, and supports command line arguments based on the version of WI.

Example usage:
```python
python MCGRemcom.py --studyArea 03_Automate_WIS.Study_Zero.xml --setup 03_Automate_WIS.setup --wibatchLocation "C:\Program Files\Remcom\Wireless InSite 3.3.5\bin\calc\wibatch.exe" --licenseLocation 123@1.1.2.3 --baseVersion 3.3.3.5 --RISPatternRX ["RISPatternRX_1", "RISPatternRX_2", "RISPatternRX_3"] --RISPatternTX ["RISPatternTX_1", "RISPatternTX_2", "RISPatternTX_3"] --help_options
```

### MCGReadRemcomPaths.py
Once you have the outputs from the simulations, you can read path-related information and received power.
For example, to read received power from multiple .p2m files, you can use:
    
```python
from MCGReadRemcomPaths import read_p2m_power

file_list = [r'./A/A.power.t001_15.r014', r'./A 2/B.power.t001_15.r014']
received_pwer = read_p2m_power(file_list=file_list)
```

## Dependencies

- Python 3.6+
- Check other imports in the scripts.

### License

MIT License

### Contact
[Artan Salihu]([https](https://www.artansalihu.com/)). Check other [research](https://scholar.google.com/citations?hl=en&user=TyEotkkAAAAJ&view_op=list_works&sortby=pubdate) or more utils at [MCG](https://mcg-deep-wrt.netlify.app/deep-wrt/utilities/).


