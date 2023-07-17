from setuptools import setup, find_packages

# Author: Artan Salihu
# Date: 2020-04-20
# Purpose: Setup file for MCGOsmHelperNX package
# Usage: python setup.py sdist bdist_wheel
#        twine upload dist/*
#        pip install MCGOsmHelperNX
#        python -m MCGOsmHelperNX
#        python -m MCGOsmHelperNX --help
#        python -m MCGOsmHelperNX --help_options
setup(
    name='mcgosmhelpernxx',
    version='0.1.2',
    author='Artan Salihu',
    description='A helper package for the MCGOsm data loader in python using OSM api and networkx',
    license='MIT',
    keywords='MCGOsm, Artan Salihu, TU Wien, OSM, Ray-tracer',
    url='https://www.artansalihu.com/',
    author_email='artan.salihu@tuwien.ac.at',
    maintainer='Artan Salihu',
    download_url='https://mcg-deep-wrt.netlify.app/deep-wrt/utilities/',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'networkx',
        'requests',
        'matplotlib',
        'scipy',
        'shapely',
        'geopandas',
        'rtree',
        'pyproj',
        'osmnx',
        'folium',
        'geojson',
    ],
    entry_points={
        'console_scripts': [
            'mcgosmhelpernxx=mcgosmhelpernxx.main:main',
        ],
    },
)