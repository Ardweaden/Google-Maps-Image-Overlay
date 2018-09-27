# -*- coding: utf-8 -*-
"""
Created on Sat May 19 20:32:26 2018

@author: Jan Jezersek
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import math
from PIL import Image
import os
import random

# x, y = np.mgrid[-1:1:200j, -1:1:200j]
# z = (x+y) * np.exp(-6.0*(x*x+y*y))
# vmin = np.amin(z)
# vmax = np.amax(z)

####################################################################################################
#    User enters either border longitudes and latitudes, or center point and dimensions of rectangle
#    User inputs desired image or data to be overlayed and zoom range
#    Later add the option to cover the whole world with an image
####################################################################################################

def save_image(data, fn, height, width,vmin,vmax,cm=0):
    sizes = np.shape(data)
    
    print(sizes)
     
    fig = plt.figure()
    fig.set_size_inches(width/height, 1, forward=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
 
    #ax.imshow(data, cmap=cm)
    ax.imshow(data,interpolation='bessel',vmin=vmin,vmax=vmax)
    print("saving ....")
    plt.savefig(fn, dpi = height) 
    plt.close()
    
def calculate_tile_coord(X,Y,zoom):
    scale = 2 ** zoom
    a = math.sin(X * math.pi / 180)
    a = min(max(a, -0.9999), 0.9999)
    worldX = 256 * (0.5 + Y / 360)
    worldY = 256 * (0.5 - math.log((1 + a) / (1 - a)) / (4 * math.pi))
    return math.floor(worldX * scale/ 256), math.floor(worldY * scale / 256)

def calculate_latLng_from_tile(X,Y,zoom):
    lng1 = (X / 2**zoom) * 360.0 - 180.0
    lng2 = ((X + 1) / 2**zoom) * 360.0 - 180.0
    
    an   = math.pi - 2.0 * math.pi * Y / 2.0**zoom
    lat1 = 180.0 / math.pi * math.atan(0.5 * (math.exp(an)-math.exp(-an)))
    an   = math.pi - 2.0 * math.pi * (Y + 1.0) / 2.0**zoom
    lat2 = 180.0 / math.pi * math.atan(0.5 * (math.exp(an)-math.exp(-an)))
    return (lng1,lng2),(lat1,lat2)

def calculate_pixel_coordinates(lat,lng,zoom):
    return math.floor(lat * 2**zoom),math.floor(lng * 2**zoom)
    
def multiple_zoom_levels_images_area(data,zoom_start,zoom_end,centerX,centerY,directory,vmin,vmax):
    if len(data)/(2 ** (zoom_end-zoom_start)) < 1:
        raise RuntimeError("Ending zoom is too small.")
    if zoom_start > zoom_end:
        raise RuntimeError("Ending zoom must be larger than starting zoom")
    if len(data) != len(data[0]):
        raise RuntimeError("Width and height of data not equal")
        
    startTileX,startTileY = calculate_tile_coord(centerX,centerY,zoom_start)
        
    for zoom in range(0,zoom_end-zoom_start):
        divider = 2 ** zoom
        data_size = len(data)/divider
        
        for i in range(divider):
            for j in range(divider):
                filename = directory + "{}_{}_{}.jpg".format(zoom_start + zoom,startTileY + i,startTileX + j)
                print(filename)
                zoom_data = data[int(i * data_size) : int((i + 1) * data_size), int(j * data_size) : int((j + 1) * data_size)]
                save_image(zoom_data,filename,256,256,vmin,vmax)
        
        startTileX = 2 * startTileX
        startTileY = 2 * startTileY

# including zoom_start,excluding zoom_end for the entire world
def multiple_zoom_levels_images_full(data,zoom_start,zoom_end,directory,vmin,vmax):
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


def multiple_zoom_levels_images_area2(data,zoom_start,zoom_end,borderLng,borderLat,directory,vmin,vmax):
    if len(data)/(2 ** (zoom_end-zoom_start)) < 1:
        raise RuntimeError("Ending zoom is too small.")
    if zoom_start > zoom_end:
        raise RuntimeError("Ending zoom must be larger than starting zoom")
    if len(data) != len(data[0]):
        raise RuntimeError("Width and height of data not equal")
        
    # 1 upper right and then clockwise from there
        
#    startTile1X,startTile1Y = calculate_tile_coord(borderLng[0],borderLat[1],zoom_start)
#    startTile2X,startTile2Y = calculate_tile_coord(borderLng[1],borderLat[1],zoom_start)
#    startTile3X,startTile3Y = calculate_tile_coord(borderLng[1],borderLat[0],zoom_start)
#    startTile4X,startTile4Y = calculate_tile_coord(borderLng[0],borderLat[0],zoom_start)
    
#    startTile1 = calculate_tile_coord(borderLng[0],borderLat[1],zoom_start)
#    startTile2 = calculate_tile_coord(borderLng[1],borderLat[1],zoom_start)
#    startTile3 = calculate_tile_coord(borderLng[1],borderLat[0],zoom_start)
#    startTile4 = calculate_tile_coord(borderLng[0],borderLat[0],zoom_start)
    
    startTile3 = calculate_tile_coord(borderLat[0],borderLng[1],zoom_start)
    startTile2 = calculate_tile_coord(borderLat[1],borderLng[1],zoom_start)
    startTile1 = calculate_tile_coord(borderLat[1],borderLng[0],zoom_start)
    startTile4 = calculate_tile_coord(borderLat[0],borderLng[0],zoom_start)
    
    tiles = [startTile1,startTile2,startTile3,startTile4]
    
    print(tiles)
    print(borderLat,borderLng)
    tileBorders = []
    
    for i in range(len(tiles)):
        tileBorders.append(calculate_latLng_from_tile(tiles[i][0],tiles[i][1],zoom_start))
        
    print(tileBorders)
            
    t1 = calculate_pixel_coordinates(borderLng[0],borderLat[1],zoom_start)
    t2 = calculate_pixel_coordinates(borderLng[1],borderLat[0],zoom_start)
    
    pixel_width = t2[0] - t1[0]
    pixel_height = t1[1] - t2[1]
    
    print("Pixel width: ",pixel_width," ---- Pixel height: ",pixel_height)
    
    # We calculated the actual pixel width and height of the area we want to cover
    # Generally, the pixel size of image from data will be the same dimensions as the data itself
    # Thus we calculate the ration of the actual size to the full size, so we can scale it down
    # Generally the width and height ratios should be the same, but not necessarily
    ### NTS raise warning if the ratios aren't the same
    
    full_pixel_height,full_pixel_width = data.shape
    
    width_ratio = pixel_width / full_pixel_width
    height_ratio = pixel_height / full_pixel_height
    
    generate_area_images(data,directory,tiles,tileBorders,borderLng,borderLat,zoom_start,width_ratio,height_ratio)
        
    print("Pixel height: ",pixel_height," and pixel width: ",pixel_width)
        
    print(tiles)
    print("\n")
    print(tileBorders)    
        
    # Now I need to calculate which pixels I should plot for each tile
    
    if 1:
        return
                
    for zoom in range(0,zoom_end-zoom_start):
        divider = 2 ** zoom
        data_size = len(data)/divider
        
        for i in range(divider):
            for j in range(divider):
                filename = directory + "{}_{}_{}.jpg".format(zoom_start + zoom,startTileY + i,startTileX + j)
                print(filename)
                zoom_data = data[int(i * data_size) : int((i + 1) * data_size), int(j * data_size) : int((j + 1) * data_size)]
                save_image(zoom_data,filename,256,256,vmin,vmax)
        
        startTileX = 2 * startTileX
        startTileY = 2 * startTileY
        
def generate_area_images(data,directory,tiles,tileBorders,borderLng,borderLat,zoom,width_ratio,height_ratio):
    print("\n\nRunning image generation ....\n")
    tiles = list(set(tiles))
    tileBorders = list(set(tileBorders))
    full_tiles = []
    full_tileBorders = []
    
    minX = np.amin(np.array(tiles)[:,1])
    minY = np.amin(np.array(tiles)[:,0])
    maxX = np.amax(np.array(tiles)[:,1])
    maxY = np.amax(np.array(tiles)[:,0])
    
    for x in range(minX,maxX + 1):
        for y in range(minY,maxY + 1):
            full_tiles.append((y,x))
            
    for i in range(len(full_tiles)):
        full_tileBorders.append(calculate_latLng_from_tile(full_tiles[i][0],full_tiles[i][1],zoom))
    
    tiles = full_tiles
    tileBorders = full_tileBorders
    
    print("Full tiles:",tiles,"\nFull tile borders: ",tileBorders,"\n")
    
    for i,tile in enumerate(tiles):
        #WE_counter, NS_counter: from where to where data spans
        north,west = calculate_pixel_coordinates(borderLat[1],borderLng[0],zoom)
        south,east = calculate_pixel_coordinates(borderLat[0],borderLng[1],zoom)
        northTile,westTile = calculate_pixel_coordinates(tileBorders[i][1][1],tileBorders[i][0][1],zoom)
        southTile,eastTile = calculate_pixel_coordinates(tileBorders[i][1][0],tileBorders[i][0][0],zoom)
        
        print("Tile height: ",southTile - northTile," ==== Tile width: ",westTile - eastTile)
        
        print(tileBorders[i][0][1],tileBorders[i][1][1])
        
        print("North, west, south, east: ",north,west,south,east,"\n")
        
        print("North tile: ",northTile)
        print("West tile: ",westTile)
        
        if tileBorders[i][1][0] >= borderLat[1] and tileBorders[i][1][1] < borderLat[0]:
            print("==== data is fully inside the tile latitude-wise ====")
            # data is fully inside the tile latitude-wise
            # set NS_counter
            NS_counter = [north - northTile,south - northTile]
        elif tileBorders[i][1][0] >= borderLat[1] and tileBorders[i][1][1] > borderLat[0]:
            print("==== northern border of data is in tile, southern spans further south ====")
            # northern border of data is in tile, southern spans further south
            # set NS_counter
            NS_counter = [north - northTile,north - south]
        elif tileBorders[i][1][0] <= borderLat[1] and tileBorders[i][1][1] < borderLat[0]:
            print("==== southern border of data is in tile, northern spans further north ====")
            # southern border of data is in tile, northern spans further north
            # set NS_counter
            NS_counter = [0,south - northTile]
        else:
            print("==== borders of data are fully outside the tile and thus spans the whole tile latitude-wise ====")
            # borders of data are fully outside the tile and thus spans the whole tile latitude-wise
            NS_counter = [0,north - south]
            
        
        if tileBorders[i][0][1] <= borderLng[1] and tileBorders[i][0][0] > borderLng[0]:
            print("==== data is fullt inside the tile longitude-wise ====")
            # data is fullt inside the tile longitude-wise
            # set WE_counter
            WE_counter = [westTile - west,east - westTile]
        elif tileBorders[i][0][1] >= borderLng[1] and tileBorders[i][0][0] > borderLng[0]:
            print("==== eastern border of data is in tile, western spans further west ====")
            # eastern border of data is in tile, western spans further west
            # set WE_counter
            WE_counter = [0,westTile - east]
        elif tileBorders[i][0][1] <= borderLng[1] and tileBorders[i][0][0] < borderLng[0]:
            print("==== western border of data is in tile, eastern spans further east ====")
            # western border of data is in tile, eastern spans further east
            # set WE_counter
            WE_counter = [westTile - west,east - west]
        else:
            print("==== borders of data are fully outside the tile and thus spans the whole tile longitude-wise ====")
            # borders of data are fully outside the tile and thus spans the whole tile longitude-wise
            WE_counter = [0,east - west]
            
        print("\nNS counter: ",NS_counter)
        print("WE counter: ",WE_counter,"\n")
        
        print(tile)
        
        filename = "{}_{}_{}.png".format(zoom,tile[1],tile[0])
        
        
        
        #image_data = data[int(NS_counter[0]/height_ratio):int(NS_counter[1]/height_ratio),int(WE_counter[0]/width_ratio):int(WE_counter[1]/width_ratio)]
        #image_data = data[int(NS_counter[0]/height_ratio):int((southTile - northTile - NS_counter[1])/height_ratio),int(WE_counter[0]/width_ratio):int((westTile - eastTile - WE_counter[1])/width_ratio)]
        image_data = data
        print("Image data shape: ",image_data.shape)
        
        print("\n",str(int(NS_counter[0]/height_ratio)),":",str(int((southTile - northTile - NS_counter[1])/height_ratio)),", ",str(int(WE_counter[0]/width_ratio)),":",str(int((westTile - eastTile - WE_counter[1])/width_ratio)),"\n")
        
        create_edge_image(directory,filename,image_data,NS_counter,WE_counter,vmin,vmax,width_ratio,height_ratio)

def create_edge_image(directory,filename,data,NS_counter,WE_counter,vmin,vmax,width_ratio,height_ratio,background_size=(256,256)):
    a = np.zeros(background_size)
    
    #print(data.shape)
    
    fig = plt.figure()
    fig.set_size_inches(256/256, 1, forward=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
     
    ax.imshow(a,alpha=0)
    print("saving background ....")
    ### NTS create generator directory if it doesn't exist
    plt.savefig("images/generator/background.png",dpi = 256,transparent=True)
    plt.close()
    
    
    fig = plt.figure()
    fig.set_size_inches(width_ratio/height_ratio,1.0,forward=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    print(width_ratio,data.shape)
     
    ax.imshow(data,interpolation='bessel',vmin=vmin,vmax=vmax)
    print("saving foreground ....")
    print("Width ratio: ",width_ratio,", data width: ",data.shape[0])
    plt.savefig("images/generator/foreground.png",dpi = data.shape[0]/width_ratio)
    plt.savefig("images/generator/foreground" + str(random.randint(10000,99999)) + ".png",dpi = data.shape[0]/width_ratio)
    plt.close()
    
    print("\nImage size: ",fig.get_size_inches(),"\n")
    #print("\nImage size: ",np.array(fig.get_size_inches())/np.array([width_ratio,height_ratio]),"\n")
    
    background = Image.open("images/generator/background.png")
    foreground = Image.open("images/generator/foreground.png")
    
    background.paste(foreground, (WE_counter[0], NS_counter[0]), foreground)
    
    print(filename)
    
    background.save(directory + filename)
    
    background.close()
    foreground.close()
        
#    os.remove("images/generator/background.png")
#    os.remove("images/generator/foreground.png")
    
    
#create_edge_image("images/testJoin2/","test.png",z,NS_counter,WE_counter,vmin,vmax)

#im = Image.open("C:/Users/dis/Documents/JanJezersek/Google-Maps-Image-Overlay/images/test5/test5.jpg")
# im = Image.open("C:/Users/dis/Documents/JanJezersek/Google-Maps-Image-Overlay/images/test4/test4.png")

# # sqrWidth = np.ceil(np.sqrt(im.size[0]*im.size[1])).astype(int)
# # im = im.resize((sqrWidth, sqrWidth))
# print(im.size)
# data = np.array(im)
# data = data.mean(axis=2)
# vmin = np.amin(data)
# vmax = np.amax(data)

        
# #multiple_zoom_levels_images_full(data,1,4,"C:/Users/dis/Documents/JanJezersek/Google-Maps-Image-Overlay/images/test5/",vmin,vmax)
# multiple_zoom_levels_images_area2(data,1,4,(-180,180),(-75,83.7),"C:/Users/dis/Documents/JanJezersek/Google-Maps-Image-Overlay/images/test4/",vmin,vmax)