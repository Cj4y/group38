import random
import csv
import math
import operator

split = 0.66

with open('rock_datasets.csv') as csvfile:
    lines = csv.reader(csvfile)
    dataset = list(lines)[1:] # remove 1st row of a csv file

random.shuffle(dataset)

div = int(split * len(dataset))
train_set = dataset [:div]
test_set = dataset [div:]


'''
1. name: euclideanDistance
2. input: one of test_set, one of training_set, length of test_set
3. output: square root of the sum of the squared differences between the two lists of numbers
'''
def euclideanDistance(test_value, train_value, length):
	distance = 0
	for x in range(length):
		distance += pow((float(test_value[x]) - float(train_value[x])), 2)
	return math.sqrt(distance)

'''
1. name: getNeighbors
2. input: train_set, one of test_set, k value
3. output: the 'k' nearest neighbors
'''
def getNeighbors(train_set, test_value, k):
	distances = []
	length = len(test_value)-1 # did -1 because every last value of arrays is the name of rock type
	for x in range(len(train_set)): # for every lists of train_set, calculate euclidean distance between one of train set and test_value, then append it to distances
		d = euclideanDistance(test_value, train_set[x], length)
		distances.append((train_set[x], d))
	distances.sort(key=operator.itemgetter(1)) # sort all distances
	neighbors = []
	for x in range(k): # append the top k nearest neighbors to neighbors
		neighbors.append(distances[x][0])
	return neighbors

'''
1. name: getHighest
2. input: neighbors
3. output: Of 'k' number of neighbors, select the neighbor with the highest frequency
'''  
k_candidates = {}
def getHighest(neighbors):
	for x in range(len(neighbors)):
		candidate = neighbors[x][-1] 
		if candidate in k_candidates:
			k_candidates[candidate] += 1
		else:
			k_candidates[candidate] = 1
	sortedCandidates = sorted(k_candidates.items(), key=operator.itemgetter(1), reverse=True)
	return sortedCandidates[0][0]

'''
1. name: getAccuracy
2. input: test_set, predicted value
3. output: the accuracy of all predictions compared to real values
'''
def getAccuracy(test_set, predictions):
	correct = 0
	for x in range(len(test_set)):
		if test_set[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(test_set))) * 100.0

predictions=[]

k = 3

print("-"*83)
print("|"+" "*15 + "Prediction" + " "*15 +"|" + " "*15 + "Actuality" + " "*16+"|")
print("-"*83)

for x in range(len(test_set)):
    neighbors = getNeighbors(train_set, test_set[x], k)
    result = getHighest(neighbors)
    predictions.append(result)
    print("|"+" "*((39-len(result))//2) + repr(result) + " "*((39-len(result))//2) +"|" + " "*((39-len(test_set[x][-1]))//2)   + repr(test_set[x][-1])+ " "*((39-len(test_set[x][-1]))//2)+"|")

accuracy = getAccuracy(test_set, predictions)

print("-"*83)
print("|"+" "*((82-len("Accuracy: " + repr(accuracy) + "%"))//2) + "Accuracy: " + repr(accuracy) + "%" + " "*((82-len("Accuracy: " + repr(accuracy) + "%"))//2)+"|")
print("-"*83)