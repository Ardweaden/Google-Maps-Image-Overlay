from mapsplotlibV2 import *


def calculate_tile_coord(X,Y,zoom):
    ##########################################################################
    #   X: latitude
    #   Y: longitude
    #   zoom level
    ##########################################################################
    scale = 2 ** zoom
    a = math.sin(X * math.pi / 180)
    a = min(max(a, -0.9999), 0.9999)
    worldX = 256 * (0.5 + Y / 360)
    worldY = 256 * (0.5 - math.log((1 + a) / (1 - a)) / (4 * math.pi))
    return math.floor(worldX * scale/ 256), math.floor(worldY * scale / 256)

def covered_tiles(borderLat,borderLng,zoom):
    ##########################################################################
    #   Returns all tiles, covered by data
    #   Maximum borderLat ==> (85,-85)
    #   Tile is [longitude (x), latitude (y)]
    ##########################################################################    
    startTile2 = calculate_tile_coord(borderLat[0],borderLng[0],zoom)
    startTile1 = calculate_tile_coord(borderLat[0],borderLng[1],zoom)
    startTile4 = calculate_tile_coord(borderLat[1],borderLng[0],zoom)
    startTile3 = calculate_tile_coord(borderLat[1],borderLng[1],zoom)
    
    tiles = [startTile1,startTile2,startTile3,startTile4]
        
    minX = tiles[0][0]
    maxX = tiles[1][0]
    minY = tiles[0][1]
    maxY = tiles[2][1]

    borders = [minX,maxX,minY,maxY]

    for latitude in range(minX,maxX+1):
        for longitude in range(minY,maxY+1):
            if (latitude,longitude) not in tiles:
                tiles.append((latitude,longitude))
    
    return tiles,borders

def calculate_latLng_from_tile(X,Y,zoom):
    ##########################################################################
    #   Calculates border longitudes and latitudes of a tile
    ##########################################################################
    lng1 = (X / 2**zoom) * 360.0 - 180.0
    lng2 = ((X + 1) / 2**zoom) * 360.0 - 180.0
    
    an   = math.pi - 2.0 * math.pi * Y / 2.0**zoom
    lat1 = 180.0 / math.pi * math.atan(0.5 * (math.exp(an)-math.exp(-an)))
    an   = math.pi - 2.0 * math.pi * (Y + 1.0) / 2.0**zoom
    lat2 = 180.0 / math.pi * math.atan(0.5 * (math.exp(an)-math.exp(-an)))
    return (lng1,lng2),(lat1,lat2)

def pad_data_to_tiles(data,borderLat,borderLng,zoom):
    ##########################################################################
    #   Pads zeros to data, so that data borders align with tile borders
    ##########################################################################
    lat_dif = borderLat[0] - borderLat[1]
    lng_dif = borderLng[0] - borderLng[1]
    
    tiles = covered_tiles(borderLat,borderLng,zoom)[:4]
    
    coord_1 = calculate_latLng_from_tile(tiles[0][0],tiles[0][1],zoom)
    coord_4 = calculate_latLng_from_tile(tiles[3][0],tiles[3][1],zoom)
    
    lat_dif_tiles = coord_1[0][0] - coord_4[0][1]
    lng_dif_tiles = coord_1[1][0] - coord_4[1][1]
    
    data_x,data_y = data.shape
    
    lat_y = data_y/lat_dif
    lng_x = data_x/lng_dif
    
    # now calculate paddding rows to add to each side
    padding_left = int((coord_1[0][0] - borderLng[0])*lng_x)
    padding_right = int((coord_4[0][1] - borderLng[1])*lng_x)
    padding_top = int((coord_1[1][0] - borderLat[0])*lat_y)
    padding_bottom = int((coord_4[1][1] - borderLat[1])*lat_y)
    

def row2lat(row):
  return 180.0/math.pi*(2.0*math.atan(math.exp(row*math.pi/180.0))-math.pi/2.0)

def mercator_faster(geodetic):
    print(geodetic.shape)
    geo = np.repeat(geodetic, 2, axis=0)
    print("geo:\n",geo)
    print(geo.shape)
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








#test = Overlay()
#test.zoom_start = 1
#test.zoom_end = 4
#test.directory = "C:/Users/dis/Documents/JanJezersek/Google-Maps-Image-Overlay/images/test7/"
#test.imageAsData("C:/Users/dis/Documents/JanJezersek/Google-Maps-Image-Overlay/images/test7/test72.jpg")
#
#print(test.data)
#print(test.data.shape)
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
##plt.savefig(test.directory,dpi=1000) 



