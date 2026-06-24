#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 12:26:26 2026

@author: chan_2006
"""

import numpy as np
from astropy.io import fits
from astropy import units as u
from astropy.coordinates import SkyCoord
import pandas as pd
from astroquery.heasarc import Heasarc

# Specify constants here

RADIUS_TO_SEARCH = 30 # in arcseconds

# Import chex-mate data

df = pd.read_csv("/home/chan_2006/CLUSTER_RESEARCH/Data/cluster_data.csv")

count = 0 # keeps track of HER_IDX
temp_object_list = {}
list_of_galaxies = df["NAME"]

for row in list_of_galaxies:
    temp_object_list[count] = [df["RA"][count], df["DEC"][count], df["z"][count]]
    count += 1

# format above is as follows: {HER_IDX : [ra, dec, z]}. RA and DEC values used
# are the x-ray peaks

list_of_results = {} # dictionary of fits files storing the radio search 
# results from NVSS for now. Format is as follows: {HER_IDX : filename}

count1 = 0

while count1 < len(list_of_galaxies):
    # retrieve coordinates of x-ray peak and query in the radio survey at those coordinates
    coords = SkyCoord(ra = df["RA"][count1], dec = df["DEC"][count1], unit = (u.hourangle, u.deg), frame = "icrs")
    table = Heasarc.query_region(coords, catalog = "NVSS", 
                                 radius = RADIUS_TO_SEARCH * u.arcsec, columns = "name, ra, dec, flux_20_cm", 
                                 verbose = "False")
    
    dummy_data = np.random.random((5, 5))
    first_header = fits.PrimaryHDU(data = dummy_data)
    # add dummy data so astropy doesn't complain 
    
    list_of_res = table["name"] # another list just for iterative purposes
    
    for i in range(len(list_of_res)):
        first_header.header["OBJECT"] = table["name"][i] # add object name to header
        first_header.header["RA"] = table["ra"][i] # add ra to header
        first_header.header["DEC"] = table["dec"][i] # add dec to header
        first_header.header["FLUX"] = table["flux_20_cm"][i]
        
    first_header.writeto("/home/chan_2006/CLUSTER_RESEARCH/Data/radio_coord_search/galaxy_" + str(count1) + ".fits", 
                         overwrite = True) # write to galaxy_i.fits file
 
    
    list_of_results.update({count1 : "galaxy_" + str(count1) + ".fits"}) # update our iterator
    
    count1 += 1
    print("Object queried") # just a visual placeholder to know when querying ends

count2 = 0
for item in list_of_results:
    with fits.open("/home/chan_2006/CLUSTER_RESEARCH/Data/radio_coord_search/" + list_of_results[item]) as hdul:
        data = hdul[0].header # open query results to get ra, dec, and flux
        
        try:
            ra = data["RA"]
            dec = data["DEC"]
            flux = data["FLUX"]
            
            coords_radio = SkyCoord(ra = ra * u.deg, dec = dec * u.deg, frame = "icrs")
            coords_xray = SkyCoord(ra = temp_object_list[item][0], dec = temp_object_list[item][1], unit = (u.hourangle, u.deg))
            
            separate_value = coords_radio.separation(coords_xray).arcsec # calculate separation in arcseconds
            print("Seperation for", item, "is: ", separate_value, "arcseconds")
            if df["VLASS Separation"][count2] != 0: # only if VLASS has data, otherwise don't do
                df.loc[count2, "NVSS Separation"] = separate_value # update our spreadsheet
                df.loc[count2, "NVSS flux_20cm"] = flux # update flux as well
            else:
                df.loc[count2, "NVSS Separation"] = 0
                df.loc[count2, "NVSS flux_20cm"] = 0
                
            count2 += 1
        
        except Exception as e:
            print("Failed on ", item, e)
            df.loc[count2, "NVSS Separation"] = 0
            df.loc[count2, "NVSS flux_20cm"] = 0
            count2 += 1

df.to_csv("/home/chan_2006/CLUSTER_RESEARCH/Data/cluster_data.csv", index = False)