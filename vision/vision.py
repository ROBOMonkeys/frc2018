from cscore import CameraServer
import cv2
import numpy as np
from grip import BluePipeline, RedPipeline
import networktables.networktables as nt

def run():
    n = nt.NetworkTables.getTable("SmartDashboard")
    
    cs = CameraServer.getInstance()

    camera = cs.startAutomaticCapture()
    camera.setResolution(320, 240)

    cvSink = cs.getVideo()

    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

    pipeline = None
    team = n.getNumber("team", 2)
    if team == 1:
        pipeline = BluePipeline()
    elif team == 0:
        pipeline = RedPipeline()
       
    
    while pipeline is not None:
        time, img = cvSink.grabFrame(img)

        if time == 0:
            continue

        
    
    
