cluster_data.csv has all the details of the CHEX-MATE sample (see http://xmm-heritage.oas.inaf.it/ for more details). 
RA and DEC refer to the x-ray peak of the cluster.

The radio_coord_search folder stores the search results of the HEASARC query. Each fits files has random 
junk data, but the header stores the name (in NVSS convention), RA, and DEC. Additionally, 
the number after "galaxy_" refers to the HER_IDX number of the galaxy minus 1 (so, galaxy_0 is HER_IDX object 1 in the CHEX-MATE reference)

VLASS.csv is a csv file containing all of the VLASS search results, which is queried by radio-xray-vlass located in the parent directory above this one. 