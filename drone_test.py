import argparse,configparser, time
from dronekit import connect, VehicleMode

parser = argparse.ArgumentParser()
parser.add_argument('--d', nargs=1, default=None)
args = parser.parse_args()

#application directory
APP_DIR = args.d[0] if args.d != None else "./"
CONFIGURATIONS = APP_DIR + 'configuration.ini'

#read a file
config = configparser.ConfigParser()

#protection 
if len(config.read(CONFIGURATIONS)) == 0:
    logging.error("Could Not Read Configurations File: " + CONFIGURATIONS)
    sys.exit() 

#variables from configuration file  
PIXHAWK = config['drone']['pixhawk']
BAUD_RATE = config['drone']['baud_rate']
PARAM = config['drone']['param']

vehicle = connect(PIXHAWK, baud= BAUD_RATE, wait_ready = True)

vehicle.mode = VehicleMode("GUIDED")   

vehicle.armed = True
time.sleep(1)
while not vehicle.armed:
    vehicle.armed = True
    time.sleep(1)

vehicle.simple_takeoff(3)
time.sleep(20)
while vehicle.mode.name != "LAND":
    vehicle.mode = VehicleMode("LAND")
    time.sleep(1)

print("Vehicle land successful")

