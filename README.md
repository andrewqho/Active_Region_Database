# The Active Region Database

This project uses Django and Matplotlib to provide a simple, clean active region database. 

To look up an active region, simply input the NOAA ID number of an active region to view a graph displaying all relavant IRIS and HMI Observations with an accompanying sortable table with relevant information. The graph is interactive, and you can zoom, select points, and change the color scheme.

# Running the code:

As of right now, the website is still in production, so to test the website, several steps are required.

First, install Django. You can follow the instructions provided at the following link:
https://docs.djangoproject.com/en/1.10/intro/install/

Second, install matplotlib. You can follow the instructions provided at the following link:
http://matplotlib.org/faq/installing_faq.html

After downloading the necessary materials, navigate the project's directory in your command line, and input the following command:

python manage.py makemigrations

After migrations have been made, input the following command:
python manage.py migrate

Finally, to locally host the website, input the following command:
python manage.py runserver

After the file "manage.py" confirms there are no errors, copy the given server into your local host and navigate to the local server. After the server name, type the following url:

(http example server)/Active Region Database

After completing the following instructions, you are free to try out the database!

# How the code works:

Django uses several directories known as "apps" to run. Within the code, I have two apps: "User_Interface" and "Utility". 

"Utility" contains all the configuration files necessary for Django to properly read other "apps". 

In User_Interface, there are several scripts that run. First, when the webpage is pulled up, the file "urls.py" uses regular expressions to invoke a different methods within the file, "views.py". Within "urls.py", there are 2 different urls possible:
/ActiveRegionDatabase/ or /ActiveRegionDatabase/NoaaNumber

The start page, "/ActiveRegionDatabase/" takes a simple user request and outputs the graph of the corresponding active region.
In urls.py, you see the following line of code:
    
    url(r'^ActiveRegionDatabase/(?P<noaaNmbr>[0-9]{5})', views.display, name = 'display'),
    url(r'^ActiveRegionDatabase', views.search, name = 'search'),

Essentially, this line of code dictates how the program runs based off of the URL:
1. If the URL matches "/ActiveRegionDatabase", then invoke the method "search" within view.py
2. If the URL matches "/ActiveRegionDatabase/someNOAAnumber", then invoke the method "display" within views.py

Within views.py, there are two major functions that can be invoked: search and display

Search is defined as the following:

    def search(request):
        return render(request, 'search.html')
        
Django uses the built-in function "render" to send data to the HTML file, search.html. The request, taken from sending the url data to the server, is returned to the html file to be shown in the browser.
