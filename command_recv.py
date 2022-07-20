import logging, threading

class Command_recv(threading.Thread):
    def __init__(self, socket, drone):
        threading.Thread.__init__(self)
        self.daemon=True
        self.socket= socket
        self.drone = drone
        self.IS_ACTIVE= True

    def run(self):
        while(self.IS_ACTIVE):
            try:
                data = (self.socket.recv(1024)).decode() #encoded data command
                self.drone.executeCommand(data)

            except Exception as e:
                logging.error('DataReceiver: '+str(e), exc_info=True)

    def stop(self):
       self.isActive = False

    

