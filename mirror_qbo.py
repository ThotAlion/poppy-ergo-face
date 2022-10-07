#!/usr/bin/python3
import dlib,json,time
import numpy as np
import cv2

if __name__ == "__main__":


    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor('shape_predictor_5_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
    xc=0.0
    yc=0.0
    cc=0.0
    tilt=0.0
    w=20.0
    cap = cv2.VideoCapture(0)



    while 1:
        try:
            t0 = time.time()
            # resp =requests.get('http://'+robotIP+'/sensors/camera/frame.png')
            # imgFile = open('image.png','wb')
            # imgFile.write(resp.content)
            # imgFile.close()

            if cap.isOpened():
                # img = dlib.load_rgb_image('image.jpg')
                flag, img = cap.read()
                dets = detector(img, 1)
                if len(dets) > 0:
                    print(dets[0].center())
                    img_shape = sp(img, dets[0])
                    theta=img_shape.parts()[0].y-img_shape.parts()[2].y
                    x = dets[0].center().x
                    y = dets[0].center().y
                    w = 1.0*np.abs(img_shape.parts()[0].x-img_shape.parts()[2].x)
                    # print(w)
                    xc = xc+0.05*(x-320)
                    cc = cc-0.07*xc
                    yc = yc+0.02*(y-240)
                    tilt = tilt+0.3*theta
                    # print(cc,yc)
                # motorGoto(robotIP,[cc,w-20,-w+20+yc,tilt,xc,xc],0.1)
                    # 
                    # print(img_shape)
                    # img_aligned = dlib.get_face_chip(img, img_shape)
                print(time.time()-t0)
        except Exception as e:
            print(e)
            break
    