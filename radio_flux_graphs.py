#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 17:02:07 2026

@author: chan_2006
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# CONSTANTS GO HERE

DEGREE = 1

df = pd.read_csv("/home/chan_2006/CLUSTER_RESEARCH/Data/cluster_data.csv")

nvss_flux = np.array([df["NVSS flux_20cm"]]) # 1.5 GHz
vlass_flux = np.array([df["VLASS flux"]]) # 3 GHz

for row in df.itertuples():
    fig, ax = plt.subplots()
    #ax.set_xscale("log")
    #ax.set_yscale("log")
    
    if (row._15 == 0 or row._15 == None) or (row._17 == 0 or row._17 == None):
        pass
    else:
        x_vals = np.array([1.5, 3]) # frequency
        y_vals = np.array([row._15, row._17]) # flux
        
        log_x = np.log10(x_vals) # convert x to logarithmic
        log_y = np.log10(y_vals) # convert y to logarithmic
        
        b, log_A = np.polyfit(log_x, log_y, DEGREE) # powerlaw with degree DEGREE specified in constants
        
        A = 10**log_A # get coefficient of fitting
        
        freq_fit = np.logspace(np.log10(1.5), np.log10(90), 500) # extrapolate to 90!!! large extrapolation and only an estimate
        flux_fit = A * freq_fit ** b # get frequency for plotting
        
        ax.plot(freq_fit, flux_fit, label = "Powerlaw Extrapolation") # plot the powerlaw
        ax.scatter(x_vals, y_vals)
    
        ax.set_xlabel("Frequency (GHz)")
        ax.set_ylabel("Flux (mJy)")
        ax.set_title(row.NAME + " HER_IDX " + str(row.HER_IDX) + ", " + "NVSS sep is " +  str(int(row._14)) + ", VLASS sep is " + str(int(row._16)))
        
        fig.savefig("/home/chan_2006/CLUSTER_RESEARCH/freq-vs-flux/" + row.NAME + "HER_IDX " + str(row.HER_IDX) + ".png")
        plt.close()