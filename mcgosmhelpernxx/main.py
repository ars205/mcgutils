import argparse
import sys
import time
from retrieve_geo_data import retrieve_geo_data

def main():
    parser = argparse.ArgumentParser(f'Retrieve a grid of sub-areas and base stations in the area')
    parser.add_argument('--area_name', type=str, default='Vienna222', help='Name of the area')
    parser.add_argument('--x_min', type=float, default=16.3157, help='Minimum longitude')
    parser.add_argument('--x_max', type=float, default=16.4362, help='Maximum longitude')
    parser.add_argument('--y_min', type=float, default=48.1663, help='Minimum latitude')
    parser.add_argument('--y_max', type=float, default=48.2275, help='Maximum latitude')
    parser.add_argument('--k', type=int, default=2, help='Number of sub-areas (bizirks) to divide the area into kxk sub-areas')
    parser.add_argument('--grid_size', type=int, default=4, help='Number of grid cells to divide each sub-area into grid_size x grid_size grid cells. The center of each grid cell will be a point of interest.')
    parser.add_argument('--generate_random_bs', type=bool, default=False, help='Generate random base stations')
    parser.add_argument('--read_bs_from_file', type=bool, default=False, help='Read the BS coordinates from a JSON file')
    parser.add_argument('--num_points_per_grid_cell', type=int, default=2, help='Number of points per grid cell.')
    parser.add_argument('--num_bs_per_area', type=int, default=1, help='Number of base stations per area')
    parser.add_argument('--help_options', action='store_true', help='Print options')
    # Parse the arguments
    args = parser.parse_args()
    # Print the available options if requested
    if args.help_options:
        parser.print_help()
        sys.exit()
    # if args.verbose:
    #     print("Verbose enabled")
    # Run the main function with the arguments    
    start_time = time.time()
    retrieve_geo_data(args)
    print("--- %s minutes ---" % ((time.time() - start_time)/60))    


if __name__ == '__main__':
    main()