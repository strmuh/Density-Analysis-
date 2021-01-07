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
        for i, image in enumerate(self.fileList()): # Loop over images
            # Create variable for image
            im = cv2.imread(str(image))
            # Convert image Grayscale
            imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            print(im)
