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
import numpy as np
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

# -- Proprietary modules -- #


SENTINELSAT_OPTIONS = {
    'date': ['20210501', '20210530'],  # Start, End date, YYYYMMDD
    'platformname': 'Sentinel-5 Precursor',
    'producttype': 'L2__CH4___',
    'processinglevel': 'L2',
    'processingmode': 'Offline',
    'shapefile': 'dk_square.geojson',
    'username': 's5pguest',
    'password': 's5pguest',
    'file_name': '2m_temperature_dk.nc',  # should end with .nc.
    'file_location': 's5p_data',
    'dir': 'may2021/',
}


def main(sentinelsat_options: dict):
    footprint = geojson_to_wkt(read_geojson(sentinelsat_options['shapefile']))
    api = SentinelAPI(sentinelsat_options['username'], sentinelsat_options['password'],
                      api_url='https://s5phub.copernicus.eu/dhus')
    products = api.query(area=footprint,
                         date=sentinelsat_options['date'],
                         platformname=sentinelsat_options['platformname'],
                         producttype=sentinelsat_options['producttype'],
                         processinglevel=sentinelsat_options['processinglevel'],
                         processingmode=sentinelsat_options['processingmode']
                         )
    print(np.shape(products))
    api.download_all(products)


if __name__ == '__main__':
    main(sentinelsat_options=SENTINELSAT_OPTIONS)
