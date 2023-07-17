# MCGOsmHelperBlend

## Overview

`MCGOsmHelperBlend` is a Python tool to provide a convinient way to loading geo-data from the OpenStreetMap (OSM) when considering a greater geographical area (e.g. a city). The aim is to simplify the process of obtaining, structuring, and analyzing spatial data to be used for a ray-tracer. The tool must be run from Blender scripting.

## Features

- **Geo Data Retrieval**: Exports OSM data as STL and Collada (DAE) files (terrain and buildings).
- **Area Segmentation**: The tool divides the defined area into a user-specified number of sub-areas.
- **Grid Cell Division**: Each sub-area is further divided into grid cells.
- **Command Line Interface**: Accessible/Adjustable via a command line interface.
- Plotting functionality to visualize the sub-areas (optional)

 
## Limitations

- Some required Python packages may not be pre-installed with Blender.
- Due to the division of the area into grid cells, some features may be split across multiple files.
- It relies on Blender OSM addon to load the OSM data.
- Currently, the script requires manual installation and configuration.

## Installation

1. Clone the repository or download the source code from [GitHub](https://github.com/ars205/mcg-tools/mcgosmhelperblend).

2. Navigate to the package directory:
   ```bash
   cd mcgosmhelperblend
   ```
3. Install the package and its dependencies using pip in development mode:
    ```bash
    pip install -e .
    ```

## Usage

The script must be run within Blender's scripting environment. Here are the steps to do so:

1. Open Blender and navigate to the scripting workspace. You can find this by clicking on the "Scripting" tab at the top of the Blender user interface.

2. Once in the scripting workspace, click "Open" to load the script file.

3. In the text editor window, navigate to the location of your Python script file (`script.py`) and click "Open Text Block" to load it into the editor.

4. With the script loaded, you will need to adjust the parameters at the top of the script. Here are the parameters you need to adjust:

   - `area_name`: Name of the area
   - `x_min`, `x_max`, `y_min`, `y_max`: Coordinates defining the area of interest.
   - `k`: Number of sub-areas (bizirks) to divide the area into (kxk).
   - `grid_size`: Number of grid cells to divide each sub-area into (grid_size x grid_size). The center of each grid cell will be a point of interest.
   - `d_file_path`: Path to the folder where the STL and DAE files will be saved. If None, the default is 'C:/Users/Desktop/Results'. You must provide the absolute path. Otherwise, data are stored in the Blender folder.
   - `scene_name`: Name of the scene in blender. Default is 'Scene'.
   - `help_options`: If True, the help options are printed.

5. Once you have adjusted the argument parameters, you can run the script by clicking the "Run Script" button in Blender.

**Note**: Make sure Blender's Python is able to import all the necessary packages. You might need to install some packages manually using `pip` and blend-osm add-on.


For detailed information about available command-line:
```shell

usage: Retrieve a grid of sub-areas and base stations in the area [-h] [--area_name AREA_NAME] [--x_min X_MIN]
                                                                  [--x_max X_MAX] [--y_min Y_MIN] [--y_max Y_MAX] 
                                                                  [--k K]
                                                                  [--grid_size GRID_SIZE] [--d_file_path D_FILE_PATH]
                                                                  [--scene_name SCENE_NAME] [--help_options]
```

## License
`MCGOsmHelperBlend` is licensed under the MIT [license](LICENSE).

## Check research work
```shell
website: https://artansalihu.com/
```