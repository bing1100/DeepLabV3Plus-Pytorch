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
from skimage import io

ROADS = "/media/bhux/ssd/oilwell/deeplab_data/"
SAVE_LOC = "/media/bhux/ssd/oilwell/deeplab_data/"
FILELOCATION = '/media/bhux/ssd/oilwell/images/'
LABELLOCATION = '/media/bhux/ssd/oilwell/labels/all/'
CENTERLOCATION = '/media/bhux/ssd/oilwell/labels/converted/'
SAVELOCATION = '/media/bhux/ssd/oilwell/deeplab_data/'

SAT = False
GT = True

# Normalize bands into 0.0 - 1.0 scale
def normalize(array):
    array_min, array_max = array.min(), array.max()
    return (array - array_min) / (array_max - array_min)

def func(i):
    print("starting " + str(i))
    fileName = FILELOCATION + str(i) + '.tif'
    
    src = rasterio.open(fileName)
    fig, ax = mpl.pyplot.subplots(1, figsize=(12,12))
    mpl.pyplot.axis('off')
    
    if SAT:
        fir = src.read(5)
        nir = src.read(4)
        red = src.read(3)
        green = src.read(2)
        blue = src.read(1)

        # Normalize band DN
        fir_norm = normalize(fir)
        nir_norm = normalize(nir)
        red_norm = normalize(red)
        green_norm = normalize(green)
        blue_norm = normalize(blue)

        # Stack bands
        nrg = np.dstack((red_norm, green_norm, blue_norm))
        mpl.pyplot.imshow(nrg)
        saveName = SAVELOCATION + "/region_" + str(i) + "_sat_rgb.png"
        fig.savefig(saveName, bbox_inches='tight', transparent=True, pad_inches=0)
        
        # Stack bands
        nrg = np.dstack((red_norm, nir_norm, fir_norm))
        mpl.pyplot.imshow(nrg)
        saveName = SAVELOCATION + "/region_" + str(i) + "_sat.png"
        fig.savefig(saveName, bbox_inches='tight', transparent=True, pad_inches=0)
    
    fig.clf()
    mpl.pyplot.close()

def func1(idx):
    print("Processing ", idx)

    image = io.imread(SAVELOCATION + "/region_" + str(idx) + "_sat_rgb.png")

    _ = plt.hist(image.ravel(), bins = 256, color = 'orange', )
    _ = plt.hist(image[:, :, 0].ravel(), bins = 256, color = 'red', alpha = 0.5)
    _ = plt.hist(image[:, :, 1].ravel(), bins = 256, color = 'Green', alpha = 0.5)
    _ = plt.hist(image[:, :, 2].ravel(), bins = 256, color = 'Blue', alpha = 0.5)
    _ = plt.xlabel('Intensity Value')
    _ = plt.ylabel('Count')
    _ = plt.legend(['Total', 'Red_Channel', 'Green_Channel', 'Blue_Channel'])
    plt.show()
    
with Pool(12) as p:
    p.map(func1, range(1))
    