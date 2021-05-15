import math
import matplotlib.pyplot as plt

moments = []

model = open("moments_data.csv","r")

for row in model.readlines():
	row = row.replace("\n","")
	moments.append(row.split(","))

model.close()

# print(moments)

def euc_dist(x,y):
	if(len(x)!=len(y)):
		print("Not possible !")
		return None
	else:
		tot_sum = 0
		for i in range(len(x)):
			tot_sum += (abs(int(x[i]) - int(y[i])))**2
		return math.sqrt(tot_sum)

test_data = []

test = open("test_data.csv","r")

for row in test.readlines():
	row = row.replace("\n","")
	test_data.append(row.split(","))

test.close()

# test_data = [
# 	[2,256530,39995985,6242934735,22542765,3517372590,549430773420,2062754925,322091455740,-20005307682],
# 	[4,265455,41514510,6500141760,23420475,3663103050,573590077260,2136681465,334224855540,-4968912862],
# 	[14,272085,60064995,13267813965,22815870,5034852345,1111697825835,1994524830,439984206045,23585276235]
# ]

correct_preds = 0
total_preds = 0

iterations_timeline = []
accuracy_timeline = []

for sample in test_data:
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
print("\nAccuracy: ",correct_preds/total_preds)

plt.plot(iterations_timeline, accuracy_timeline)
plt.xlabel("Iterations")
plt.ylabel("Accuracy")
plt.title("Accuracy over increasing time")
plt.show()