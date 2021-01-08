""" Function to Determine Image Pixel Density for Microscopy Samples """
# Import relavent packages
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import xlsxwriter

# Create analysis class
class Determinedensity():
    # Create class variables
    def __init__(self, directory):
        self.directory = directory

    def __str__(self):
        return self.directory

    # Create class method to form list of image files
    def fileList(self):
        filelist = []
        for file in os.listdir(self.directory): # Loop over all files in directory
            # Extract Image files (JPG)
            if file.endswith(".JPG"):
                filelist.append(file)
        return filelist

    # Create method for reading image files
    def loadImages(self):
        imgrays = {}
        for i, image in enumerate(self.fileList()): # Loop over images
            # Create variable for image
            im = cv2.imread(str(image))
            # Convert image Grayscale
            imgrays[image] = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        return imgrays

    def densities(self, threshold):
        Hist = {}
        Densities = {}
        for name, imgray in self.loadImages().items():
            counts, bins = np.histogram(imgray, range(256))
            # Store Histogram data in Dictionary
            Hist[name] = [[counts], [bins]]
            Total_Pixels = sum(counts)
            voids = 0
            for a in range(1, int(threshold[name])):
                voids += counts[a]
            Density = 100 - voids / Total_Pixels * 100
            Densities[name] = Density
        return Densities

    def autoimage(self):
        autoImage = {}
        for name, imgray in self.loadImages().items():
            th3, ret3 = cv2.threshold(imgray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)
            autoImage[name] = {'Threshold':th3, 'Image':ret3}
        return autoImage

    def manimage(self, threshold=110):
        manImage = {}
        for name, imgray in self.loadImages().items():
            thresh1, ret = cv2.threshold(imgray, threshold, 255, cv2.THRESH_BINARY)
            manImage[name] = {'Threshold':thresh1, 'Image':ret}
        return manImage

    def autodensity(self):
        autoThresh = {}
        for name, items in self.autoimage().items():
            autoThresh[name] = items['Threshold']
        autoDensities = self.densities(autoThresh)
        return autoDensities

    def mandensity(self):
        manthresholds = {}
        for name, items in self.manimage().items():
            manthresholds[name] = items['Threshold']
        mandensities = self.densities(manthresholds)
        return mandensities

    def histogram_plot(self):
        for name, imgray in self.loadImages().items():
            counts, bins = np.histogram(imgray, range(256))
            # plot histogram centered on values 0..255
            plt.figure(name)
            plt.bar(bins[:-1] - 0.5, counts, width=1, edgecolor='none')
            # for j, k in enumerate(counts):
            #     if k != 0:
            #         min_val = j
            #         break
            # for d, t in enumerate(counts[::-1]):
            #     if t!= 0:
            #         max_val = len(counts)-d
            #         break
            # plt.xlim([min_val-2, max_val+2])
            plt.xlim([-0.5, 255.5])
            plt.show()

    def save_images(self):
        manimgs = self.manimage()
        autoimgs = self.autoimage()
        ogimgs = self.loadImages()
        for name, ogimg in ogimgs.items():
            fig, axs = plt.subplots(1,3)
            axs[0].imshow(ogimg, 'gray')
            axs[0].set_title('Original Image')
            axs[1].imshow(manimgs[name]['Image'], 'gray')
            axs[1].set_title('Manual Threshold')
            axs[2].imshow(autoimgs[name]['Image'], 'gray')
            axs[2].set_title('Automatic Threshold')
            fig.suptitle(name, fontsize=16)
            plt.show()
