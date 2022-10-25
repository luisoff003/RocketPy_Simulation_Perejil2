from tkinter import Place
from rocketpy import Environment, SolidMotor, Rocket, Flight

class LaunchPlace:
    Latitude = 20.141352
    Longitude = -99.148987
    Elevation = 2200
    name = "ElSalitre"

#Setting up the simulation
Env = Environment(
    railLength=2.0, 
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

help(Rocket)

### CREATE THE MOTOR PEREJIL 2
PRJL2 = SolidMotor(
    thrustSource="Perejil_2_Thrust-Time.csv",        #CSV file must not contain headers/Column1=sec/Column2=T[N]
    burnOut=3.41,        #Time s
    grainNumber=5,
    grainSeparation=5/1000,
    grainDensity=1815,
    grainOuterRadius=59/1000,
    grainInitialInnerRadius=29/ 1000,
    grainInitialHeight=60/1000,
    nozzleRadius=40/1000,
    throatRadius=16/1000,
    interpolationMethod="linear",
)

# PRJL2.info()

###     CREATE THE ROCKET
Perejil2 = Rocket(
    motor=PRJL2,
    radius= 85.8/2000,
    mass = 5.222, #Without propellant in kg  PRJIL=1511g+1680g
    inertiaI=6.60,
    inertiaZ=0.03,
    distanceRocketNozzle=-1.255,
    distanceRocketPropellant=-0.85704,
    powerOffDrag=0.2,
    powerOnDrag=0.2,
) 

Perejil2.setRailButtons([0.2, -0.5])

NoseCone = Perejil2.addNose(length=0.55829, kind="ogive", distanceToCM=0.71971)

FinSet = Perejil2.addTrapezoidalFins(
    n=4,
    rootChord=0.120,
    tipChord=0.040,
    span=0.100,
    distanceToCM=-1.04956,
    cantAngle=0,
    radius=None,
    airfoil=None,
)

Tail = Perejil2.addTail(
    topRadius=0.0635, bottomRadius=0.0435, length=0.060, distanceToCM=-1.194656
)

def mainTrigger(p, y):
    # p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate main when vz < 0 m/s and z < 800 + 1400 m (+1400 due to surface elevation).
    return True if y[5] < 0 else False


Main = Perejil2.addParachute(
    "Main",
    CdS=10.0,
    trigger=mainTrigger,
    samplingRate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

TestFlight = Flight(rocket=Perejil2, environment=Env, inclination=85, heading=0)

TestFlight.allInfo()