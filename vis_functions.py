#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Call sentinelsat API with SENTINELSAT_OPTIONS"""

# -- File info -- #
__author__ = ['Andreas R. Stokholm']
__copyright__ = ['A. Stokholm']
__contact__ = ['andreas_stokholm@hotmail.com']
__version__ = '0.0.1'
__date__ = '2022-01-24'

# -- Built-in modules -- #

# -- Third-party modules -- #
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np


def plot_eu(bg_img, c=1, r=1, n=1):
    polar_stereographic = ccrs.Stereographic(
        central_latitude=50.0,
        central_longitude=12.5,
        false_easting=0.0,
        false_northing=0.0,
        true_scale_latitude=70.0,
        globe=ccrs.Globe('WGS84')
    )

    if 'ne_' in bg_img:
        res = 'low'
    elif bg_img == 'BM':
        res = 'high'
    elif 'GEBCO_2019' in bg_img:
        """
        Full world at 
        layers = ['GEBCO_2019_Grid', 'GEBCO_2019_Grid_2', 'GEBCO_2019_TID'] 
        found at  https://www.gebco.net/data_and_products/gebco_web_services/2019/mapserv?request=getcapabilities&service=wms&version=1.3.0
        """
        url = 'https://www.gebco.net/data_and_products/gebco_web_services/2019/mapserv?'
        print(
            'Remember to acknow. : \nImagery reproduced from the GEBCO_2019 Grid, \nGEBCO Compilation Group (2019) GEBCO 2019 Grid \n(doi:10.5285/836f016a-33be-6ddc-e053-6c86abc0788e)')

    elif 'GEBCO_NORTH' in bg_img:
        """
        for Polar map: but wrong srs
        layers = [GEBCO_NORTH_POLAR_VIEW]    
        https://www.gebco.net/data_and_products/gebco_web_services/north_polar_view_wms/mapserv?&request=getcapabilities&service=wms&version=1.3.0
        """
        url = 'https://www.gebco.net/data_and_products/gebco_web_services/north_polar_view_wms/mapserv?'

    ax = plt.subplot(c, r, n, projection=polar_stereographic)
    # ax = plt.axes(projection=polar_stereographic)
    # Greenland
    # ax.set_extent([-60, 26, 58, 84]) # Map bounds, [west, east, south, north]
    # EU
    # ax.set_extent([-10, 40, 30, 70])  # Map bounds, [west, east, south, north]
    # DK
    ax.set_extent([7, 16, 54, 58])  # Map bounds, [west, east, south, north]

    if bg_img == 'wms':
        ax.add_wms(wms='http://vmap0.tiles.osgeo.org/wms/vmap0', layers=['basic'])
    elif 'GEBCO' in bg_img:
        ax.add_wms(wms=url, layers=[bg_img])
    else:
        ax.background_img(name=bg_img, resolution=res, extent=[-110, 20, 54, 87])

    ax.coastlines(resolution='10m', zorder=1)

    return ax


def spatial_grid(lat_min, lat_max, lat_res, lon_min, lon_max, lon_res):
    """
    Parameters
    ----------
    lat_min : float
        minimum latitude
    lat_max : float
        maximum latitude
    lat_res : float
        latitude steps. 0.01 -> pixel for every 0.01 latitude
    lon_min : float
        minimum longitude
    lon_max : float
        maximum longitude
    lon_res : float
        longitude steps. 0.01 -> pixel for every 0.01 longitude

    Returns
    -------
    grid : str
        grid for harp.import_product operations

    """
    lat_n_steps = int(np.round((lat_max - lat_min) / lat_res, 0))
    lon_n_steps = int(np.round((lon_max - lon_min) / lon_res, 0))

    grid = lat_n_steps, lat_min, lat_res, lon_n_steps, lon_min, lon_res

    return grid
