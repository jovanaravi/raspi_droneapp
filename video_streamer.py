import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time, socket, configparser, argparse, sys, logging
from utils import Utils

parser = argparse.ArgumentParser()
parser.add_argument('--d', nargs=1, default=None)
args= parser.parse_args()

APP_DIR = args.d[0] if args.d != None else './'
CONFIGURATIONS = APP_DIR + 'configuration.ini'

config = configparser.ConfigParser()



DRONE_ID = 1
HOST_IP = '192.168.8.107'
VIDEO_PORT = 1313

GRAYSCALE = 'false'.lower() == 'true'
FRAMES_PER_SECOND = 13
JPEG_QUALITY = 80
WIDTH = 512
HEIGHT = 352




camera = None
video_socket = None

while(True):
    try:
        camera = PiCamera()
        camera.resolution = (WIDTH, HEIGHT)
        camera.framerate = FRAMES_PER_SECOND

        rawCapture = PiRGBArray(camera, size=(WIDTH, HEIGHT))
        time.sleep(0.1)

        
        video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        video_socket.connect((HOST_IP, VIDEO_PORT))


        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image_data = frame.array
            
            image_data = cv2.rotate(image_data, cv2.ROTATE_180)
            
            if GRAYSCALE:
                image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
            
            code, jpg_buffer = cv2.imencode(".jpg", image_data, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])

            datagramMsgBytes = Utils.create_datagram_message(jpg_buffer)

            video_socket.sendall(datagramMsgBytes)
            
            rawCapture.truncate(0)


    except Exception as e:
        
        
        if camera != None:
            camera.close()
        if video_socket != None:
            video_socket.close()
        
        time.sleep(2)