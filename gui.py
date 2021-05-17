import tkinter as tk
import os
import math
from tkinter import filedialog
import cv2

def euc_dist(x,y):
	if(len(x)!=len(y)):
		print("Not possible !")
		return None
	else:
		tot_sum = 0
		for i in range(len(x)):
			tot_sum += (abs(int(x[i]) - int(y[i])))**2
		return math.sqrt(tot_sum)

def Moment_pq(p,q,img):
	moment = 0
	for row in range(img.shape[0]):
		for col in range(img.shape[1]):
			moment += int(((row+1)**p)*((col+1)**q)*img[row,col])
	return moment

def train():
	filename = filedialog.askopenfile(initialdir="/")
	print(filename.name)
	dirname = filename.name.split("/")[-1]
	dirname_name = dirname.split(".")[0]
	print(dirname_name)
	vidcap = cv2.VideoCapture(filename.name)
	success,image = vidcap.read()
	count = 0
	success = True
	os.mkdir(dirname_name)
	while success:
		success,image = vidcap.read()
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)	
		blur = cv2.GaussianBlur(image,(5,5),0)
		ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		th3 = cv2.bitwise_not(th3)

		try:				
			row = str(dirname_name)
			for p in range(0,3):
				for q in range(0,3):
					row += "," + str(Moment_pq(p,q,th3))
		except:
			continue 
		model = open("moments_data.csv","a")
		model.write(row+"\n")
		print(row)
		model.close()

		cv2.imwrite(dirname_name+"/frame%d.jpg" % count, th3)     # save frame as JPEG file
		if cv2.waitKey(10) == 27:                     # exit if Escape is hit
			break
		count += 1

def predict():
	filename = filedialog.askopenfile(initialdir="/")
	print(filename.name)
	dirname = filename.name.split("/")[-1]
	dirname_name = dirname.split(".")[0]
	print(dirname_name)
	vidcap = cv2.VideoCapture(filename.name)
	success,image = vidcap.read()
	count = 0
	success = True

	moments = []
	model = open("moments_data.csv","r")
	for row in model.readlines():
		row = row.replace("\n","")
		moments.append(row.split(","))
	model.close()

	correct_preds = 0
	total_preds = 0

	iterations_timeline = []
	accuracy_timeline = []

	while success:
		success,image = vidcap.read()
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)	
		blur = cv2.GaussianBlur(image,(5,5),0)
		ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		th3 = cv2.bitwise_not(th3)
		
		try:				
			sample = [dirname_name]
			for p in range(0,3):
				for q in range(0,3):
					sample.append(str(Moment_pq(p,q,th3)))
		except:
			continue 

		neighbours = {}
		for data in moments[1:]:
			neighbours[str(data)] = euc_dist(data[1:],sample[1:])
		sorted_neighbours = {k: v for k, v in sorted(neighbours.items(), key=lambda item: item[1])}
		print(list(sorted_neighbours.keys())[0],list(sorted_neighbours.values())[0])
		print("Actual person: ",sample[0])
		temp = list(sorted_neighbours.keys())[0]
		temp = temp.replace("[","")
		temp = temp.replace("]","")
		temp = temp.replace(" ","")
		temp = temp.replace("'","")
		temp = temp.split(",")
		print("Estimated person: ",temp[0])
		total_preds += 1
		if(str(sample[0])==temp[0]):
			correct_preds+=1
		iterations_timeline.append(total_preds)
		accuracy_timeline.append(correct_preds/total_preds)

		# cv2.imwrite(dirname_name+"/frame%d.jpg" % count, th3)     # save frame as JPEG file
		# if cv2.waitKey(10) == 27:                     # exit if Escape is hit
		# 	break
		count += 1
	print("\nAccuracy: ",correct_preds/total_preds)

############## Main ############

top = tk.Tk()
top.geometry("300x100")

top.title("Prediction GUI Video Input")

train = tk.Button(top, text='Train Video', width=25, command=train)

predict_vid = tk.Button(top, text='Predict Video', width=25, command=predict)

train.pack()
predict_vid.pack()
top.mainloop()