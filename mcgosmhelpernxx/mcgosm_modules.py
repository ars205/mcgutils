"""
mcgosm functions.
"""

import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import json
import os
import xml.etree.ElementTree as ET
import requests
import time
import math


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


def divide_area_into_voronoi_cells(x_min, y_min, x_max, y_max, points=None, k=None, plot=False):
    """
    Divides the rectangular area defined by the given coordinates into arbitrary non-overlapping voronoi cells.

    Args:
        x_min (float): The minimum x-coordinate of the rectangular area.
        y_min (float): The minimum y-coordinate of the rectangular area.
        x_max (float): The maximum x-coordinate of the rectangular area.
        y_max (float): The maximum y-coordinate of the rectangular area.
        points (list): A list of tuples representing the points as (x, y) coordinates.
        k (int): The number of points to generate if points are not given.
        plot(bool): Whether to plot the voronoi cells or not (default: False)

    Returns:
        A list of lists representing the voronoi cells as a list of (x, y) coordinates.
    """

    # If points are not given, generate k random points
    if points is None:
        points = generate_random_points_in_area(x_min, y_min, x_max, y_max, k)

    # Create the voronoi diagram
    vor = Voronoi(points)

    # Plot the voronoi diagram
    if plot:
        # Plot the points
        plt.plot(np.array(points)[:, 0], np.array(points)[:, 1], 'ko')
        # Plot the voronoi diagram
        voronoi_plot_2d(vor)
        # Index the points
        for i, point in enumerate(points):
            plt.text(point[0], point[1], i)
        plt.show()

    # Get the voronoi cells
    voronoi_cells = vor.regions

    # Remove the infinite voronoi cells
    #voronoi_cells = [voronoi_cell for voronoi_cell in voronoi_cells if -1 not in voronoi_cell]

    # Return also the coordinates of each cell
    voronoi_cells = [vor.vertices[voronoi_cell] for voronoi_cell in voronoi_cells]

    return voronoi_cells


def generate_random_points_in_area(x_min, y_min, x_max, y_max, k):
    """
    Generates K random points within the rectangular area defined by the four points a, b, c, and d.

    Args:
        k (int): The number of random points to generate.
        
    Returns:
        A list of tuples representing the randomly generated points as (x, y) coordinates.
    """

    # Generate K random points within the rectangular area
    x_vals = np.random.uniform(x_min, x_max, k)
    y_vals = np.random.uniform(y_min, y_max, k)
    points = np.column_stack((x_vals, y_vals))

    return points

def read_points_from_json(json_file):
    """
    Reads the points from a JSON file.

    Args:
        json_file (str): The path to the JSON file.
        
    Returns:
        A list of tuples representing the points as (x, y) coordinates.
    """
    with open(json_file) as f:
        data = json.load(f)
    points = []
    for point in data['points']:
        points.append((point['latitude'], point['longitude']))
    return np.array(points)


def is_point_in_areas(point, areas):
    """
    Checks if a point is within a list of areas.

    Args:
        point (tuple): The point as (x, y) coordinates.
        areas (list): A list of areas as (x_min, y_min, x_max, y_max).
        
    Returns:
        True if the point is within one of the areas, False otherwise.
    """
    for ar in areas:
        x_min, y_min, x_max, y_max = ar
        if x_min <= point[0] <= x_max and y_min <= point[1] <= y_max:
            return True
    return False


# Define a function that downloads osm map based on x_min, x_max, y_min, y_max
def download_osm_map(x_min, y_min, x_max, y_max, filename):
    """
    Downloads an OSM map based on the given coordinates.

    Args:
        x_min (float): The minimum x-coordinate of the rectangular area.
        y_min (float): The minimum y-coordinate of the rectangular area.
        x_max (float): The maximum x-coordinate of the rectangular area.
        y_max (float): The maximum y-coordinate of the rectangular area.
        filename (str): The name of the file to save the map to.
    """
    # Define the bounding box coordinates for the area you want to download
    west, south, east, north = x_min, y_min, x_max, y_max

    # Send a GET request to the OSM API to download the map data
    url = f"https://api.openstreetmap.org/api/0.6/map?bbox={west},{south},{east},{north}"
    response = requests.get(url)

    # Save the map data to a file
    with open(filename, 'w') as f:
        f.write(response.content.decode('utf-8'))
