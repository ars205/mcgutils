# MIT License

# Copyright (c) 2023 MCG - Artan Salihu

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


bl_info = {
    "name": "MCG OSM Helper Tool Blender Script",
    "author": "MCG - Artan Salihu",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Tool > OSM Export",
    "description": "Export OSM data to STL",
    "warning": "",
    "wiki_url": "https://mcg-deep-wrt.netlify.app/deep-wrt/utilities/",
    "category": "MCG-Tools",
}

import bpy

import pip
#pip.main(['install', 'tqdm', '--user'])
#pip.main(['install', 'matplotlib', '--user'])
#pip.main(['install', 'numpy', '--user'])
#pip.main(['install', 'scipy', '--user'])
#pip.main(['install', 'osmnx', '--user'])
#pip.main(['install', 'shapely', '--user'])
#pip.main(['install', 'requests', '--user'])
#pip.main(['install','argparse', '--user'])

import numpy as np
import json
import os
import argparse
#import osmnx as ox
#import shapely.geometry as sg
import time
import sys



#from wrt_modules.utils import divide_area_into_grid

def divide_area_into_grid(x_min, y_min, x_max, y_max, k, plot=False):
    """
    Divides the rectangular area defined by the given coordinates into (k x k) arbitrary non-overlapping squares.
    
    Args:
        x_min (float): The minimum x-coordinate of the rectangular area.
        y_min (float): The minimum y-coordinate of the rectangular area.
        x_max (float): The maximum x-coordinate of the rectangular area.
        y_max (float): The maximum y-coordinate of the rectangular area.
        k (int): The number of sub_areas to divide the area into (k x k)
        plot(bool): Whether to plot the sub_areas or not (default: False
        
    Returns:
        A list of tuples representing the squares as (x_min, y_min, x_max, y_max).
    """
    # Calculate the size of each square
    x_step = (x_max - x_min) / k
    y_step = (y_max - y_min) / k

    # Create the sub_areas
    squares = []
    for i in range(k):
        for j in range(k):
            x_start = x_min + i * x_step
            y_start = y_min + j * y_step
            x_end = x_min + (i + 1) * x_step
            y_end = y_min + (j + 1) * y_step
            squares.append((x_start, y_start, x_end, y_end))
    
    # Plot the squares
    if plot:
        for square in squares:
            x_start, y_start, x_end, y_end = square
            plt.plot([x_start, x_end, x_end, x_start, x_start], [y_start, y_start, y_end, y_end, y_start])
        # Index squares
        for i, square in enumerate(squares):
            x_start, y_start, x_end, y_end = square
            plt.text(x_start + (x_end - x_start) / 2, y_start + (y_end - y_start) / 2, i)
        plt.show()

    return squares



