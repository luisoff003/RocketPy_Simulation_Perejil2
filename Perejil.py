from tkinter import Place
from rocketpy import Environment, SolidMotor, Rocket, Flight

class LaunchPlace:
    Latitude = 20.141352
    Longitude = -99.148987
    Elevation = 2200
    name = "ElSalitre"

#Setting up the simulation
Env = Environment(
    railLength=5.2, 
    latitude = LaunchPlace.Latitude,
    longitude = LaunchPlace.Longitude, 
    elevation= LaunchPlace.Elevation
)


#Get weather data from the GFS forecast
import datetime

tomorrow = datetime.date.today() + datetime.timedelta(days=1)

Env.setDate((tomorrow.year, tomorrow.month, tomorrow.day, 12))  # Hour given in UTC time

#Tell the GFS forecast to get the atmopheric conditions for flight.
#Probably not all the wind speeds or atmosoheric temperatures are available.
Env.setAtmosphericModel(type="Forecast", file="GFS")

Env.info()      #To see what the weather will look like.


### CREATE THE MOTOR PEREJIL 2
Perejil2 = SolidMotor(
    thrustSource=250,  #".csv",        #CSV file must not contain headers/Column1=sec/Column2=T[N]
    burnOut=3.9,
    grainNumber=5,
    grainSeparation=5/1000,
    grainDensity=1815,
    grainOuterRadius=33/1000,
    grainInitialInnerRadius=15 / 1000,
    grainInitialHeight=120 / 1000,
    nozzleRadius=33 / 1000,
    throatRadius=11 / 1000,
    interpolationMethod="linear",
)

Perejil2.info()
