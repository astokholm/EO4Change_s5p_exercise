#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    30574 Earth observations for monitoring changes (EO4Change) exercise with Sentinel-5P.
    Show Sentinel-5P Level-2 product.
"""

# -- File info -- #
__author__ = ['Andreas R. Stokholm']
__copyright__ = ['A. Stokholm']
__contact__ = ['andreas_stokholm@hotmail.com']
__version__ = '0.0.1'
__date__ = '2022-06-06'

# -- Built-in modules -- #

# -- Third-party modules -- #
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

# -- Proprietary modules -- #
from s5p_get import SENTINELSAT_OPTIONS


# -- Read here -- #
# In this part of the exercise, you can display one of the downloaded files on a world map. Depending on what product
# you have downloaded, the product name will vary. To find out the desired product name, look up the
# Product User Manual (PUM) 
# https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-5p/products-algorithms
# Again, you may have to try different files as some may be empty (despite the large file size).
# Fill out the file and the product name and run. Optionally, you can add units to your colorbar or change the extent
# to cover only your region of interest.
# The final part of the exercise is in s5p_level3.py.


def main(sentinelsat_options: dict):
    # -- Enter name of the Sentinel-1 file here: (Include the file extension!). -- #
    file = 'S5P_OFFL_L2__NO2____20210529T020851_20210529T035021_18780_01_010400_20210530T190815.nc'  # example file
    s5p_product_name = 'nitrogendioxide_tropospheric_column'  # Name of the product in the level-2 file.
    s5p_product = xr.open_dataset(sentinelsat_options['data_dir'] + '/' + file, group='PRODUCT')  # Opens the .nc file.

    s5p_fig = plt.figure()

    # Make the figure have lat lon projection.
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Apply coastlines. Resolution can be 10m, 50m or 110m. Higher resolution may be slower.
    ax.coastlines(resolution='110m', color='black', linewidth=1)

    # Plot the product as a scatter plot. Note that x=lon and y=lat.
    plt.scatter(x=s5p_product['longitude'], y=s5p_product['latitude'],
                c=s5p_product[s5p_product_name].squeeze(),
                vmin=np.nanquantile(s5p_product[s5p_product_name], q=0.01),
                vmax=np.nanquantile(s5p_product[s5p_product_name], q=0.99))

    # Get colorbar. You can add colorbar units with cbar.set_label('unit').
    # The unit can be found by s5p_product['your product'].attrs['units'].
    cbar = plt.colorbar()

    # The figure can be saved with s5p_fig.savefig('cool_s5p_fig.png', format='png').

    # The plot will be shown until the window is closed.
    plt.show()


if __name__ == '__main__':
    main(sentinelsat_options=SENTINELSAT_OPTIONS)
