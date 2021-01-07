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
            for a in range(1, int(threshold)):
                voids += counts[a]
            Density = 100 - voids / Total_Pixels * 100
            Densities[name] = Density
        return Densities

    def autothreshold(self):
        autoThresh = {}
        autoImage = {}
        for name, imgray in self.loadImages().items():
            th3, ret3 = cv2.threshold(imgray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)
            autoThresh[name]= th3
            autoImage[name] = ret3
            autoDensities = self.densities(th3)
        return autoDensities
