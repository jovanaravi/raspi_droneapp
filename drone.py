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
    
    def freeze(self):
        logging.info('Freezing in a spot')        

    def close(self):
        self.vehicle.close()    