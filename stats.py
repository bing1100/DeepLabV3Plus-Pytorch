import fiona
import rasterio
import rasterio.plot
import matplotlib as mpl
import matplotlib.pyplot
from descartes import PolygonPatch
from shapely.geometry import LineString
import numpy as np
import sys
from multiprocessing import Pool
np.set_printoptions(threshold=np.inf)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import math
import pickle
from multiprocessing import Pool

# [3938.47000184 3150.82132884 1876.45311538 2927.56342991 5049.26181194] [ 525.55644231  747.63753359  655.36573108 1025.89798496 2398.54461364]
# [37.25768717, 50.53054942, 41.82911744] [28.74567631, 34.12372886, 31.84100706]
# [37.25768717, 73.06358305, 105.06015209] [28.74567631, 37.23757292, 40.10277116]
ROADS = "/media/bhux/ssd/oilwell/deeplab_data/"
SAVE_LOC = "/media/bhux/ssd/oilwell/deeplab_data/"
FILELOCATION = '/media/bhux/ssd/oilwell/images/'
LABELLOCATION = '/media/bhux/ssd/oilwell/labels/all/'
CENTERLOCATION = '/media/bhux/ssd/oilwell/labels/converted/'
SAVELOCATION = '/media/bhux/ssd/oilwell/deeplab_data/'

SAT = False
GT = True
PXL = 500*500

# Normalize bands into 0.0 - 1.0 scale
def normalize(array):
    array_min, array_max = array.min(), array.max()
    return (array - array_min) / (array_max - array_min)

def sum(i):
    print("starting " + str(i))
    fileName = FILELOCATION + str(i) + '.tif'
    
    src = rasterio.open(fileName)
    src1 = rasterio.open(SAVELOCATION + "region_" + str(i) + "_sat_rgb.png")

    fir = src.read(5)
    nir = src.read(4)
    red = src.read(3)
    green = src.read(2)
    blue = src.read(1)

    return [#np.sum(blue)/250000, 
            #np.sum(green)/250000, 
            #np.sum(red)/250000, 
            #np.sum(nir)/250000, 
            #np.sum(fir)/250000, 
            np.sum(src1.read(1))/PXL, 
            np.sum(src1.read(2))/PXL, 
            np.sum(src1.read(3))/PXL]

def sd2(i):
    fileName = FILELOCATION + str(i) + '.tif'
    
    src = rasterio.open(fileName)
    src1 = rasterio.open(SAVELOCATION + "region_" + str(i) + "_sat_rgb.png")

    fir = src.read(5)
    nir = src.read(4)
    red = src.read(3)
    green = src.read(2)
    blue = src.read(1)
    
    avg = [37.25768717, 50.53054942, 41.82911744]
    
    return [#np.sum((blue-avg[0])**2)/250000, 
            #np.sum((green-avg[1])**2)/250000, 
            #np.sum((red-avg[2])**2)/250000, 
            #np.sum((nir-avg[3])**2)/250000, 
            #np.sum((fir-avg[4])**2)/250000, 
            np.sum((src1.read(1)-avg[0])**2)/PXL, 
            np.sum((src1.read(2)-avg[1])**2)/PXL, 
            np.sum((src1.read(3)-avg[2])**2)/PXL]

with Pool(20) as p:
    vals = p.map(sum, range(600))
    
    avg = np.sum(vals, axis=0) / 600
    
    vals = p.map(sd2, range(600))
    
    sd = np.sqrt(np.sum(vals, axis=0) / 600)
    print(avg, sd)