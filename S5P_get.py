#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    30574 Earth observations for monitoring changes (EO4Change) exercise with Sentinel-5P.
    Download Sentinel-5P Level-2 products.
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
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

# -- Proprietary modules -- #


# -- Read here -- #
# In this part of the exercise, you should only change entries in the dictionary below and run the whole script,
# e.g. either by using run file, or doing 'python s5p_get.py' in the command line while being in the correct directory.
# Add the start and end date of your search, and the footprint_file. There should already be a geojson file but
# feel free to make a new one. :) This can be done at: https://geojson.io
# It is recommended that you download multiple (2-5) of S5P files, as some of them may not contain measurements over the
# area of interest. But be careful of your 30GB storage limit on the HPC! Each S5P file is ~500MB.
# The next exercise is in file s5p_display.py.


SENTINELSAT_OPTIONS = {
    'date': ['20210501', '20210530'],  # Start, End date, YYYYMMDD, the summer period is adviced.
    'platformname': 'Sentinel-5 Precursor',  # Satellite platform name.
    'producttype': 'L2__NO2___',  # Find other products @ link below:
     # https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-5p/products-algorithms
    'processinglevel': 'L2',  # Level of the product.
    'processingmode': 'Offline',  # Processing mode, i.e. Offline, NRT.
    'footprint_file': 'dk_square.geojson', # name of geojson file. Inset filename or make your own https://geojson.io
    'username': 's5pguest',  # Default username for Sentinel-5P download, no need to sign-up.
    'password': 's5pguest',  # Default password for Sentinel-5P download, no need to sign-up.
    'data_dir': 's5p_data',  # Directory to download data to.
    'download_index': [1, 2, 3, 4, 5],  # Must be > 1. Multiple indexes list will download multiple available files.
}


def main(sentinelsat_options: dict):
    # Make data directory (if it does not exist).
    os.makedirs(os.path.join(os.getcwd(), sentinelsat_options['data_dir']), exist_ok=True)

    # Initialize API.
    api = SentinelAPI(sentinelsat_options['username'], sentinelsat_options['password'],
                      api_url='https://s5phub.copernicus.eu/dhus')

    # Get geojson footprint.
    footprint = geojson_to_wkt(read_geojson(sentinelsat_options['footprint_file']))

    # Find matching files based on criteria.
    products = api.query(area=footprint,
                         date=sentinelsat_options['date'],
                         platformname=sentinelsat_options['platformname'],
                         producttype=sentinelsat_options['producttype'],
                         processinglevel=sentinelsat_options['processinglevel'],
                         processingmode=sentinelsat_options['processingmode']
                         )

    # convert to Pandas DataFrame
    products_df = api.to_dataframe(products)

    if len(products_df) < 1:
        exit('No products available.')

    print(f"Number of products available: {len(products_df)}")
    cwd = os.getcwd()  # remember current work directory (CWD).
    os.chdir(sentinelsat_options['data_dir'])  # Change directory.
    for index in sentinelsat_options['download_index']:
        print(f"Downloading product: {products_df.head(index)['title']}")

        # Select and download product to data directory.
        product_df = products_df.head(index)  # Get desired product based on selected index.
        api.download_all(product_df.index)  # Download product. Needs '.index' as it cannot download df directly.

    os.chdir(cwd)  # Return to project directory.


if __name__ == '__main__':
    main(sentinelsat_options=SENTINELSAT_OPTIONS)
