import csv
import numpy
from sklearn import ensemble

# load sample feature (training)
with open('sample_train_x.csv', 'r') as train_x_csv:
	reader = csv.reader(train_x_csv, delimiter=',')
	next(reader)
	x=list(reader)
	trainingX=numpy.array(x).astype('double')

# trainingX = [[1, 2], [3, 4]]

# load labels (training)
with open('truth_train.csv', 'r') as train_y_csv:
	reader = csv.reader(train_y_csv, delimiter=',')
	x=list(reader)
	trainingY=numpy.array(x).astype('double')
# trainingY = [1, -1]
	trainingY=trainingY[:, 1]
print(trainingY)

# load sample feature (testing)
with open('sample_test_x.csv', 'r') as test_x_csv:
	reader = csv.reader(test_x_csv, delimiter=',')
	next(reader)
	x=list(reader)
	testingX=numpy.array(x).astype('double')
#print(testingX)
#testingX = [[3, 4], [3, 4], [1, 2], [1, 2]]

# AdaBoost
rfc = ensemble.AdaBoostClassifier(n_estimators=1000)
rfc.fit(trainingX, trainingY)
predictLabel = rfc.predict(testingX)

print(predictLabel)

# output result to file
with open('Ada_1000x1.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for label in predictLabel:
		writer.writerow([label])

