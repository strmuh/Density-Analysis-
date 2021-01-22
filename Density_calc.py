""" Function to Determine Image Pixel Density for Microscopy Samples """
# Import relavent packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os
import xlsxwriter
from openpyxl import load_workbook

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
        for image in self.fileList(): # Loop over images
            # Create variable for image
            im = cv2.imread(self.directory+'/'+ str(image))
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
        autoThresh = {}
        #Loop over images and obtain auto threshold data
        for name, imgray in self.loadImages().items():
            th3, ret3 = cv2.threshold(imgray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)
            autoImage[name] = ret3
            autoThresh[name] = th3
        return autoImage, autoThresh

    def manimage(self, threshold=110):
        # Create empty Dict to store Image and manual Threshold data
        manImage = {}
        manThresh = {}
        # Loop over images and obtain manual threshold data
        for name, imgray in self.loadImages().items():
            thresh1, ret = cv2.threshold(imgray, threshold, 255, cv2.THRESH_BINARY)
            manImage[name] = ret
            manThresh[name] =  thresh1
        return manImage, manThresh

    def autodensity(self):
        autoThresh = self.autoimage()[1]
        autoDensities = self.densities(autoThresh)
        return autoDensities

    def mandensity(self, threshold=110):
        manthresholds = self.manimage()[1]
        mandensities = self.densities(manthresholds)
        return mandensities

    def histogram_plot(self):
        hist_data = {}
        for name, imgray in self.loadImages().items():
            counts, bins = np.histogram(imgray, range(256))
            hist_data[name] = {'Counts':counts,'Bins':bins}
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

    def save_images(self, destination='', preview = False, save_fig = False):
        manimgs = self.manimage()
        autoimgs = self.autoimage()
        ogimgs = self.loadImages()
        fig_list = []
        if save_fig:
            # fig, axs = plt.subplots(1, 3, constrained_layout=True)
            for name, ogimg in ogimgs.items():
                fig, axs = plt.subplots(1, 3, constrained_layout=True)
                axs[0].imshow(ogimg, 'gray')
                axs[0].set_title('Original Image')
                axs[1].imshow(manimgs[0][name], 'gray')
                axs[1].set_title('Manual Threshold ={}'.format(manimgs[1][name]))
                axs[2].imshow(autoimgs[0][name], 'gray')
                axs[2].set_title('Automatic Threshold={}'.format(autoimgs[1][name]))
                fig.suptitle(name, fontsize=11)
                plt.draw()
                out = destination+'/'+str(name)
                plt.savefig(out)
                plt.close()
                
            # plt.tight_layout()
        if preview:
            pre_image = self.fileList()[0]
            fig, axs = plt.subplots(1, 3, constrained_layout=True)
            axs[0].imshow(ogimgs[pre_image], 'gray')
            axs[0].set_title('Original Image')
            axs[1].imshow(manimgs[0][pre_image], 'gray')
            axs[1].set_title('Manual Threshold ={}'.format(manimgs[1][pre_image]))
            axs[2].imshow(autoimgs[0][pre_image], 'gray')
            axs[2].set_title('Automatic Threshold={}'.format(autoimgs[1][pre_image]))
            fig.suptitle(pre_image, fontsize=11)
            plt.show()


    def export_data(self, auto_option = False, man_option = False, threshold = 110, filename = 'Test_results.xlsx'):
        hist = self.histogram_plot()

        # Create DataFrame with info to be exported
        if auto_option and man_option:
            # Assign auto threshold density and image data to variables
            density_data = [self.autodensity(),self.autoimage()[1],self.mandensity(threshold),self.manimage(threshold)[1]]
            # image_data_auto = self.autoimage()[0]
            # # Assign manual threshold density and image data to variables
            # density_data_man = self.mandensity(threshold).items()
            # image_data_man = self.manimage(threshold)
            ex_df = pd.DataFrame(density_data).transpose()
            ex_df.columns = ['Auto Density', 'Auto Threshold', 'Manual Density', 'Manual Threshold']
            ex_df.index.name = 'Sample Number'
        elif auto_option and not man_option:
            density_data = [self.autodensity(),self.autoimage()[1]]
            ex_df = pd.DataFrame(density_data).transpose()
            ex_df.columns = ['Auto Density', 'Auto Threshold']
            ex_df.index.name = 'Sample Number'
        else:
            density_data = [self.mandensity(threshold),self.manimage(threshold)[1]]
            ex_df = pd.DataFrame(density_data).transpose()
            ex_df.columns = ['Manual Density', 'Threshold']
            ex_df.index.name = 'Sample Number'

        stats = pd.DataFrame(ex_df.describe())
        stats.index.name = 'Statistics Summary'
        hist_out= pd.DataFrame([hist[i]['Counts'] for i in hist.keys()], index = hist.keys())
        hist_out.rename_axis('Histogram Bins:', inplace=True)
        hist_out.rename_axis('Histogram Data', axis = 1, inplace = True)
        # Create a workbook and add a worksheet.
        try:
            book = load_workbook(filename)
            writer = pd.ExcelWriter(filename, engine='openpyxl')
            writer.book = book
        except FileNotFoundError:
            # Create a Pandas Excel writer using XlsxWriter as the engine.
            writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        # Position the dataframes in the worksheet.
        folder_name = self.directory.split('/')
        ex_df.to_excel(writer, sheet_name=folder_name[-1], index=True)  # Default position, cell A1.
        stats.to_excel(writer, sheet_name=folder_name[-1], index=True, startcol=len(ex_df.columns)+2)
        hist_out.to_excel(writer, sheet_name=folder_name[-1], startcol=len(ex_df.columns)+len(stats.columns)+4)
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        

        # workbook = xlsxwriter.Workbook('Test_results.xlsx')
        # worksheet = workbook.add_worksheet(self.directory)
        # # Add a bold format to use to highlight cells.
        # bold = workbook.add_format({'bold': True})
        # # # Write some data headers.
        # worksheet.write('A1', self.directory, bold)
        # worksheet.write('A2', 'Sample Number', bold)
        # worksheet.write('B2', 'Threshold', bold)
        # worksheet.write('C2', 'Density', bold)
        # # Start from the first cell. Rows and columns are zero indexed.
        # row = 2
        # col = 0
        # # Iterate over the data and write it out row by row.
        # for key, value in self.autodensity().items():
        #     worksheet.write(row, col, key.split(".")[0])
        #     worksheet.write(row, col + 1, autoimgs[key]['Threshold'])
        #     worksheet.write(row, col + 2, value)
        #     for a,w in enumerate(hist[key]['Counts']):
        #         worksheet.write(2, 5 + a, w)
        #     row += 1
        # workbook.close()
        