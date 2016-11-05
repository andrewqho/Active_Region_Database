from django.shortcuts import render
from django.http import HttpResponse
from pylab import figure, axes, pie, title
from matplotlib.backends.backend_agg import FigureCanvasAgg

from django.shortcuts import render_to_response

from django.template import loader

from django_tables2 import RequestConfig

import re
import ftplib
import os
from urllib.request import urlopen
import json
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Rectangle, Circle, PathPatch
from matplotlib.path import Path
from matplotlib.transforms import Affine2D
import numpy as np
import pylab
import sunpy.time
import numpy as np
from adjustText import adjust_text
import pandas as pd
from scipy import interpolate
import shutil

from .tables import HEK_Table

from mpld3 import plugins

from User_Interface import models

import matplotlib.pyplot as plt, mpld3

from django.views.decorators.csrf import csrf_exempt,csrf_protect

dateAndTimeHEK = []
xcen = []
ycen = []
xfov = []
yfov = []
sciObj = []

dateAndTimeHMI = []
latMin = []
latMax = []
lonMin = []
lonMax = []

@csrf_exempt

def getNumberOfEntries(hekJSON):
    return len(dateAndTimeHEK)

def getInfo(counter, hekJSON):
    for counter in range(len(hekJSON["Events"])):
        dateAndTimeHEK.append(hekJSON["Events"][counter]["startTime"])
        xcen.append(float("%.2f" % hekJSON["Events"][counter]["xCen"]))
        ycen.append(float("%.2f" % hekJSON["Events"][counter]["yCen"]))
        xfov.append(float("%.2f" % hekJSON["Events"][counter]["raster_fovx"]))
        yfov.append(float("%.2f" % hekJSON["Events"][counter]["raster_fovy"]))
        sciObj.append(hekJSON["Events"][counter]["sciObjectives"])

def sortHEK():
    for i in range(len(dateAndTimeHEK)):
        for j in range(len(dateAndTimeHEK)-1, i, -1):
            if ( dateAndTimeHEK[j] < dateAndTimeHEK[j-1]):
                temp1 = dateAndTimeHEK[j]
                dateAndTimeHEK[j] = dateAndTimeHEK[j-1]
                dateAndTimeHEK[j-1] = temp1

                temp2 = xcen[j]
                xcen[j] = xcen[j-1]
                xcen[j-1] = temp2

                temp3 = ycen[j]
                ycen[j] = ycen[j-1]
                ycen[j-1] = temp3

                temp4 = xfov[j]
                xfov[j] = xcen[j-1]
                xfov[j-1]=temp4

                temp5 = yfov[j]
                yfov[j] = ycen[j-1]
                yfov[j-1]=temp5

                temp6 = sciObj[j]
                sciObj[j] = sciObj[j-1]
                sciObj[j-1] = temp6

def createAnnotations(hekJSON, noaaNmbr):
    annotations = []
    for i in range(len(hekJSON['Events'])):
        annotations.append(dateAndTimeHEK[i])
        # annotations.append(dateAndTimeHEK[i] + ', ' + getLocation(i, noaaNmbr))

    return annotations

def fixAnnotations(annotations):
    texts = []
    for xt, yt, s in zip(xcen, ycen, annotations):
        texts.append(plt.text(xt, yt, s))
    return texts

def round_multiple(x, base):
    return int(base * round(float(x) / base)) 

def onclick(event):
    print( 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata))

def reset():
    del dateAndTimeHEK [:]
    del xcen [:]
    del ycen [:]
    del xfov [:]
    del yfov [:]
    del sciObj [:]

def makeGraph(hekJSON, noaaNmbr):
    fig, ax = plt.subplots(figsize=(8,8))
    # plt.plot(xcen, ycen, linestyle="dashed", color="red")
    # plt.plot(xcen, ycen, 'ro', color = 'blue')
    plt.plot(xcen, ycen, linestyle="dashed", color="red")
    plt.plot(xcen, ycen, 'ro', color = 'blue')
    # circle = Circle((0, 0), 980 , facecolor='none', edgecolor=(0, 0.8, 0.8), linewidth=3, alpha=0.5)

    # ax.add_patch(circle)
    ax.add_patch(Circle((0, 0), 980 , facecolor='none', edgecolor=(0, 0.8, 0.8), linewidth=3, alpha=0.5))
    ax.set_xlabel('X-Cen (HPC Arcseconds)')
    ax.set_ylabel('Y-Cen (HPC Arcseconds)')


    # for i in range(len(hekJSON['Events'])):
    #     if xfov[i] != 0:
    #         xStart = xcen[i] - (xfov[i]/2)
    #         yStart = ycen[i] - (yfov[i]/2)
    #         ax.add_patch(Rectangle((xStart, yStart), xfov[i], yfov[i], facecolor='none'))

    # ax.grid(True)
    plt.axis('equal')

    ax.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')

    ax.set_title("Active Region:" + " " + noaaNmbr, size=30)
    
    js_data = json.dumps(mpld3.fig_to_dict(fig))

    return js_data

def makeTable(hekJSON, noaaNmbr):
    if models.HEK_Observations.objects.filter(noaaNmbr=noaaNmbr).count() == 0:
        for i in range(len(hekJSON["Events"])):
            observation = models.HEK_Observations(noaaNmbr=noaaNmbr, 
                                                dateAndTime=dateAndTimeHEK[i], 
                                                xcen=xcen[i], 
                                                ycen=ycen[i], 
                                                xfov=xfov[i], 
                                                yfov=yfov[i], 
                                                sciObj=sciObj[i])
            observation.save()

    table = models.HEK_Observations.objects.filter(noaaNmbr=noaaNmbr)

    return table

def search(request):
    return render(request, 'search.html')

def empty(request, noaaNmbr):
    return render(request, 'empty.html')

def display(request, noaaNmbr):
    reset()

    urlData = 'http://www.lmsal.com/hek/hcr?cmd=search-events3&outputformat=json&instrument=IRIS&noaanum=' + noaaNmbr + '&hasData=true'

    webUrl = urlopen(urlData)
    counter = 0
    data = webUrl.read().decode('utf-8')
    hekJSON = json.loads(data)
    
    getInfo(counter, hekJSON)

    if len(dateAndTimeHEK) == 0:
        return render(request, 'empty.html')

    sortHEK()

    # urlDataJSOC = 'http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info'
    # for i in range(getNumberOfEntries()):
    #     JSOC_Dict = fetch.fetch('hmi.sharp_720s[]', start=stanfordJSOC.setLowerTimeBound(i), end_or_span=stanfordJSOC.setUpperTimeBound(i), keys=['NOAA_AR','T_OBS','LAT_MIN','LON_MIN','LAT_MAX','LON_MAX']) 
    #     stanfordJSOC.getInfo(i, JSOC_Dict, noaaNmbr)

    # sortHMI()

    return render(request, 'display.html', {"Graph": makeGraph(hekJSON, noaaNmbr), "Table": makeTable(hekJSON, noaaNmbr)})

