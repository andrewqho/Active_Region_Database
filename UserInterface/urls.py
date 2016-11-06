from django.conf.urls import url, include
from UserInterface import views

urlpatterns = [
 	# url(r'^search/(?P<noaaNmbr>[0-9]{5})', views.display, name = 'display'),

    url(r'^ActiveRegionDatabase/(?P<noaaNmbr>[0-9]{5})', views.display, name = 'display'),
    url(r'^ActiveRegionDatabase', views.search, name = 'search'),
    # url(r'^ActiveRegionDatabase/search/(?P<noaaNmbr>)', views.empty, name = 'empty'),
]