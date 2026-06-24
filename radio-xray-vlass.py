#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 15:32:48 2026

@author: chan_2006
"""

import numpy as np
from astropy.io import fits
from astropy import units as u
from astropy.coordinates import SkyCoord
import pandas as pd
from tqdm.auto import tqdm
import polars as pl

# Specify constants here

RADIUS_TO_SEARCH = 30 # in arcseconds

# Import CHEX-MATE and VLASS data

df = pd.read_csv("/home/chan_2006/CLUSTER_RESEARCH/Data/cluster_data.csv")
vlass = pd.read_csv("/home/chan_2006/CLUSTER_RESEARCH/Data/VLASS.csv")

count = 0 # keeps track of HER_IDX
temp_object_list = {}
list_of_galaxies = df["NAME"]

for row in list_of_galaxies:
    temp_object_list[count] = [df["RA"][count], df["DEC"][count], df["z"][count]]
    count += 1

# format above is as follows: {HER_IDX : [ra, dec, z]}. RA and DEC values used
# are the x-ray peaks

query_ra = (
    (pl.scan_csv("/home/chan_2006/CLUSTER_RESEARCH/Data/VLASS.csv").select(["RA_Source"])))

ra_table = query_ra.collect()
ra_list = ra_table.get_column("RA_Source").to_list()

query_dec = (
    (pl.scan_csv("/home/chan_2006/CLUSTER_RESEARCH/Data/VLASS.csv").select(["DEC_Source"])))

dec_table = query_dec.collect()
dec_list = dec_table.get_column("DEC_Source").to_list()

query_name = (
    (pl.scan_csv("/home/chan_2006/CLUSTER_RESEARCH/Data/VLASS.csv").select(["Host_objID"])))

name_table = query_name.collect()
name_list = name_table.get_column("Host_objID").to_list()

catalog_coords = SkyCoord(ra = ra_list * u.deg, dec = dec_list * u.deg, frame = "icrs")

count1 = 0
while count1 < len(list_of_galaxies):
    # retrieve coordinates of x-ray peak and query in the radio survey at those coordinates
    coords = SkyCoord(ra = df["RA"][count1], dec = df["DEC"][count1], unit = (u.hourangle, u.deg), frame = "icrs")
    
    idx, sep, _ = coords.match_to_catalog_sky(catalog_coords)
    
    if sep.arcsec <= RADIUS_TO_SEARCH:
        df.loc[count1, "VLASS Separation"] = sep.arcsec
        df.loc[count1, "VLASS flux"] = vlass["Total_flux_source"][idx]
    else:
        df.loc[count1, "VLASS Separation"] = 0
        df.loc[count1, "VLASS flux"] = 0
    
    count1 += 1
    
df.to_csv("/home/chan_2006/CLUSTER_RESEARCH/Data/cluster_data.csv", index = False)



