import cv2
import numpy
import face_recognition
import os
from datetime import datetime
import csv
#####################
import os,urllib.request
from django.conf import settings
face_detection_videocam = cv2.CascadeClassifier(os.path.join(settings.BASE_DIR, 'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))
##############
go=True

class VideoCamera(object):
	def __init__(self):
		self.video =  cv2.VideoCapture(0)



	def __del__(self):
		self.video.release()


	def get_frame(self):
		path = 'ImagesAttendance'
		myList = os.listdir(path)
		images = []
		classNames = []
		for cls in myList:
			curImg = cv2.imread(f'{path}/{cls}')
			images.append(curImg)
			classNames.append(os.path.splitext(cls)[0])
		encodeList = []
		for img in images:
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			encode = face_recognition.face_encodings(img)[0]
			encodeList.append(encode)
		encodeListKnown =  encodeList

		success, videoImg = self.video.read()
		videoImg = cv2.cvtColor(videoImg, cv2.COLOR_BGR2RGB)

		#Time
		now = datetime.now()
		dtString = now.strftime('%d/%m/%Y %H:%M:%S')
		cv2.putText(videoImg, dtString, (5,30), cv2.FONT_HERSHEY_COMPLEX,1,(62, 214, 129),2)
    
		facesCurFrame = face_recognition.face_locations(videoImg)
		encodesCurFrame = face_recognition.face_encodings(videoImg, facesCurFrame)

		for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
			matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
			faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

			matchIndex = numpy.argmin(faceDis)

			if matches[matchIndex]:
				name = classNames[matchIndex].upper()
				y1,x2,y2,x1 = faceLoc
				cv2.rectangle(videoImg, (x1,y1), (x2,y2), (0,0,255),2)
				cv2.rectangle(videoImg, (x1, y2-35), (x2, y2), (0, 0, 255), 2, cv2.FILLED)
				cv2.putText(videoImg, name, (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),1)
				with open('Attendance.csv', 'a+') as f:
					myDataList = f.readlines()
					nameList = []
					for line in myDataList:
						entry = line.split(',')
						nameList.append(entry[0])

					if name not in nameList:
						now = datetime.now()
						dtString = now.strftime('%H:%M:%S')
						dtDate = now.strftime('%d-%m-%Y')
						go=True
						if go==True:
							bul_entry = 'Yes'
							bul_exit = 'No'
							go=False
						else:
							bul_entry = 'No'
							bul_exit = 'Yes'
							go=True
						f.writelines(f'\n{name},{dtDate},{dtString},{bul_entry},{bul_exit}')
			else:
				name = "Unknown"
				y1,x2,y2,x1 = faceLoc
				cv2.rectangle(videoImg, (x1,y1), (x2,y2), (0,0,255),2)
				cv2.rectangle(videoImg, (x1, y2-35), (x2, y2), (0, 0, 255), 2, cv2.FILLED)
				cv2.putText(videoImg, name, (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),1)
				with open('Attendance.csv', 'a+') as f:
					myDataList = f.readlines()
					nameList = []
					for line in myDataList:
						entry = line.split(',')
						nameList.append(entry[0])

					if name not in nameList:
						now = datetime.now()
						dtString = now.strftime('%H:%M:%S')
						dtDate = now.strftime('%d-%m-%Y')
						go=True
						if go==True:
							bul_entry = 'Yes'
							bul_exit = 'No'
							go=False
						else:
							bul_entry = 'No'
							bul_exit = 'Yes'
							go=True
						f.writelines(f'\n{name},{dtDate},{dtString},{bul_entry},{bul_exit}')
		ret, jpeg = cv2.imencode('.jpg', videoImg)
		return jpeg.tobytes()
