#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    30574 Earth observations for monitoring changes (EO4Change) exercise with Sentinel-5P.
    Make and show Sentinel-5P Level-3 product.
"""

# -- File info -- #
__author__ = ['Andreas R. Stokholm']
__copyright__ = ['A. Stokholm']
__contact__ = ['andreas_stokholm@hotmail.com']
__version__ = '0.0.1'
__date__ = '2022-06-06'

# -- Built-in modules -- #
import os

# -- Third-party modules -- #
import cartopy.crs as ccrs
import harp
import matplotlib.pyplot as plt
import numpy as np

# -- Proprietary modules -- #
from s5p_get import SENTINELSAT_OPTIONS


# -- Read here -- #
# In this final part of the exercise, you will create a level-3 product using multiple level-2 products.
# To help us with aligning pixels across measurements, we utilize the HARP package through a Python interface.
# This exercise is more complex than the previous. The first function (harp_process) carries out the HARP processing.
# No need to make adjustments here. The required adjustments are in the start and end of main().
# Make sure to read the comments. :)
# You can find documentation on HARP @ https://stcorp.github.io/harp/doc/html/index.html
# Remember to send me your images. :) stokholm@space.dtu.dk


def harp_process(filename: str, harp_product_name: str, qa_validity, data_dir: str, grid: tuple,
                 lat_min: float, lat_max: float, lon_min: float, lon_max: float):
    # This function processes S5P files using HARP. Each file is processed.
    try:  # Catches HARP no data error. In case of this error, the except section will run.

        # HARP gets a file directory and a string containing operations. What is in keep() will be returned.
        harp_data = harp.import_product(data_dir + '/' + filename,
                                        operations=f"{harp_product_name}>{qa_validity}; \
                                        latitude > {lat_min} [degree_north]; \
                                        latitude < {lat_max} [degree_north]; \
                                        longitude > {lon_min} [degree_east]; \
                                        longitude < {lon_max} [degree_east]; \
                                        bin_spatial{str(grid)}; \
                                        keep(latitude_bounds,longitude_bounds,{harp_product_name}) ")

        # Unpack harp_data.
        values = harp_data[harp_product_name].data.squeeze()
        lat = harp_data["latitude_bounds"].data[:, 0]
        lon = harp_data["longitude_bounds"].data[:, 0]

    # In case of no data nans will be returned.
    except harp._harppy.NoDataError:
        values = np.nan
        lat = np.nan
        lon = np.nan

    return lat, lon, values


def main(sentinelsat_options: dict):
    # To make a level-3 product, we need to tell HARP what type of product we want it to process, what the validity
    # should be, and we need to define a grid. Afterwards, HARP will process each S5P file. We can then combine these
    # files into a single average for the period.

    # -- Make adjustments here -- #
    harp_product_name = ''  # You can find harp product (variables) names @
    # https://stcorp.github.io/harp/doc/html/conventions/variable_names.html, e.g. NO2_column_number_density
    qa_validity = 0.  # Minimum quality of product, [0, 1]. The recommendation for NO2 products are 0.75, but it may be
    # useful to keep it low for visualization purposes. Otherwise, there may not be any valid pixels. Play around. :)

    # Grid for HARP. Default option is Denmark but feel free to change them.
    lat_min, lat_max, lat_res = [51, 60, 0.01]
    lon_min, lon_max, lon_res = [5, 18, 0.01]

    # -- End of your adjustments -- #

    lat_n_steps = int(np.round((lat_max - lat_min) / lat_res, 0))  # Number of pixels in the lat direction.
    lon_n_steps = int(np.round((lon_max - lon_min) / lon_res, 0))  # Number of pixels in the lon direction.

    grid = lat_n_steps, lat_min, lat_res, lon_n_steps, lon_min, lon_res  # Grid for HARP. Needs to be in this order.

    file_list = os.listdir(sentinelsat_options['data_dir'])  # Get list of the downloaded files.
    values = []  # We will add 2d values to this list.

    # Iterate through the files in the list.
    for idx, file in enumerate(file_list):
        print(f"{idx + 1} / {len(file_list)}")
        lat, lon, product = harp_process(filename=file, harp_product_name=harp_product_name, qa_validity=qa_validity,
                                         data_dir=sentinelsat_options['data_dir'], grid=grid,
                                         lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max)

        # Check if there are any values in the returned variables. Append if there are.
        if np.sum(~np.isnan(product)):
            print(f"available pixels: {np.sum(~np.isnan(product))}")
            values.append(product)

        else:
            print(f"no valid overlapping data in file {file}")

    # Terminate program if there are no valid pixels in values.
    if not len(values):
        exit('no data points in grid')

    # Change the list to a numpy array and remove excess dimensions.
    values = np.stack(values)

    lon2d, lat2d = np.meshgrid(lon, lat)  # Get 2d lat lon arrays.

    # -- Plot level-3 product -- #
    s5p_level3 = plt.figure()
    # Make the figure have lat lon projection.
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Limit the extent to the region of interest.
    ax.set_extent([lon_min, lon_max, lat_min, lat_max])

    # Apply coastlines. Resolution can be 10m, 50m or 110m. Higher resolution may be slower.
    ax.coastlines(resolution='50m', color='black', linewidth=2)
    print(f"image is in shape: {lon2d.shape}")

    # Plot the mean of values as a scatter plot. Note that we do nanmean because some pixels are empty.
    plt.scatter(x=lon2d, y=lat2d, c=np.nanmean(values, axis=0), s=1, marker='.')

    # -- Make adjustments here -- #
    # Get colorbar. You can add colorbar units with cbar.set_label('unit').
    # The unit can be found where the harp product name was located.
    cbar = plt.colorbar()



    # -- End of your adjustments -- #
    # The plot will be shown until the window is closed.
    # Find anything interesting in the image? Let's look at it tomorrow in the lecture.
    # Send me a copy at stokholm@space.dtu.dk either by screenshotting or by saving the image with
    # s5_level3.savefig('cool_s5p_level3.png', format='png').
    plt.show()




if __name__ == '__main__':
    main(sentinelsat_options=SENTINELSAT_OPTIONS)
