import logging, time, argparse, configparser, sys
import socket, os, signal, psutil 
from subprocess import Popen

from watchdog import Watchdog
from drone import Drone
from command_recv import Command_recv


parser = argparse.ArgumentParser()
parser.add_argument('--d', nargs=1, default=None)
args = parser.parse_args()

#application directory
APP_DIR = args.d[0] if args.d != None else "./"
CONFIGURATIONS = APP_DIR + 'configuration.ini'

#logging init
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(APP_DIR + 'logs/main app | ' + str(time.asctime()) + '.log'),
        logging.StreamHandler()
    ]
)

#read a file
config = configparser.ConfigParser()
#protection 
if len(config.read(CONFIGURATIONS)) == 0:
    logging.error("Could Not Read Configurations File: " + CONFIGURATIONS)
    sys.exit() 

#variables from configuration file  
DRONE_ID = config['drone']['id']
HOST_IP = config['cloud-app']['ip']
MAX_RECONNECTION_ATTEMPTS = int( config['cloud-app']['max-reconnection-attempts'])
NODE_PORT = int(config['cloud-app']['node-port'])


if __name__ == '__main__':
    while(True):
        try:
            drone = Drone(config)
            break
        except Exception as e:
            logging.error(str(e), exc_info=True)
            time.sleep(2)
    
    watchdog = Watchdog(drone, HOST_IP, MAX_RECONNECTION_ATTEMPTS)
    watchdog.start()

    video_streamer = None
    node_socket = None 
    command_receiver = None 

    

    while drone.IS_ACTIVE:
        try:
            while not watchdog.net_status:
               time.sleep(1)
            
            time.sleep(3)

            video_streamer = Popen('/usr/bin/python3 ' + APP_DIR + 'video_streamer.py', shell=True) #separate process for video streamer is created

            node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            node_socket.connect((HOST_IP, NODE_PORT))                    
            logging.info('Socket TCP Connection Opened') 
            
            command_receiver = Command_recv(node_socket, drone) #separate thread for receiving commands were created
            command_receiver.start()
            while watchdog.net_status and drone.IS_ACTIVE:
                lon= drone.Get_lon()
                lat= drone.Get_lat()
                msg= (str(lat)+ " " +str(lon)).encode()
                node_socket.send(msg)
                time.sleep(10) #promeni vreme na sekund, nemoj zaboraviti curko
        except Exception as e:
            logging.error(str(e), exc_info=True)
            drone.freeze() 

        finally:
            if video_streamer != None:
                current_process = psutil.Process(video_streamer.pid)
                children = current_process.children(recursive=True)
                
                for child in children:
                    if child.pid != os.getpid():
                        os.kill(child.pid, signal.SIGKILL)

                os.kill(video_streamer.pid, signal.SIGKILL)
            if node_socket != None:
                node_socket.close()
            if command_receiver != None:
                command_receiver.stop()    
    drone.close()
    
    logging.info('Drone Offline')      


