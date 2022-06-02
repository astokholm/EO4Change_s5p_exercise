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
import os

# -- Third-party modules -- #
import cartopy.crs as ccrs
import harp
import matplotlib.pyplot as plt
import numpy as np

# -- Proprietary modules -- #
from vis_functions import spatial_grid


S5P_OPTIONS = {
    'file_location': 's5p_data',
    'dir': 'may2021/',

    # Minimum quality of product.
    'product': 'CH4_column_volume_mixing_ratio_dry_air_validity',
    'qa_validity': -1,

    # Grid for HARP. # DK
    'lat_min': 51,
    'lat_max': 60,
    'lat_res': 0.01,
    'lon_min': 5,
    'lon_max': 18,
    'lon_res': 0.01,

    # Image options
    'remove_ticks': True,
    'dpi': 312,
    'label': r'$XCH_{4}$ [ppb]',

    # cbar
    'cbar_label': 'May 2021 monthly average',
    'fraction': 0.035,
    'pad': 0.049,
}
FIG_NAME = 'ch4_avg'
S5P_OPTIONS['extent'] = [S5P_OPTIONS['lon_min'], S5P_OPTIONS['lon_max'],
                         S5P_OPTIONS['lat_min'], S5P_OPTIONS['lat_max']]  # Map bounds, [west, east, south, north]


def savefig(fig, fig_name, dpi):
    fig.savefig(fig_name, dpi=dpi, bbox_inches='tight', pad_inches=0, transparent=True, format='.png')
    print(fig_name + " saved")


def remove_ticks(fig):
    if remove_ticks:
        plt.xticks([], [])
        plt.yticks([], [])

    return fig


def show_colorbar(scatter, ax, s5p_options: dict):
    plt.colorbar(mappable=scatter, ax=ax, label=s5p_options['label'],
                 fraction=s5p_options['fraction'], pad=s5p_options['pad'])
    plt.title(s5p_options['cbar_label'])


def view_s5p(s5p_options: dict):
    grid = spatial_grid(s5p_options['lat_min'], s5p_options['lat_max'], s5p_options['lat_res'],
                        s5p_options['lon_min'], s5p_options['lon_max'], s5p_options['lon_res'])
    file_list = os.listdir(s5p_options['dir'])
    latloned = 0
    ch4_list = []
    for idx, file in enumerate(file_list):
        print(f"{idx + 1} / {len(file_list)}")
        lon, lat, ch4 = harp_process(file=file, grid=grid)
        if np.sum(~np.isnan(ch4)):
            print(np.sum(~np.isnan(ch4)))
            ch4_list.append(ch4)
            if latloned == 0:
                latloned += 1
                lon2d, lat2d = np.meshgrid(lon, lat)

        else:
            print('no data')

    ch4_jan = np.dstack(ch4_list)
    plt.close('all')
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent(s5p_options['extent'])
    scatter = ax.scatter(x=lon2d, y=lat2d, c=np.nanmean(ch4_jan, axis=2), s=0.01, marker='.')
    ax.coastlines(resolution='10m', color='black', linewidth=2)
    fig = remove_ticks(fig)
    show_colorbar(scatter=scatter, ax=ax, s5p_options=s5p_options)
    savefig(fig, FIG_NAME, s5p_options['dpi'])


def harp_process(s5p_options: dict, file: str, grid: str):
    try:
        harp_data = harp.import_product(s5p_options['dir'] + file,
                                        operations=f"{s5p_options['product']}>{s5p_options['qa_validity']};\
                                        latitude > {s5p_options['lat_min']} [degree_north]; \
                                        latitude < {s5p_options['lat_max']} [degree_north]; \
                                        longitude > {s5p_options['lon_min']} [degree_east]; \
                                        longitude < {s5p_options['lon_max']} [degree_east]; \
                                        bin_spatial{str(grid)} ; \
                                        keep(latitude_bounds,longitude_bounds,{s5p_options['product']}) ")
        ch4 = harp_data[s5p_options['product']].data.squeeze()
        lon = harp_data["longitude_bounds"].data[:, 0]
        lat = harp_data["latitude_bounds"].data[:, 0]
    except harp._harppy.NoDataError:
        print('empty file')
        ch4 = np.nan
        lon = np.nan
        lat = np.nan

    return lon, lat, ch4


def main(s5p_options: dict):
    view_s5p(s5p_options=s5p_options)


if __name__ == '__main__':
    main(s5p_options=S5P_OPTIONS)
