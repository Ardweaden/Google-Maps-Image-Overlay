import numpy as np
from PIL import Image
import math
import matplotlib.pyplot as plt

from testing_mapsplotlib import multiple_zoom_levels_images_full
from helper_functions import *


class Overlay:

	def __init__(self,zoom_start=0,zoom_end=22,directory="",data=None,borderLng=(-180,180),borderLat=(-85,85)):
		#######################################################################################################
		#	Initial values default at initilialisation, except if specified otherwise
		# 	All zoom levels, max longitude and latitude
		#	vmin,vmax parameters of the colormap
		#	Directory to which generated images will be saved
      #  Border latitude and longitude must always be in format (north,south),(west,east)
		#######################################################################################################
		self.zoom_start = zoom_start
		self.zoom_end = zoom_end
		self.directory = directory
		self.borderLng = borderLng
		self.borderLat = borderLat

		self._data = data

	@property
	def data(self):
		return self._data

	@data.setter
	def data(self, value):
		if value is not None:
			self.vmin = np.amin(value)
			self.vmax = np.amax(value)
			print("vmin set to",self.vmin,"and vmax set to",self.vmax)
		self._data = value

	def imageAsData(self,image_directory,size=None):
		#####################################################################################################################
		#	Imports image from directory and converts it to a 2D numpy array and assigns it as data
		#	RGB values are averaged to produce one value.
		#	TO DO: if image is not square
		#####################################################################################################################
		if size is not None:
			pass

		im = Image.open(image_directory)

		data = np.array(im)
		data = data.mean(axis=2)

		self.data = data

	def generateFullGlobe(self):
		####################################################################################################################
		#	Generates overlay for the full globe
		####################################################################################################################
		multiple_zoom_levels_images_full(self.data,self.zoom_start,self.zoom_end,self.directory,self.vmin,self.vmax)

	def generateWithBoundaries(self):
		####################################################################################################################
		#	Generates overlay with coordinate boundaries
		####################################################################################################################
		pass

	def dataToMercator(self,fullGlobe=False):
		####################################################################################################################
		#	Transforms geodetic data with Mercator projection (requires boundaries)
		#	User provides a picture in equirectangular projection and coordinates which it spans and border coordinates
		#	Except if data for the whole globe is provided
		#	Fuck this
		#	It will be assumed that the data is defined in the following way:
		#	Latitude difference x longitude difference with N points in between regardless of distances between points
		####################################################################################################################
		if fullGlobe:
			self.data = mercator_faster(self.data)
		else:
			pass




#test = Overlay()
#test.zoom_start = 1
#test.zoom_end = 4
#test.directory = "C:/Users/dis/Documents/JanJezersek/Google-Maps-Image-Overlay/images/test7/"
#test.imageAsData("C:/Users/dis/Documents/JanJezersek/Google-Maps-Image-Overlay/images/test7/test72.jpg")
#
#print(test.data)
#print(test.data.shape)
#
#test.data = mercator_faster(test.data)
#
#print("\nmercator\n")
#
#fig = plt.figure()
#fig.set_size_inches(1, 1, forward=False)
#ax = plt.Axes(fig, [0., 0., 1., 1.])
#ax.set_axis_off()
#fig.add_axes(ax)
#
#ax.imshow(test.data,interpolation='bessel',vmin=test.vmin,vmax=test.vmax)
#plt.savefig(test.directory,dpi=1000) 
