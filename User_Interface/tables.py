# tutorial/tables.py
import django_tables2 as tables
from .models import HEK_Observations

class HEK_Table(tables.Table):
    class Meta:
        model = HEK_Observations
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}