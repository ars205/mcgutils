import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import json
import os
import argparse
import osmnx as ox
import shapely.geometry as sg
import time
import sys

from mcgosm_modules import divide_area_into_grid, divide_area_into_voronoi_cells, generate_random_points_in_area, read_points_from_json, is_point_in_areas

# Change the name of main() to retrieve_geo_data() to run the code

def retrieve_geo_data(args):
    """
    Documentation of the function:
    This function retrieves the geo data from OpenStreetMap and stores the data in a JSON file.
    The data includes the coordinates of the base stations, the coordinates of the grid cells, the coordinates of the Voronoi cells, and the coordinates of the buildings.
    The data is stored in a JSON file in the Results folder.
    The JSON file is named as the area_name.
    The JSON file contains the following data:
        1. base_station_loca: The coordinates of the base stations
        2. grid_cells: The coordinates of the grid cells
        3. voronoi_cells: The coordinates of the Voronoi cells
        4. buildings: The coordinates of the buildings

    Args:
        args: The arguments passed to the function

    Returns:
        None
    """
    # Input the area x_min, x_max, y_min, y_max
    x_min = args.x_min
    y_min = args.y_min
    x_max = args.x_max
    y_max = args.y_max

    
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

    # Check whether to generate random base stations or read the BS coordinates from a JSON file
    generate_random_bs = args.generate_random_bs
    read_bs_from_file = args.read_bs_from_file
    if generate_random_bs:
        read_bs_from_file = False

    # Generate random base_station_points in each square or read the BS coordinates from a JSON file
    if generate_random_bs:
        base_station_loca = []
        for ar in bizirk:
            x_min, y_min, x_max, y_max = ar
            base_station_loca.extend(generate_random_points_in_area(x_min, y_min, x_max, y_max, k=args.num_bs_per_area))
    elif read_bs_from_file:
        base_station_loca = read_points_from_json('bs_coordinates.json')
    else:
        # base_station_loca is the center of each grid cell
        base_station_loca = []
        for i, ar in enumerate(bizirk):
            for j, cell in enumerate(grid_cells[i]):
                x_min, y_min, x_max, y_max = cell
                base_station_loca.append(((x_min + x_max) / 2, (y_min + y_max) / 2))

    # Filter only the base_station_points that are within the sub-areas/areas
    base_station_loca = [bs_loc for bs_loc in base_station_loca if is_point_in_areas(bs_loc, bizirk)]  

    # Convert the base_station_loca to a dictionary with the key being the area number
    # and the value being a list of base stations in that area
    base_station_loca_dict = {}
    for i, ar in enumerate(bizirk):
        base_station_loca_dict[i] = []
        for bs_loc in base_station_loca:
            if is_point_in_areas(bs_loc, [ar]):
                base_station_loca_dict[i].append(bs_loc)

    # Save a plot with areas, base stations and grid cells to a filename with the extension .png
    fig, ax = plt.subplots()
    for i, ar in enumerate(bizirk):
        x_min, y_min, x_max, y_max = ar
        ax.add_patch(plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, fill=False))
        ax.text((x_min + x_max) / 2, (y_min + y_max) / 2, str(i), ha='center', va='center', fontsize=20)
    for i, ar in enumerate(bizirk):
        for j, cell in enumerate(grid_cells[i]):
            x_min, y_min, x_max, y_max = cell
            ax.add_patch(plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, fill=False))
            ax.text((x_min + x_max) / 2, (y_min + y_max) / 2, str(i) + '_' + str(j), ha='center', va='center', fontsize=20)
    if len(base_station_loca) > 0:
        # Plot the base stations and show the name of the base station
        plt.plot(np.array(base_station_loca)[:, 0], np.array(base_station_loca)[:, 1], 'ko')
    # Else plot the base stations in the center of each grid cell
    else:
        for i, ar in enumerate(bizirk):
            for j, cell in enumerate(grid_cells[i]):
                x_min, y_min, x_max, y_max = cell
                plt.plot((x_min + x_max) / 2, (y_min + y_max) / 2, 'ko')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Areas')
    # Save the figure to a Results/area_name folder
    if not os.path.exists('Results'):
        os.makedirs('Results')
    if not os.path.exists('Results/' + area_name):
        os.makedirs('Results/' + area_name)
    plt.savefig(f'Results/' + area_name + '/'+area_name+'.png')
    #plt.show()
    # close the figure
    plt.close()

    # Save grid_cells dictionary to a JSON file
    with open('Results/' + area_name + '/grid_cells.json', 'w') as fp:
        json.dump(grid_cells, fp)
    
    # Read the grid_cells dictionary from a JSON file
    with open('Results/' + area_name + '/grid_cells.json', 'r') as fp:
        grid_cells = json.load(fp)

    grid_cells_new = {int(k): v for k, v in grid_cells.items()}

    for k, v in grid_cells_new.items():
        print(f'"Bizirk" or sub-area {k} of {area_name} has {len(v)} grid cells')

    # For each grid cell get center coordinates and get the geometries of buildings and railway from OSM (nodes-edges)
    grid_cell_centers = {}
    for k, v in grid_cells_new.items():
        grid_cell_centers[k] = []
        j = 0
        for cell in v:
            x_min, y_min, x_max, y_max = cell
            grid_cell_centers[k].append(((y_min + y_max) / 2, (x_min + x_max) / 2))
            dist = 300

            # grid_cell_centers[k][0] in the format of (longitude, latitude)

            #Get tag info on building and railway
            tags = {'building':True, 'railway':True, 'highway':True, 'amenity':True}

            #Get geometries of buildings and railway (nodes-edges)
            bbox = ox.utils_geo.bbox_from_point(grid_cell_centers[k][j], dist=dist)
            print(bbox)

            # Get graph from point
            #graph_from_point = ox.graph_from_point(grid_cell_centers[k][j], dist=dist,retain_all=True)
            #fig, ax = ox.plot_graph(graph_from_point, node_size=0, node_color='k', node_edgecolor='gray', node_zorder=2, edge_color='#999999', edge_linewidth=1, edge_alpha=1, bgcolor='k')
            gdf_geometries = ox.geometries_from_point(grid_cell_centers[k][j], tags, dist)

            # Print sub-area number, grid cell number and point number
            print(f'Area {k}, Grid cell {j}, Point {grid_cell_centers[k][j]}')

            gdf_proj = ox.project_gdf(gdf_geometries, to_latlong=True)

            # Change longitude and latitude to latitute and longitude for gdf geometry type Point
            #gdf['geometry'] = gdf['geometry'].apply(lambda x: Point(x.y, x.x))
            
            # If building:levels is a column in the gdf_proj dataframe, then use it to calculate the height of each building
            if "building:levels" in gdf_proj.columns:
                # Get the number of levels for each building from the building:levels column
                levels = gdf_proj["building:levels"]
                # Make all levels with Nan values 0
                levels = levels.fillna(0+1e-5)
                # Convert levels to integers
                levels = levels.astype(int)
                # Add a column to gdf_proj with the height of each building calculated from the number of levels for each building * 3.5
                gdf_proj['height'] = levels * 3.5
                # Convert to float
                gdf_proj['height'] = gdf_proj['height'].astype(float)

                # Print the heigh of 11 buildings with the highest height
                print(gdf_proj.sort_values(by='height', ascending=False)['height'][:11])
                # For each building, update polygon geometry to a 3D polygon with height information
                for i, row in gdf_proj.iterrows():
                    height = row['height']
                    if height >= 0.:
                        if row['geometry'].geom_type == 'Polygon':
                            polygon = row['geometry']
                            # Create a 3D polygon from the 2D polygon and the height
                            gdf_proj.at[i, 'geometry'] = sg.Polygon([(p[0], p[1], height) for p in polygon.exterior.coords])
            

            #Save the figure to a Results/area_name and Results/area_name/grid_cells_area_name folder
            if not os.path.exists('Results/' + area_name + '/grid_cells_images'):
                os.makedirs('Results/' + area_name + '/grid_cells_images')

            #Create a figure with yellow colors on buildings
            if "building" in gdf_proj.columns:
                fig1, ax = ox.plot_footprints(gdf_proj, ax = None, figsize=(10, 10), color='yellow', edge_linewidth=2, bgcolor='#333333', save=False, show=False, close=False, dpi=600)
                fig1.savefig(f'Results/' + area_name + '/grid_cells_images/' + str(k) + '_' + str(j) + '.png', dpi = 600)
                # Close the figure  
                plt.close(fig1)
            else:
                # save a blank figure, with background color black
                fig1 = plt.figure(figsize=(10, 10), facecolor='#333333')
                fig1.savefig(f'Results/' + area_name + '/grid_cells_images/' + str(k) + '_' + str(j) + '.png', dpi = 600)
                # Close the figure
                plt.close(fig1)

            # Save the gdf_proj dataframe to a GeoJSON file
            if not os.path.exists('Results/' + area_name + '/grid_cells_geojson'):
                os.makedirs('Results/' + area_name + '/grid_cells_geojson')
            with open ('Results/' + area_name + '/grid_cells_geojson/' + str(k) + '_' + str(j) + '.geojson', 'w') as f:
                f.write(gdf_proj.to_json())
            j += 1
