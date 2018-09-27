from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import numpy as np
import requests
import json
from django.http import HttpResponse
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

# Create your views here.

@require_http_methods(['POST','GET'])
def index(request):
    if request.method == "GET":
        return render(request,'overlay/test-image-overlay.html')
    elif request.method == "POST":
        coordX = request.POST['coordX']
        coordY = request.POST['coordY']
        
        
def save_image(data, fn, height, width,vmin,vmax,cm=0):
    sizes = np.shape(data)
     
    fig = plt.figure()
    fig.set_size_inches(width/height, 1, forward=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
 
    #ax.imshow(data, cmap=cm)
    ax.imshow(data,interpolation='bessel',vmin=vmin,vmax=vmax)
    plt.savefig(fn, dpi = height) 
    plt.close()

# including zoom_start,excluding zoom_end
def multiple_zoom_levels_images(data,zoom_start,zoom_end,directory,vmin,vmax):
    if len(data)/(2 ** zoom_end) < 1:
        raise RuntimeError("Ending zoom is too small.")
    if zoom_start > zoom_end:
        raise RuntimeError("Ending zoom must be larger than starting zoom")
    if len(data) != len(data[0]):
        raise RuntimeError("Width and height of data not equal")
        
    for zoom in range(zoom_start,zoom_end):
        divider = 2 ** zoom
        data_size = len(data)/divider
        
        for i in range(divider):
            for j in range(divider):
                filename = directory + "{}_{}_{}.jpg".format(zoom,i,j)
                zoom_data = data[int(i * data_size) : int((i + 1) * data_size), int(j * data_size) : int((j + 1) * data_size)]
                save_image(zoom_data,filename,256,256,vmin,vmax)
                
def generate_specific_image(data,coordY,coordX,zoom,directory,vmin,vmax):
    if coordX >= 2 ** zoom or coordY >= 2 ** zoom:
        raise RuntimeError("Coordinates are out of bounds")
    if coordX < 0 or coordY < 0:
        raise RuntimeError("Coordinates must be larger than 0")
    if len(data) != len(data[0]):
        raise RuntimeError("Width and height of data not equal")
        
    divider = 2 ** zoom
    data_size = len(data)/divider
    
    filename = directory + "{}_{}_{}.jpg".format(zoom,coordY,coordX)
    zoom_data = data[int(coordY * data_size) : int((coordY + 1) * data_size), int(coordX * data_size) : int((coordX + 1) * data_size)]
    save_image(zoom_data,filename,256,256,vmin,vmax)