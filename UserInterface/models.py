from django.db import models
import datetime

class HEK_Observations(models.Model):
    noaaNmbr = models.CharField(max_length = 40, default = 0, verbose_name = 'Noaa Number')
    dateAndTime = models.DateTimeField(max_length = 40, verbose_name = 'Date And Time')
    xcen = models.FloatField(max_length = 40, default = 0, verbose_name = 'X-Cen')
    ycen = models.FloatField(max_length = 40, default = 0, verbose_name = 'Y-Cen')
    xfov = models.FloatField(max_length = 40, default = 0, verbose_name = 'X-FOV')
    yfov = models.FloatField(max_length = 40, default = 0, verbose_name = 'Y-FOV')
    sciObj = models.CharField(max_length = 100, default = 'None recorded', verbose_name = 'Science Observations')

class HMI_DataSeries(models.Model):
    noaaNmbr = models.CharField(max_length = 40, default = 0, verbose_name = 'Noaa Number')
    dateAndTime = models.DateTimeField(max_length = 40, verbose_name = 'Date And Time')
    latMin = models.FloatField(max_length = 40, default = 0, verbose_name = 'Minimum Lat')
    latMax = models.FloatField(max_length = 40, default = 0, verbose_name = 'Maximum Lat')
    lonMin = models.FloatField(max_length = 40, default = 0, verbose_name = 'Minimum Long')
    lonMax = models.FloatField(max_length = 40, default = 0, verbose_name = 'Maximum Long')