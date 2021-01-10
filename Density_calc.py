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
        # Create empty Dict to store Image and auto Threshold data
        autoImage = {}
        #Loop over images and obtain auto threshold data
        for name, imgray in self.loadImages().items():
            th3, ret3 = cv2.threshold(imgray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)
            autoImage[name] = {'Threshold':th3, 'Image':ret3}
        return autoImage

    def manimage(self, threshold=110):
        # Create empty Dict to store Image and manual Threshold data
        manImage = {}
        # Loop over images and obtain manual threshold data
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

    def mandensity(self, threshold=110):
        manthresholds = {}
        for name, items in self.manimage(threshold).items():
            manthresholds[name] = items['Threshold']
        mandensities = self.densities(manthresholds)
        return mandensities

    def histogram_plot(self):
        hist_data = {}
        for name, imgray in self.loadImages().items():
            counts, bins = np.histogram(imgray, range(256))
            hist_data[name] = {'Counts':counts.transpose().tolist(), 'Bins': bins.transpose()}
            # plot histogram centered on values 0..255
            # plt.figure(name)
            # plt.bar(bins[:-1] - 0.5, counts, width=1, edgecolor='none')
            # for j, k in enumerate(counts):
            #     if k != 0:
            #         min_val = j
            #         break
            # for d, t in enumerate(counts[::-1]):
            #     if t!= 0:
            #         max_val = len(counts)-d
            #         break
            # plt.xlim([min_val-2, max_val+2])
            # plt.xlim([-0.5, 255.5])
            # plt.show()
        return hist_data

    def save_images(self):
        manimgs = self.manimage()
        autoimgs = self.autoimage()
        ogimgs = self.loadImages()
        for name, ogimg in ogimgs.items():
            fig, axs = plt.subplots(1,3, constrained_layout=True)
            axs[0].imshow(ogimg, 'gray')
            axs[0].set_title('Original Image')
            axs[1].imshow(manimgs[name]['Image'], 'gray')
            axs[1].set_title('Manual Threshold ={}'.format(manimgs[name]['Threshold']))
            axs[2].imshow(autoimgs[name]['Image'], 'gray')
            axs[2].set_title('Automatic Threshold={}'.format(autoimgs[name]['Threshold']))
            fig.suptitle(name, fontsize=11)
            # plt.tight_layout()
            plt.show()

    def export_data(self):
        manimgs = self.manimage()
        autoimgs = self.autoimage()
        hist = self.histogram_plot()
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook('Test_results.xlsx')
        worksheet = workbook.add_worksheet(self.directory)
        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})
        # # Write some data headers.
        worksheet.write('A1', self.directory, bold)
        worksheet.write('A2', 'Sample Number', bold)
        worksheet.write('B2', 'Threshold', bold)
        worksheet.write('C2', 'Density', bold)
        # Start from the first cell. Rows and columns are zero indexed.
        row = 2
        col = 0
        # Iterate over the data and write it out row by row.
        for key, value in self.autodensity().items():
            worksheet.write(row, col, key.split(".")[0])
            worksheet.write(row, col + 1, autoimgs[key]['Threshold'])
            worksheet.write(row, col + 2, value)
            for a,w in enumerate(hist[key]['Counts']):
                worksheet.write(2, 5 + a, w)
            row += 1
        workbook.close()
        