import cv2
import numpy
import face_recognition
import os
from datetime import datetime

path = 'ImagesAttendance'
myList = os.listdir(path)
print(myList)

images = []
classNames = []

for cls in myList:
    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance.csv', 'a+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

encodeListKnown = findEncodings(images)
print(len(encodeListKnown))

# step three

cap = cv2.VideoCapture(0)

while True:
    success, videoImg = cap.read()
    imgSml = cv2.resize(videoImg, (0,0), None, 0.25, 0.25)
    imgSml = cv2.cvtColor(imgSml, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgSml)
    encodesCurFrame = face_recognition.face_encodings(imgSml, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = numpy.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(videoImg, (x1,y1), (x2,y2), (0,0,255),2)
            cv2.rectangle(videoImg, (x1, y2-35), (x2, y2), (0, 0, 255), 2, cv2.FILLED)
            cv2.putText(videoImg, name, (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)

    cv2.imshow('webcam', videoImg)
    cv2.waitKey(1)