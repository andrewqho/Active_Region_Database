# The Active Region Database

This project uses Django, a python webframework, Matplotlib, a popular python plotting library that mimics Matlab's capabilities, and MPLD3, a useful library that allows the conversion of Matplotlib plots into javascript, to provide a clean active region database. 

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

    (http example server)/ActiveRegionDatabase

After completing the following instructions, you are free to try out the database!

# How the code works:

Django acts as a bridge between the client side, which uses HTML, and the server side, which runs on Python. In the python script, data is sent to the HTML files known as templates. 

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

"Search" is defined as the following:

    def search(request):
        return render(request, 'search.html')
        
Django uses the built-in function "render" to send data to the HTML file, search.html. The request, taken from sending the url data to the server, is returned to the template "search.html" to be shown in the browser.

"Display" is defined as the following:

    def display(request, noaaNmbr):
        reset()

        urlData = 'http://www.lmsal.com/hek/hcr?cmd=search-events3&outputformat=json&instrument=IRIS&noaanum=' + noaaNmbr + '&hasData=true'

        webUrl = urlopen(urlData)
        counter = 0
        data = webUrl.read().decode('utf-8')
        hekJSON = json.loads(data)

        getInfoHEK(counter, hekJSON)

        if len(dateAndTimeHEK) == 0:
            return render(request, 'empty.html')

        sortHEK()

        urlDataJSOC = 'http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info'
        for i in range(len(dateAndTimeHEK)):
            JSOC_Dict = fetch.fetch('hmi.sharp_720s[]', start=stanfordJSOC.setLowerTimeBound(i), end_or_span=stanfordJSOC.setUpperTimeBound(i), keys=['NOAA_AR','T_OBS','LAT_MIN','LON_MIN','LAT_MAX','LON_MAX']) 
            print(JSOC_Dict)
            stanfordJSOC.getInfoHMI(i, JSOC_Dict, noaaNmbr)

        sortHMI()

        print(dateAndTimeHMI)

        return render(request, 'display.html', {"Graph": makeGraph(noaaNmbr), "Table": makeTable(noaaNmbr)})

Display is invoked after an Active region is submitted. To pull data to create the graph and the table, it accesses a URL from IRIS that ouputs a JSON file of metadata, and uses the entries within the JSON to extract HMI observations that are closest to the IRIS observations for the active region. The data is stored within the following global array-lists.

    #IRIS Data
    dateAndTimeHEK = []
    xcen = []
    ycen = []
    xfov = []
    yfov = []
    sciObj = []

    # HMI Sharp Data Series
    dateAndTimeHMI = []
    latMin = []
    latMax = []
    lonMin = []
    lonMax = []

After the data is stored within the arrays, they are used in the functions makeGraph and makeTable.

makeGraph is a simple function that uses Matplotlib and MPLD3 to create a plot using the data in the array lists.

makeTable uses a key attribute of Django: Models

Models make use of the built-in SQLite Database provided with every Django project. Within models.py, there are two different classes: HEK_Observation and HMI_DataSeries. Whenever a new active region(not searched before) is inputed, the code will add the corresponding entries into the database for later usage. When an active region is searched, the code searches through the database first to see if any entries for the active region already exist. If not, then a new set of database entries are created.

After both the table and the graph are created, they are packaged into JSON dicts and the data is sent to the template, where they are rendered within the templates.
