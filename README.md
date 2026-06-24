# wave-summer-2026
Code I've written for SURF summer 2026 at Caltech. My work is in identifying and removing three types of AGN contamination from Sunyaev-Zeldovich effect maps of galaxy clusters, with the goal of improving multi-probe data analysis and triaxial modeling of a sample of galaxy clusters. 
___
Inside the "Data" folder lies all the data that the scripts in this folder will use. cluster_data.csv is the CHEX-MATE sample (see http://xmm-heritage.oas.inaf.it/ for more details), and there should also be VLASS.csv which is not uploaded here but can be found online. 

radio-xray-nvss.py is a code that queries NVSS through NASA's HEASARC and calculates
the distances between the radio source from the given x-ray source. 

radio-xray-vlass.py is code that queries VLASS and does the same as above, calculating the distance between the nearest radio source and the given x-ray source. 

The code is currently being run in the order of VLASS first, then NVSS, and only clusters with a radio source found within 30 arcseconds are also queried in NVSS.  
