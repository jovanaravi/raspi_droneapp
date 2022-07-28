import time, logging, netifaces
from dronekit import connect, VehicleMode, Command
from pymavlink import mavutil

class Drone:

    def __init__(self, config):

        PIXHAWK = config['drone']['pixhawk']
        BAUD_RATE =int(config['drone']['baud_rate'])
        PARAM = config['drone']['param']
        TAKEOFF_ALT = int(config['drone']['takeoff_alt'])
        GND_SPEED = int(config['drone']['gnd_speed'])

        #connect to vehicle
        try:
            self.vehicle = connect(PIXHAWK, baud= BAUD_RATE, wait_ready = True)
            logging.info('Connected to Flight Controller Hardware on:  %s ', PIXHAWK)
        except:
            logging.error('Connection with Flight Controller on: %s is not made', PIXHAWK)
        
        self.TAKEOFF_ALT = TAKEOFF_ALT
        self.GND_SPEED = GND_SPEED
        self.STATE = "DISARMED"
        self.IS_ACTIVE = True
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0
        logging.info('Drone Connected')
        
    def executeCommand(self, command):

        if command == 'TAKEOFF':
            print(command)
            self.takeoff()

        if command == 'LAND':
            print(command)
            self.land()
        
        if command == 'RIGHT_45':
            print(command)
            self.rotate(1, 45)

        if command == 'LEFT_45':
            print(command)
            self.rotate(-1,45)

        if command == 'FREEZE':
            self.freeze()

        if command == 'GO_HOME':
            self.Go_home()

        if command == 'FORWARD':
            self.Go_forward()

        if command == 'BACKWARD':
            self.Go_backward()

        if command == 'RIGHT':
            self.Go_right()

        if command == 'LEFT':
            self.Go_left()

        
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
        self.stopMovement()

    def close(self):
        self.vehicle.close() 

    def takeoff(self):

        logging.info("Command TAKEOFF has started...")

        logging.info("Arming") 
        
        self.vehicle.mode = VehicleMode("GUIDED")   

        self.vehicle.armed = True
        time.sleep(1)
    
        while not self.vehicle.armed:
            logging.debug('self.vehicle.armed: '+str(self.vehicle.armed))
            self.vehicle.armed = True
            time.sleep(1)
        
        self.vehicle.simple_takeoff(self.TAKEOFF_ALT)
        logging.info("Takeoff")

        while True:
            current_hight = self.vehicle.location.global_relative_frame.alt
            """
            if current_hight >= self.TAKEOFF_ALT * 0.95:
                logging.info("Altitude reached")
                #commanding movement to the same location to unlock Yaw
                self.vehicle.simple_goto( self.vehicle.location.global_relative_frame)
                break
            time.sleep(1)"""
    
    def rotate(self, direction, rotation_angle):

        msg = self.vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        rotation_angle,  # param 1, yaw in degrees
        1,          # param 2, yaw speed deg/s
        direction,          # param 3, direction -1 ccw, 1 cw
        True, # param 4, 1 - relative to current position offset, 0 - absolute, angle 0 means North
        0, 0, 0)    # param 5 ~ 7 not used
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()

    def Go_forward(self):
        self.set_velocity_body(self.GND_SPEED, 0, 0)

    def Go_backward(self):
        self.set_velocity_body(-self.GND_SPEED, 0, 0)

    def Go_right(self):
        self.set_velocity_body(0, self.GND_SPEED, 0)

    def Go_left(self):
        self.set_velocity_body(0, -self.GND_SPEED, 0)
    
    def Go_home(self):
        logging.info('Going Home')

        self.vehicle.mode = VehicleMode("RTL")
        
        time.sleep(1)

    def set_velocity_body(self, vx, vy, vz):

        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0,
            0, 0,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000111111000111, #-- BITMASK -> Consider only the velocities
            0, 0, 0,        #-- POSITION
            vx, vy, vz,     #-- VELOCITY
            0, 0, 0,        #-- ACCELERATIONS
            0, 0)
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()

    def executeChangesNow(self):
       msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
       0,       # time_boot_ms (not used)
       0, 0,    # target system, target component
       mavutil.mavlink.MAV_FRAME_BODY_NED, # frame
       0b0000111111000111, # type_mask (only positions enabled)
       0, 0, 0,
       self.speed_x, self.speed_y, self.speed_z, # x, y, z velocity in m/s
       0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
       0, 0)
        
       self.vehicle.send_mavlink(msg)
       self.vehicle.flush()
    
    def stopMovement(self):
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0
        self.executeChangesNow()

    def land(self):

        logging.info("Command LAND has started...")

        logging.info("Landing")
        self.vehicle.channels.overrides = {}
        self.vehicle.mode = VehicleMode("LAND")