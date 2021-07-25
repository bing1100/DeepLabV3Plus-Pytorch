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
    fig, ax = mpl.pyplot.subplots(1, figsize=(6.5,6.5))
    mpl.pyplot.axis('off')
    
    srcCrs = str(src.crs).lower()
    labels = []
    if GT:
        for j in range(1,600):
            cLabelName = LABELLOCATION + str(j) + '.shp'
            
            with fiona.open(cLabelName, "r") as shapefile:
                cLabelCrs = str(shapefile.crs['init'])
                cLabels = [feature["geometry"] for feature in shapefile]
                
            if srcCrs == cLabelCrs:
                labels.extend(cLabels)
        
        patches = [PolygonPatch(feature, edgecolor="red", facecolor="red", linewidth=1) for feature in labels]
        ax.add_collection(mpl.collections.PatchCollection(patches, match_original=True))

        # for j in range(1,7):
        #     cLabelName = CENTERLOCATION + "c" + str(j) + '.shp'
            
        #     with fiona.open(cLabelName, "r") as shapefile:
        #         cLabelCrs = str(shapefile.crs['init'])
        #         cLabels = [feature["geometry"] for feature in shapefile]
        #         cLabels = [LineString(label["coordinates"]).buffer(1) for label in cLabels]
        #     # print(srcCrs, cLabelCrs)
            
        #     labels.extend(cLabels)
        
        # patches = [PolygonPatch(feature, edgecolor="red", facecolor="red", linewidth=3) for feature in labels]
        # ax.add_collection(mpl.collections.PatchCollection(patches, match_original=True))
        
        rasterio.plot.show((src, 3), ax=ax)
        saveName = SAVELOCATION + str(i) + "_Odata.png"
        fig.savefig(saveName, bbox_inches='tight', transparent=True, pad_inches=0)
    
    # Convert to numpy arrays
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

    # read the image
    roads = Image.open(ROADS + "/" + str(idx) + "_Odata.png")

    # find road masks
    pxs = np.array(roads)
    roadMask = pxs != np.array([255, 0, 0, 255])
    pxs = np.delete(pxs, 3, 2)
    pxs[roadMask[:, :, 0]] = [0, 0, 0]
    red = pxs == [255, 0, 0]
    pxs[red[:, :, 0]] = [255, 255, 255]

    # Save the segmentation
    img = Image.fromarray(pxs, 'RGB')
    gray = img.convert('L')
    bw = gray.point(lambda x: 0 if x < 128 else 255, '1')
    bw.save(SAVE_LOC + "/region_" + str(idx) + "_O_gt.png")

with Pool(18) as p:
    p.map(func, range(600))
    
with Pool(18) as p:
    p.map(func1, range(600))