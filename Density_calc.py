""" Function to Determine Image Pixel Density for Microscopy Samples """
# Import relavent packages
import numpy as np
from pandas import DataFrame, ExcelWriter
import matplotlib.pyplot as plt
from cv2 import imread, cvtColor, COLOR_BGR2GRAY, THRESH_BINARY,THRESH_TRIANGLE
from cv2 import threshold as cv2threshold
from os import listdir
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
        for file in listdir(self.directory): # Loop over all files in directory
            # Extract Image files (JPG)
            if file.endswith(".JPG"):
                filelist.append(file)
        return filelist

    # Create method for reading image files
    def loadImages(self):
        imgrays = {}
        for image in self.fileList(): # Loop over images
            # Create variable for image
            im = imread(self.directory+'/'+ str(image))
            # Convert image Grayscale
            imgrays[image] = cvtColor(im, COLOR_BGR2GRAY)
        return imgrays
    # Method for calculating pixel density based on a selected threshold value
    def densities(self, threshold):
        Hist = {}
        Densities = {}
        for name, imgray in self.loadImages().items():
            counts, bins = np.histogram(imgray, range(256))
            # Store Histogram data in Dictionary
            Hist[name] = [[counts], [bins]]
            Total_Pixels = sum(counts)
            voids = 0
            # Loop over all bins and sum the total number of pixel below threshold value
            for a in range(1, int(threshold[name])):
                voids += counts[a]
            Density = 100 - voids / Total_Pixels * 100 # Phase density formula
            Densities[name] = Density
        return Densities

    def autoimage(self):
        # Create empty Dict to store Image and auto Threshold data
        autoImage = {}
        autoThresh = {}
        #Loop over images and obtain auto threshold data
        for name, imgray in self.loadImages().items():
            th3, ret3 = cv2threshold(imgray, 0, 255, THRESH_BINARY + THRESH_TRIANGLE)
            autoImage[name] = ret3
            autoThresh[name] = th3
        return autoImage, autoThresh

    def manimage(self, threshold=110):
        # Create empty Dict to store Image and manual Threshold data
        manImage = {}
        manThresh = {}
        # Loop over images and obtain manual threshold data
        for name, imgray in self.loadImages().items():
            thresh1, ret = cv2threshold(imgray, threshold, 255, THRESH_BINARY)
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
        return hist_data
    
    def graph_plot(self):
        for im_name, data in self.histogram_plot().items():
            bins = data['Bins']
            counts = data['Counts']
            plt.figure(im_name)
            plt.bar(bins[:-1] - 0.5, counts,
                    width=1, edgecolor='none')
            plt.xlim([-0.5, 255.5])
            plt.title(im_name)
            plt.show()

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
            ex_df = DataFrame(density_data).transpose()
            ex_df.columns = ['Auto Density', 'Auto Threshold', 'Manual Density', 'Manual Threshold']
            ex_df.index.name = 'Sample Number'
        elif auto_option and not man_option:
            density_data = [self.autodensity(),self.autoimage()[1]]
            ex_df = DataFrame(density_data).transpose()
            ex_df.columns = ['Auto Density', 'Auto Threshold']
            ex_df.index.name = 'Sample Number'
        else:
            density_data = [self.mandensity(threshold),self.manimage(threshold)[1]]
            ex_df = DataFrame(density_data).transpose()
            ex_df.columns = ['Manual Density', 'Threshold']
            ex_df.index.name = 'Sample Number'

        stats = DataFrame(ex_df.describe())
        stats.index.name = 'Statistics Summary'
        hist_out= DataFrame([hist[i]['Counts'] for i in hist.keys()], index = hist.keys())
        hist_out.rename_axis('Histogram Bins:', inplace=True)
        hist_out.rename_axis('Histogram Data', axis = 1, inplace = True)
        # Create a workbook and add a worksheet.
        try:
            book = load_workbook(filename)
            writer = ExcelWriter(filename, engine='openpyxl')
            writer.book = book
        except FileNotFoundError:
            # Create a Pandas Excel writer using XlsxWriter as the engine.
            writer = ExcelWriter(filename, engine='xlsxwriter')
        # Position the dataframes in the worksheet.
        folder_name = self.directory.split('/')
        ex_df.to_excel(writer, sheet_name=folder_name[-1], index=True)  # Default position, cell A1.
        stats.to_excel(writer, sheet_name=folder_name[-1], index=True, startcol=len(ex_df.columns)+2)
        hist_out.to_excel(writer, sheet_name=folder_name[-1], startcol=len(ex_df.columns)+len(stats.columns)+4)
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

        