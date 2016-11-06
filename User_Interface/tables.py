# tutorial/tables.py
import django_tables2 as tables
from .models import HEK_Observations
from .models import HMI_DataSeries

class HEK_Table(tables.Table):
    class Meta:
        model = HEK_Observations
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}

class HMI_Table(tables.Table):
	class Meta:
		model = HMI_DataSeries
		atrs = {'class': 'paleblue'}