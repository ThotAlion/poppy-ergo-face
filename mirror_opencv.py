import requests,json,time,cv2
from numpy import *

def enableMotors(robotIP):
    """
    This function enables the motors of the robot.
    """
    for m in ["m1","m2","m3","m4","m5","m6"]:
        url = "http://"+robotIP+"/motors/"+m+"/registers/compliant/value.json"
        data = "false"
        h = {'Content-type': 'application/json'}
        response = requests.post(url, data=data, headers=h)

def disableMotors(robotIP):
    """
    This function enables the motors of the robot.
    """
    for m in ["m1","m2","m3","m4","m5","m6"]:
        url = "http://"+robotIP+"/motors/"+m+"/registers/compliant/value.json"
        data = "true"
        h = {'Content-type': 'application/json'}
        response = requests.post(url, data=data, headers=h)

def getRobot(robotIP):
    """
    This function gets the robot information.
    """
    url = "http://"+robotIP+"/robot.json"
    response = requests.get(url)
    return response.json()

def motorGoto(robotIP,listPositions,duration):
    """
    This function sets the motor position of the robot.
    """
    url = "http://"+robotIP+"/motors/goto.json"

    data = json.dumps({
        "motors": ["m1","m2","m3","m4","m5","m6"],
        "positions": listPositions,
        "duration": duration,
        "wait": "false",
    })
    h = {'Content-type': 'application/json'}
    response = requests.post(url, data=str(data), headers=h)
    return response.json()

if __name__ == "__main__":
    robotIP = "10.0.0.14:8080"
    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

    enableMotors(robotIP)
    motorGoto(robotIP,[0.0,-20.0,0.0,0.0,0.0,0.0],1.0)
    time.sleep(1)
    f = 1.0
    Amp = 70.0
    xc=0.0
    yc=0.0
    cc=0.0
    for i in range(100):
        t=time.time()
        resp =requests.get('http://'+robotIP+'/sensors/camera/frame.png')
        imgFile = open('image.png','wb')
        imgFile.write(resp.content)
        imgFile.close()
        img = cv2.imread('image.png')
        (x,y,w,h) = getFace(face_cascade,img)
        tilt=0
        if x >= 0:
            xc = xc+0.04*(x-320)
            cc = cc-0.05*xc
            yc = yc+0.02*(y-240)
            tilt = 20.0
        motorGoto(robotIP,[cc,-20.0,yc,tilt,xc,xc],0.5)
        print(time.time()-t,i,Amp*sin(2*pi*f*t))
    disableMotors(robotIP)
