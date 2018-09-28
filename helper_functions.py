from mapsplotlibV2 import *


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

test.data = mercator_faster(test.data)

print("\nmercator\n")

fig = plt.figure()
fig.set_size_inches(1, 1, forward=False)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)

ax.imshow(test.data,interpolation='bessel',vmin=test.vmin,vmax=test.vmax)
#plt.savefig(test.directory,dpi=1000) 



def row2lat(row):
  return 180.0/math.pi*(2.0*math.atan(math.exp(row*math.pi/180.0))-math.pi/2.0)

def mercator(geodetic):
    geo = np.repeat(geodetic, 2, axis=0)
    merc = np.zeros_like(geo)
    side = geo[0].size
    for row in range(side):
        lat = row2lat(180 - ((row * 1.0)/side) * 360)
        g_row = (abs(90 - lat)/180)*side
        fraction = g_row-math.floor(g_row)
        for col in range(side):
            high_row = geo[math.floor(g_row)][col] * (fraction)
            low_row = geo[math.ceil(g_row)][col] * (1-fraction)
            merc[row][col] = high_row + low_row
    return merc