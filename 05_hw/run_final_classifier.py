'''
run_final_classifier.py
Author: Victor Chen
Date: 10-14-12
Description: In the terminal, type "ipython --pylab", 
             then "run run_final_classifier.py path/to/images"
             If that fails, just perform "run run_final_classifier.py",
             then 'run_final_classifier("path/to/images")'
             If that STILL doesn't work, try out the run_final_classifier
             method inside the notebook file.
'''

# Run ipython with --pylab
from sys import argv

import numpy as np
import matplotlib

from matplotlib import image as mpimg
import os
import string
import cPickle

from scipy.ndimage.filters import correlate1d
import skimage
from skimage.filter import sobel, canny
from skimage.feature import greycomatrix, greycoprops

from scipy import ndimage
from scipy.ndimage import watershed_ift

import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV
from sklearn import metrics

# Restore session from data_pickled.dat and target_pickled.dat
f = open('data_pickled.dat','rb')
p = cPickle.Unpickler(f)
data = p.load()
f.close()

f = open('target_pickled.dat', 'rb')
p = cPickle.Unpickler(f)
target = p.load()
f.close()

# Construct a random forest classifier
## Note: I did not include a pickle.dat for the classifier because it
## is over 600mb.
parameters = {'n_estimators':[20,60,100], 'max_features':[3,11,19], \
              'compute_importances':[True]}
rf_tune = GridSearchCV(RandomForestClassifier(), \
            parameters, score_func=metrics.zero_one_score, n_jobs=-1, cv=5)

rf_opt = rf_tune.fit(data,target)

