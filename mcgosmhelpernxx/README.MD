# MCGOsmHelperNXX

## Overview

`MCGOsmHelperNXX` is a Python tool to provide a convinient way to loading geo-data from the OpenStreetMap (OSM) when considering a greater geographical area (e.g. a city). The aim is to simplify the process of obtaining, structuring, and analyzing spatial data to be used for a ray-tracer.

## Features

- **Geo Data Retrieval**: Fetch data for a specified area based on defined latitude and longitude.
- **Area Segmentation**: The tool divides the defined area into a user-specified number of sub-areas.
- **Grid Cell Division**: Each sub-area is further divided into grid cells. The center of each cell serves as a point of interest. You can also divide into Voronoi cells.
- **Base Stations**: Generate random BS locations in the defined area or import base station coordinates from a JSON file. The number of base stations per area is also customizable.
- **Command Line Interface**: Accessible/Adjustable via a command line interface.

## Limitations

`MCGOsmHelperNXX` is only for research purposes and isin development stages. As such, there might be limitations or bugs that have not yet been addressed. It is advised while utilizing the tool for research or large-scale tasks, to investigate the code. Feedback and contributions to improve the functionalities are much appreciated.

## Installation

1. Clone the repository or download the source code from [GitHub](https://github.com/ars205/mcg-tools/mcgosmhelpernxx).

2. Navigate to the package directory:
   ```bash
   cd mcgosmhelpernxx
   ```
3. Install the package and its dependencies using pip in development mode:
    ```bash
    pip install -e .
    ```

## Usage
        cd mcgosmhelpernxx

After installation, you can run the package with:
```shell
mcgosmhelpernxx --area_name 'YourAreaName' --x_min min_longitude --x_max max_longitude --y_min min_latitude --y_max max_latitude
```
Example:
```shell
mcgosmhelpernxx --area_name 'Vienna' --x_min 16.2 --x_max 16.5 --y_min 48.1 --y_max 48.3
```

For detailed information about available command-line:
```shell

usage: mcgosmhelpernxx [-h] [--area_name AREA_NAME] [--x_min X_MIN]
                       [--x_max X_MAX] [--y_min Y_MIN] [--y_max Y_MAX]
                       [--num_areas NUM_AREAS] [--num_cells NUM_CELLS]
                       [--num_base_stations NUM_BASE_STATIONS]
                       [--base_stations_file BASE_STATIONS_FILE]
                       [--output_dir OUTPUT_DIR] [--help_options]```
mcgosmhelpernxx --help_options
```

## License
`MCGOsmHelperNXX` is licensed under the MIT [license](LICENSE).

## Check research work
```shell
website: https://artansalihu.com/
```