import cv2
import pyrebase
from ultralytics import YOLO
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import supervision as sv
import time

config={
"apiKey": "AIzaSyCDAGglBwh-7NEU4lAFTS7f5tbGacUXdMA",
  "authDomain": "kvh-proj.firebaseapp.com",
  "projectId": "kvh-proj",
  "storageBucket": "kvh-proj.appspot.com",
  "messagingSenderId": "348476571342",
  "appId": "1:348476571342:web:9aa8f6c522c33a2f171a9f",
  "measurementId": "G-FW36366BN7",
  "databaseURL": "https://kvh-proj-default-rtdb.firebaseio.com"
}
db=pyrebase.initialize_app(config)
rl_db=db.database()
im_db=db.storage()

inc_id=str(rl_db.generate_key())

#im_db.child("images/"+inc_id+".jpg").put('download.jpeg')
model = YOLO("best.pt")
model_crime_classification=load_model('kavach.h5')
labels = ['Abuse', 'Arrest', 'Arson', 'Assault', 'Burglary', 'Explosion', 'Fighting', 'NormalVideos', 'RoadAccidents', 'Robbery', 'Shooting', 'Shoplifting', 'Stealing', 'Vandalism']

img = cv2.imread('drowsyman.jpg')
# img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
# img = cv2.resize(img,(640,640))
# img = img.reshape(1,640,640,3)

#print(result)

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture('http:/192.168.137.160:9060/stream/video.mjpeg')
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpeg', image)
        de = cv2.imdecode(jpeg,cv2.IMREAD_COLOR)
        cv2.imwrite('test.jpg',de)
        img = cv2.cvtColor(jpeg, cv2.COLOR_RGB2BGR)
        img = cv2.resize(img,(64,64))
        img = img.reshape(1,64,64,3)
        result = model('test.jpg')[0]
        detections = sv.Detections.from_yolov8(result)
        label = [f"{model.model.names[class_id]} {confidence:0.1f}" for _, confidence, class_id, _ in detections]
        crime = model_crime_classification.predict(img)
        # if labels[np.argmax(crime)]!='NormalVideos':    
        #     print(labels[np.argmax(crime)])
        print(labels[np.argmax(crime)])
        print(label)
        inc_time = time.gmtime(0)
        rl_db.child("incidents").child(inc_id).set({'incident_type':'abuse','incident_time':inc_time,'img_url':"oioi",'cam_id':"x1"})
        im_db.child("images/"+inc_id+".jpg").put('test.jpg')
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        
        #print(result)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')