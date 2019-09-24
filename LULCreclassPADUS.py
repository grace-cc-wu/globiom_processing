# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:41:44 2019

@author: Grace
"""

##--------------------------------Preamble ----------------------------------
import arcpy
import numpy
import numpy.lib.recfunctions
import scipy.stats as stats
import math
import time
import os
import csv
import re
import pandas as pd
import collections
start_time = time.time()
print(start_time)
# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")
from arcpy import env
from arcpy.sa import *
import arcpy.cartography as CA
arcpy.env.overwriteOutput = True

year = 2016

## PAD US as raster (using LULC as template for conversion)
PAD_fp = "C:\\Users\\Grace\\Documents\\FABLE\GLOBIOM\\US_data\\Conservation\PADUS2_0_GDB_Arc10x\PADUS2_0.gdb\\PADUS2_0Combined_Proclamation_Marine_Fee_Designation_Easement_proj_raster"

## Polygon (SimU) datast
SimU_fp = "C:\\Users\\Grace\\Documents\\FABLE\\GLOBIOM\\SimU\\gis\\SimU_all_select840_USstateSplit_proj_newSUcol.shp"

## Raster dataset
LULC_fp= "C:\\Users\\Grace\\Documents\\FABLE\\GLOBIOM\\US_data\\LULC\\NLCD\\NLCD_" + str(year) + "_Land_Cover_L48_20190424\\NLCD_" + str(year) + "_Land_Cover_L48_20190424.img"


## Reclassify the gap raster
## all status 1 and 2 as 10x the original class value, all statuses 3 and 4 as value 1 (original LULC class value)
PAD_reclass = Reclassify(PAD_fp, "GAP_Sts_int", 
                         RemapValue([[1,10],[2,10],[3,1],[4,1]]))

## Multiply the reclassified PADUS values by the NLCD class values
NLCD_PAD = Raster(LULC_fp)*PAD_reclass

## fill in the gaps in NLCD_PAD by using raster calculator
NLCD_PAD_final = Con(IsNull(NLCD_PAD), Raster(LULC_fp), NLCD_PAD)

## Save the modified NLCD class
NLCD_PAD_final.save(LULC_fp.replace(".img", "") + "_PAD.tif")

elapsed_time = (time.time() - start_time)/(60)
print("^^^^ Total time for completion: " + str(elapsed_time) + " minutes")