def run_final_classifier(directory_path):
    
    f = open('img_classes_pickled.dat','rb')
    p = cPickle.Unpickler(f)
    img_classes = p.load()
    f.close()
    
    test_data = []
    for dirname, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            if not filename[-4:] == '.jpg':
                continue
            fullfilename = os.path.join(dirname, filename)
            img = mpimg.imread(fullfilename,'rb')
            ## The following bug is not fixed yet: imread flips the image upside-down
            img = np.flipud(img)
            if len(img.shape) == 2:
                img = np.dstack( (img, img, img) )
            
            features = []
            ######## Compute 15 features ########
            
            ###### No. 1: image size, or number of pixels ------------------------------------
            num_pixels = img[...,0].size
            features.append(num_pixels)
            
            ###### No. 2-4: avg of the RGB channel intensity ---------------------------------
            avg_R = np.mean(img[...,0])
            features.append(avg_R)
            avg_G = np.mean(img[...,1])
            features.append(avg_G)
            avg_B = np.mean(img[...,2])
            features.append(avg_B)
            
            ###### No. 5-8: GLCM for corner patches ------------------------------------------
            # RGB --> gray
            try:
                r,g,b = np.rollaxis(img,axis=-1)
            except:
                print fullfilename
            gray = (0.299*r + 0.587*g + 0.114*b).astype('int');
            
            PATCH_SIZE = 20
            # select some corner patches
            TL = (0,0)
            TR = (0,gray.shape[1] - 1 - PATCH_SIZE)
            BL = (gray.shape[0] - 1 - PATCH_SIZE, 0)
            BR = (gray.shape[0] - 1 - PATCH_SIZE, gray.shape[1] - 1 - PATCH_SIZE)
            locs = [TL, TR, BL, BR]
            corner_patches = []
            for loc in locs:
                corner_patches.append(gray[loc[0]:loc[0] + PATCH_SIZE,
                                           loc[1]:loc[1] + PATCH_SIZE])
            # compute some GLCM properties each patch
            xs = []
            ys = []
            for i, patch in enumerate(corner_patches):
                glcm = greycomatrix(patch, [5], [0], 256, symmetric=True, normed=True)
                xs.append(greycoprops(glcm, 'dissimilarity')[0, 0])
                ys.append(greycoprops(glcm, 'correlation')[0, 0])
            
            features.append(np.mean(xs))
            features.append(np.var(xs))
            features.append(np.mean(ys))
            features.append(np.var(ys))
            
            ###### No. 9-12: GLCM for central patches ----------------------------------------
            # RGB --> gray
            #r,g,b = np.rollaxis(img,axis=-1)
            gray = (0.299*r + 0.587*g + 0.114*b).astype('int');
            
            PATCH_SIZE = 20
            # select some center patches
            center = (gray.shape[0] / 2, gray.shape[1] / 2)
            TL = (center[0] - PATCH_SIZE, center[1] - PATCH_SIZE)
            TR = (center[0] - PATCH_SIZE, center[1] + PATCH_SIZE)
            BL = (center[0] + PATCH_SIZE, center[1] - PATCH_SIZE)
            BR = (center[0] + PATCH_SIZE, center[1] + PATCH_SIZE)
            locs = [TL, TR, BL, BR]
            corner_patches = []
            for loc in locs:
                corner_patches.append(gray[loc[0]:loc[0] + PATCH_SIZE,
                                           loc[1]:loc[1] + PATCH_SIZE])
            # compute some GLCM properties each patch
            xs = []
            ys = []
            for i, patch in enumerate(corner_patches):
                glcm = greycomatrix(patch, [5], [0], 256, symmetric=True, normed=True)
                xs.append(greycoprops(glcm, 'dissimilarity')[0, 0])
                ys.append(greycoprops(glcm, 'correlation')[0, 0])
            
            features.append(np.mean(xs))
            features.append(np.var(xs))
            features.append(np.mean(ys))
            features.append(np.var(ys))
            
            ###### No. 13-16: Edges (Sobel & Canny) ------------------------------------------
            # Proportion of image that are edges
            
            # sobel works only with float32, not uint8
            #
            gray = 0.299*r + 0.587*g + 0.114*b;
            edges_sobel = sobel(gray)
            SOBEL_THRESHOLD_1 = np.max(edges_sobel.flat) / 10
            edges_sobel_size = edges_sobel[edges_sobel > SOBEL_THRESHOLD_1].size
            edges_sobel_ratio_1 = edges_sobel_size * 1. / gray.size
            SOBEL_THRESHOLD_2 = np.max(edges_sobel.flat) / 5
            edges_sobel_size = edges_sobel[edges_sobel > SOBEL_THRESHOLD_2].size
            edges_sobel_ratio_2 = edges_sobel_size * 1. / gray.size
            SOBEL_THRESHOLD_3 = np.max(edges_sobel.flat) / 3
            edges_sobel_size = edges_sobel[edges_sobel > SOBEL_THRESHOLD_3].size
            edges_sobel_ratio_3 = edges_sobel_size * 1. / gray.size
    
            edges_canny = canny(gray).astype('int');
            edges_canny_ratio = np.sum(edges_canny.astype(int)) * 1. / gray.size;
            
            features.append(edges_sobel_ratio_1)
            features.append(edges_sobel_ratio_2)
            features.append(edges_sobel_ratio_3)
            features.append(edges_canny_ratio)
            
            ###### No. 17-19: Segmentation (label count) -------------------------------------
            gray = (0.299*r + 0.587*g + 0.114*b).astype('int');
            elevation_map = sobel(gray)
            elevation_map = elevation_map / np.max(elevation_map)
            elevation_map = (elevation_map * 255).astype('uint8')
            
            markers = np.zeros_like(gray);
            markers[gray < 30] = 1
            markers[gray > 150] = 2
            segmentation = watershed_ift(elevation_map,markers)
            segmentation = ndimage.binary_fill_holes(segmentation - 1)
            labeled_elements, count = ndimage.label(segmentation)
            features.append(count)
            
            markers = np.zeros_like(gray)
            markers[gray < 80] = 1
            markers[gray > 180] = 2
            segmentation = watershed_ift(elevation_map,markers)
            segmentation = ndimage.binary_fill_holes(segmentation - 1)
            labeled_elements, count = ndimage.label(segmentation)
            features.append(count)
            
            markers = np.zeros_like(gray)
            markers[gray < 100] = 1
            markers[gray > 200] = 2
            segmentation = watershed_ift(elevation_map,markers)
            segmentation = ndimage.binary_fill_holes(segmentation - 1)
            labeled_elements, count = ndimage.label(segmentation)
            features.append(count)
             
            ###### Store features into data --------------------------------------------------
            test_data.append(features)
            
    test_data = np.array(test_data, dtype='float16')
    
    # Load pickled classifier
    f = open('clf_pickled.dat','rb')
    p = cPickle.Unpickler(f)
    rf_clf = p.load()
    f.close()
    # make predictions for testing set
    predictions = rf_clf.predict(test_data)
    print "filename         predicted_class"
    print "------------------------------------"
    # assuming order of the predictions is the same as the order of the filenames...
    for dirname, dirnames, filenames in os.walk(directory_path):
        counter = 0
        for filename in filenames:
            if not filename[-4:] == '.jpg':
                continue
            ind = int(predictions[counter])
            counter += 1
            for key, val in img_classes.iteritems():
                if val == ind:
                    print filename + "  " + key


if __name__ == '__main__':
    try:
        run_final_classifier(argv[1])
    except:
        pass