# Active_Region_Database

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
