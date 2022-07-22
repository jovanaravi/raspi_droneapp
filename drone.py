import time, logging, netifaces
from dronekit import connect, VehicleMode, Command

class Drone:

    def __init__(self, config):

        PIXHAWK = config['drone']['pixhawk']
        BAUD_RATE =int(config['drone']['baud_rate'])
        PARAM = config['drone']['param']
        TAKEOFF_ALT = int(config['drone']['takeoff_alt'])

        #connect to vehicle
        try:
            self.vehicle = connect(PIXHAWK, baud= BAUD_RATE, wait_ready = True)
            logging.info('Connected to Flight Controller Hardware on:  %s ', PIXHAWK)
        except:
            logging.error('Connection with Flight Controller on: %s is not made', PIXHAWK)
        
        self.TAKEOFF_ALT = TAKEOFF_ALT
        self.STATE = "DISARMED"
        self.IS_ACTIVE = True
        logging.info('Drone Connected')
        
    def executeCommand(self, command):

        if command == 'TAKEOFF':
            print(command)

        if command == 'LAND':
            print(command)
        
        if command == 'RIGHT':
            print(command)

        if command == 'LEFT':
            print(command)
    
    def Get_lon(self):
        location = self.vehicle.location.global_frame
        first_split= str(location).split()
        a= first_split[0].split('=')
        b= a[2].split(",")
        lon = b[0]
        return lon
    def Get_lat(self):    
        location = self.vehicle.location.global_frame
        first_split= str(location).split()
        a= first_split[0].split('=')
        b= a[1].split(",")
        lat= b[0]
        return lat

    def freeze(self):
        logging.info('Freezing in a spot')        

    def close(self):
        self.vehicle.close()    