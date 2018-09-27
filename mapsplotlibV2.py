import numpy as np
from PIL import Image
import math
import matplotlib.pyplot as plt

from testing_mapsplotlib import multiple_zoom_levels_images_full


class Overlay:

	def __init__(self,zoom_start=0,zoom_end=22,directory="",data=None,borderLng=(-180,180),borderLat=(-85,85)):
		#######################################################################################################
		#	Initial values default at initilialisation, except if specified otherwise
		# 	All zoom levels, max longitude and latitude
		#	vmin,vmax parameters of the colormap
		#	Directory to which generated images will be saved
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

	def dataToMercator(self):
		####################################################################################################################
		#	Transforms geodetic data with Mercator projection (requires boundaries)
		####################################################################################################################
		pass




test = Overlay()
test.zoom_start = 1
test.zoom_end = 4
test.directory = "C:/Users/dis/Documents/JanJezersek/Google-Maps-Image-Overlay/images/test7/"
test.imageAsData("C:/Users/dis/Documents/JanJezersek/Google-Maps-Image-Overlay/images/test7/test72.jpg")

print(test.data)
print(test.data.shape)

def row2lat(row):
  return 180.0/math.pi*(2.0*math.atan(math.exp(row*math.pi/180.0))-math.pi/2.0)

def mercator_faster(geodetic):
    geo = np.repeat(geodetic, 2, axis=0)
    merc = np.zeros_like(geo)
    side = geo[0].size
    for row in range(side):
        lat = row2lat((180 - ((row * 1.0)/side) * 360))
        g_row = (abs(90 - lat)/180)*side
        fraction = g_row-math.floor(g_row)
        high_row = geo[math.floor(g_row), :] * (fraction)
        low_row = geo[math.ceil(g_row), :] * (1-fraction)
        merc[row, :] = high_row + low_row

    return merc

test.data = mercator_faster(test.data)

print("\nmercator\n")

fig = plt.figure()
fig.set_size_inches(1, 1, forward=False)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)

ax.imshow(test.data,interpolation='bessel',vmin=test.vmin,vmax=test.vmax)
plt.savefig(test.directory,dpi=1000) 