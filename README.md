# Welcome to PyFlora!

This little piece of software was made as a "final paper" for the Algebra Python course.

## Howto and Features

### Running the application
All the necessary modules and exact versions are located in requirements.txt

If you are opening this project in a compatible IDE it will ask you to install modules automatically.

When running this application I was always using Python venv so modules are not installed in the root of my OS

The default database is generated for you but if you wish you can re-generate it by executing generate_db.py

You run the application by running main.py
### Login
With the default database, you can log in with admin/admin1234 or for example goran/goran1234

### Main Screen
When you log in you will see the main welcome screen.

You will see Location, Latitude, and Longitude information which is stored in the database.

You can also see a graph with a daily forecast for your location based on Latitude and Longitude. This information is fetched from online API.

By changing these values in Admin Panel, graph data will change.

Note that only the admin user can see and access Admin Panel
### Admin Panel and My Profile
If you press on My Profile, you will be taken to the page where you can see and edit your information. Only admin can change passwords.

If you are logged in as admin and you access the admin panel you will see sections for application configuration and user administration.

Application Configuration parameters can be changed but you cannot leave them empty.

Users can be created, deleted, or edited. You cannot create a user with an empty username or password, or even set the empty password on an existing user.
### Plants
In the plants section, you can add new, edit, or delete plants.

When adding a new or editing an existing plant, all the parameters except the Description must be entered.

Measurement parameters must be entered as int or float depending on the measurement.

You cannot create multiple plants with the same name.
### Pots
There are multiple features of the Pots section.

You create a new pot with a unique Name and Description, after creation, only the description can be edited.

When Pot is created you can attach a plant to it. When attached, Pot will assume a picture of the plant and 1 entry of the sensor measurement data will be generated.

You can also detach the Plant from the Pot, when you attach it again to some Plant, 1 new measurement entry will be created again for the Pot.

In the table, if your simulated sensor readings are not in the range of min and max values of the plant, it will show Not OK in red color, else it will show green OK.

If you press on the "Sync with Sensor" button, 1 entry of the sensor data will be generated for your current datetime with random values.

If you press the "Fix Plant" button, this will simulate that you made all the necessary steps to fix the Plant in the
Pot and new measurement data will be created which is in the range of min and max values for the Plant measurements.

If you delete the Pot, all measurements will be deleted also.

By pressing on Graphs you can see line and bar (column) graphs with the last 5 measurement entries for the Pot.