def blender_osm_export_stl(args):
    """
    1. x_min: The minimum x-coordinate of the rectangular area.
    2. y_min: The minimum y-coordinate of the rectangular area.
    3. x_max: The maximum x-coordinate of the rectangular area.
    4. y_max: The maximum y-coordinate of the rectangular area.
    5. area_name: The name of the area to create a folder for the data in Results folder.
    6. k: The number of sub_areas to divide the area into (k x k)
    7. grid_size: The number of grid cells to divide each sub-area into (grid_size x grid_size)
    8. osm_file: The name of the OSM file to be used for the export.
    9. scene_name: The name of the scene in Blender.

    I-It creates a folder in Results/area_name_blen folder and saves the STL files in it.

    II-It also creates a JSON file in the same folder with the name grid_cells.json which contains the grid cells of the area.

    III-Also reads the grid_cells.json file and returns the grid_cells dictionary.
    
    Args:
        args: The arguments to the function.

    Returns:
        grid_cells: The grid cells of the area.
        .stl files: The STL files of the OSM data.

    """
    # Input the area x_min, x_max, y_min, y_max
    x_min = args.x_min # min longitude
    y_min = args.y_min # min latitude
    x_max = args.x_max # max longitude 
    y_max = args.y_max # max latitude

    # Name of the Area to create a folder for the data in Results folder
    area_name = args.area_name

    # Input the number of sub-areas to divide the area into kxk sub-areas
    k = args.k

    # Define the rectangular into k sub-areas
    bizirk = divide_area_into_grid(x_min, y_min, x_max, y_max, k, plot=False)

    # Divide the sub-areas into grid cells and store grid cells in a dictionary with the key being the area number
    grid_cells = {}
    for i, ar in enumerate(bizirk):
        x_min, y_min, x_max, y_max = ar
        if args.grid_size > 0:
            grid_cells[i] = divide_area_into_grid(x_min, y_min, x_max, y_max, args.grid_size, plot=False)
        else:
            grid_cells[i] = [ar]

    # Create now folders for blender Results/area_name_blen folder
    # If user has not specified a directory, create a default directory in Desktop
    if args.d_file_path == None:
        home = os.path.expanduser("~")
        args.d_file_path = os.path.join(home, "Desktop", "Results")
    if not os.path.exists(args.d_file_path):
        os.makedirs(args.d_file_path,mode = 777 )
    if not os.path.exists(args.d_file_path):
        os.makedirs(args.d_file_path,mode = 777 )
    if not os.path.exists(args.d_file_path + f'/{area_name}'):
        os.makedirs(args.d_file_path + f'/{area_name}')

    with open(args.d_file_path + f'/{area_name}' + '/grid_cells.json', 'w') as fp:
        json.dump(grid_cells, fp)
    
    with open(args.d_file_path + f'/{area_name}' + '/grid_cells.json', 'r') as fp:
        grid_cells = json.load(fp)

    grid_cells_new = {int(k): v for k, v in grid_cells.items()}

    for k, v in grid_cells_new.items():
        print(f'"Bizirk" or sub-area {k} of {area_name} has {len(v)} grid cells')

        for i, ar in enumerate(v):
            min_lon, min_lat, max_lon, max_lat = ar
            print(f'Grid cell {i} of sub-area {k} has coordinates: {min_lon, min_lat, max_lon, max_lat}')

            # Paste into blosom the coordinates of the grid cell
            bpy.data.scenes[args.scene_name].blosm.minLon = min_lon
            bpy.data.scenes[args.scene_name].blosm.minLat = min_lat     
            bpy.data.scenes[args.scene_name].blosm.maxLon = max_lon
            bpy.data.scenes[args.scene_name].blosm.maxLat = max_lat 

            print(args.d_file_path)


            # First, get terrain data
                    # 1.0 Firs, terrain data:
            bpy.context.scene.blosm.dataType = 'terrain'
            bpy.ops.blosm.import_data()
            print("Terrain data loaded from ArcGIS")
            
            # Export to Collada only terrain
            bpy.ops.wm.collada_export(filepath=args.d_file_path + f'/{area_name}/{k}_{i}_terrain.dae')

            # Switch to OSM

            bpy.context.scene.blosm.dataType = 'osm'

            # ---- Collada ---- #

            bpy.data.scenes[args.scene_name].blosm.mode = '3Dsimple'
            bpy.data.scenes[args.scene_name].blosm.buildings = True
            bpy.data.scenes[args.scene_name].blosm.water = False
            bpy.data.scenes[args.scene_name].blosm.highways = False
            bpy.data.scenes[args.scene_name].blosm.forests = False
            bpy.data.scenes[args.scene_name].blosm.vegetation = False
            bpy.data.scenes[args.scene_name].blosm.railways = False

            bpy.ops.blosm.import_data() # Import buildings

            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')

            # Select objects with ".osm_buildings" in their name
            for obj in bpy.context.scene.objects:
                if ".osm_buildings" in obj.name:
                    obj.select_set(True)

            bpy.ops.wm.collada_export(filepath=args.d_file_path + f'/{area_name}/{k}_{i}_buildings.dae', selected=True) # Export buildings

            # bpy.data.scenes[args.scene_name].blosm.buildings = False
            # bpy.data.scenes[args.scene_name].blosm.water = False
            # bpy.data.scenes[args.scene_name].blosm.highways = False
            # bpy.data.scenes[args.scene_name].blosm.forests = False
            # bpy.data.scenes[args.scene_name].blosm.vegetation = False
            # bpy.data.scenes[args.scene_name].blosm.railways = True

            # bpy.ops.blosm.import_data() # Import railways

            # # Deselect all objects
            # bpy.ops.object.select_all(action='DESELECT')

            # # Select objects that contain "railway"
            # for obj in bpy.context.scene.objects:
            #     if "railway" in obj.name:
            #         obj.select_set(True)

            # bpy.ops.wm.collada_export(filepath=args.d_file_path + f'/{k}_{i}_railway.dae', selected=True) # Export buildings
            
            # ---- STL ----
            # Select all objects
            bpy.ops.object.select_all(action='SELECT')
            # Export to stl and give a complete filename
            bpy.ops.export_mesh.stl(filepath=args.d_file_path + f'/{area_name}/{k}_{i}.stl')

            # --- Next grid cell ---

            # Select all objects
            bpy.ops.object.select_all(action='SELECT')

            # Delete selected objects
            bpy.ops.object.delete()
            
            print("HERE")

            # Pause the script for 30 seconds
            
if __name__ == '__main__':
    # Run the main function
    parser = argparse.ArgumentParser(f'Retrieve a grid of sub-areas and base stations in the area')
    parser.add_argument('--area_name', type=str, default='Vienna_Model_22', help='Name of the area')
    parser.add_argument('--x_min', type=float, default=16.3157, help='Minimum longitude')
    parser.add_argument('--x_max', type=float, default=16.4362, help='Maximum longitude')
    parser.add_argument('--y_min', type=float, default=48.1663, help='Minimum latitude')
    parser.add_argument('--y_max', type=float, default=48.2275, help='Maximum latitude')
    parser.add_argument('--k', type=int, default=2, help='Number of sub-areas (bizirks) to divide the area into kxk sub-areas')
    parser.add_argument('--grid_size', type=int, default=2, help='Number of grid cells to divide each sub-area into grid_size x grid_size grid cells. The center of each grid cell will be a point of interest.')
    parser.add_argument('--d_file_path', type=str, default= None, help='Path to the folder where the stl files will be saved. If None, then default is C:/Users/Desktop/Results. You MUST have the absolute path here. Otherwise data are stored in Blender folder.')
    parser.add_argument('--scene_name', type=str, default='Scene', help='Name of the scene in blender. Default is Scene')
    parser.add_argument('--help_options', action='store_true', help='Print options')
    # Parse the arguments
    args = parser.parse_args()
    # Print the available options if requested
    if args.help_options:
        parser.print_help()
        sys.exit()
    # if args.verbose:
    #     print("Verbose enabled")
    start_time = time.time()
    blender_osm_export_stl(args)
    print("--- %s minutes ---" % ((time.time() - start_time)/60))

