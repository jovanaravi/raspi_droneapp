# This is watching connection, when is called from master app, execution starts from run() method

import threading, logging, time
from urllib.request import urlopen 

class Watchdog(threading.Thread):

    def __init__(self, drone, host_ip, max_reconnection_attempts):
        threading.Thread.__init__(self)
        self.daemon = True
        self.drone = drone
        self.host_ip = host_ip
        self.max_reconnection_attempts = max_reconnection_attempts
        self.connection_attempts = 0
        self.net_status = False

    def run(self):
        time.sleep(5)
      
        while(True):
            try:
                if self.is_internet_on():
                    self.connection_attempts = 0
                    time.sleep(1)
                else:
                    self.drone.freeze()
                    self.connection_attempts = self.connection_attempts + 1
                    logging.info("Connection attempt %s, max_reconnection_attempts %s", str(self.connection_attempts), str(self.max_reconnection_attempts))
                    time.sleep(1)
                    if self.connection_attempts == self.max_reconnection_attempts:
                        self.drone.return_to_launch()
                        break
            except Exception as e:
                logging.error(str(e), exc_info=True)
                time.sleep(2)
        
    def is_internet_on(self):
        try:
            urlopen(str('http://' + self.host_ip + ':5000'), timeout=5)
            self.net_status = True
            return True
        except: 
            logging.error('Watchdog - Network is unreachable: ', exc_info=True)
            self.net_status = False
            return False