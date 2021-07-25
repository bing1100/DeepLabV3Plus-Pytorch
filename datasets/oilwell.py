import os
import sys
import tarfile
import collections
import torch.utils.data as data
import shutil
import numpy as np

from PIL import Image
from torchvision.datasets.utils import download_url, check_integrity

class Oilwell(data.Dataset):
    train_id_to_color = np.array([(0,0,0), (255,255,255)])
    
    def __init__(self,
                 root,
                 image_set='train',
                 type='RO',
                 splits="B",
                 color="RBG",
                 update=False,
                 download=False,
                 transform=None):
        
        self.root = '/media/bhux/ssd/oilwell/deeplab_data/'
        self.transform = transform
        
        imgExt = "_sat_rgb.png"
        if color == "IF":
            imgExt = "_sat.png"
            
        targetLoc = "/region_"
        if update:
            targetLoc = "/update/region_"
        
        r = range(600)
        if splits == "R":
            r = range(400)
        elif splits == "F":
            r = range(400,600)
        
        indrange_train = []
        indrange_validation = []
        for x in r:
            if x % 10 < 8 :
                indrange_train.append(x)

            if x % 10 == 9:
                indrange_validation.append(x)

        if image_set == 'train':
            self.images = [self.root + "/region_" + str(i) + imgExt for i in indrange_train]
            self.masks = [self.root + targetLoc + str(i) + "_"+type+"_gt.png" for i in indrange_train]
        elif image_set == 'val':
            self.images = [self.root + "/region_" + str(i) + imgExt for i in indrange_validation]
            self.masks = [self.root + targetLoc + str(i) + "_"+type+"_gt.png" for i in indrange_validation]
            
        assert (len(self.images) == len(self.masks))

    def __getitem__(self, index):
        """
        Args:
            index (int): Index
        Returns:
            tuple: (image, target) where target is the image segmentation.
        """
        imgname = self.images[index]
        tarname = self.masks[index]
        img = Image.open(imgname).convert('RGB')
        target = Image.open(tarname)
        if self.transform is not None:
            img, target = self.transform(img, target)

        return img, target, imgname, tarname
    
    @classmethod
    def decode_target(cls, target):
        return cls.train_id_to_color[target]

    def __len__(self):
        return len(self.images)
     