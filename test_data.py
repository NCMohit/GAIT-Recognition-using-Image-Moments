import cv2

dataset = "C:\\Users\\ncmoh\\OneDrive\\Desktop\\GAIT\\CASIAB"

def Moment_pq(p,q,img):
	moment = 0
	for row in range(img.shape[0]):
		for col in range(img.shape[1]):
			moment += int(((row+1)**p)*((col+1)**q)*img[row,col])
	return moment

moment_range = 2

for person in range(5,16):
	current_dir = dataset +"\\"+ str(person).zfill(3)
	for pos in ['bg-01','bg-02','nm-04','nm-05']:
		current_dir2 = current_dir + "\\" + pos
		for angle in ["000","018","036"]:
			current_dir3 = current_dir2 + "\\" + angle
			for img in range(1,2):
				current_dir4 = current_dir3 + "\\" + str(person).zfill(3) + "-" + pos + "-" + angle + "-" + str(img).zfill(3) +".png"
								
				current_img = cv2.imread(current_dir4,cv2.IMREAD_GRAYSCALE)
				row = str(person)
				for p in range(0,moment_range+1):
					for q in range(0,moment_range+1):
						# print("M "+str(p)+","+str(q)+" value is: "+str(Moment_pq(p,q,current_img)))
						row += "," + str(Moment_pq(p,q,current_img))
 
				model = open("test_data.csv","a")
				model.write(row+"\n")
				print(row)
				model.close()