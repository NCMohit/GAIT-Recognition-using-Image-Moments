import cv2

dataset = "C:\\Users\\ncmoh\\OneDrive\\Desktop\\GAIT\\CASIAB"

# model = open("moments_data.csv","a")
# model.write("Person,M00,M01,M02,M10,M11,M12,M20,M21,M22"+"\n")
# model.close()

def Moment_pq(p,q,img):
	moment = 0
	for row in range(img.shape[0]):
		for col in range(img.shape[1]):
			moment += int(((row+1)**p)*((col+1)**q)*img[row,col])
	return moment


for person in range(1,16):
	current_dir = dataset +"\\"+ str(person).zfill(3)
	for pos in ['bg-01','bg-02']:
		current_dir2 = current_dir + "\\" + pos
		for angle in ["000","018","036"]:
			current_dir3 = current_dir2 + "\\" + angle
			for img in range(1,11):
				current_dir4 = current_dir3 + "\\" + str(person).zfill(3) + "-" + pos + "-" + angle + "-" + str(img).zfill(3) +".png"
				
				try:				
					current_img = cv2.imread(current_dir4,cv2.IMREAD_GRAYSCALE)
					row = str(person)
					for p in range(0,3):
						for q in range(0,3):
							# print("M "+str(p)+","+str(q)+" value is: "+str(Moment_pq(p,q,current_img)))
							row += "," + str(Moment_pq(p,q,current_img))
				except:
					continue 
				model = open("moments_data.csv","a")
				model.write(row+"\n")
				print(row)
				model.close()
