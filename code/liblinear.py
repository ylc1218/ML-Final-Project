import csv
import numpy
import sys
from sklearn import svm
from sklearn import cross_validation as CV
from sklearn import preprocessing as pp

# chekc track is specified
if(len(sys.argv) < 2):
	print("please specify track, track = {track1, track2}")
	exit(1)
track = sys.argv[1]

# load sample feature (training)
with open('time_train.csv', 'r') as train_x_csv:
	reader = csv.reader(train_x_csv, delimiter=',')
	next(reader)
	x=list(reader)
	trainingX=numpy.array(x).astype('double')

# remove the first column (ID)
trainingX=trainingX[:, 1:]
print('load trainingX with shape = ' + str(trainingX.shape))
# trainingX = [[1, 2], [3, 4]]

# load labels (training)
with open('truth_train.csv', 'r') as train_y_csv:
	reader = csv.reader(train_y_csv, delimiter=',')
	x=list(reader)
	trainingY=numpy.array(x).astype('double')
# trainingY = [1, -1]
	trainingY=trainingY[:, 1]
# print(trainingY)


# load sample feature (testing)
with open('time_test.csv', 'r') as test_x_csv:
	reader = csv.reader(test_x_csv, delimiter=',')
	next(reader)
	x=list(reader)
	testingX=numpy.array(x).astype('double')

testingX=testingX[:, 1:]
print('load testingX with shape = ' + str(testingX.shape))
# print(testingX)
# testingX = [[3, 4], [3, 4], [1, 2], [1, 2]]


# scale data to zero mean, 1 std var
scaler = pp.StandardScaler()
trainingX = scaler.fit_transform(trainingX)
testingX = scaler.fit_transform(testingX)
print('scaled')

params = []
for C in [0.1, 1, 10]:
	params.append([C])


bestParam = []
bestScore = 0
scoring = 'accuracy' if track == 'track2' else 'average_precision'

# Cross-validation
for param in params:
	print(param)
	# random forest
	lsvc = svm.LinearSVC(C=param[0], tol=1e-6)
	cvScores = CV.cross_val_score(lsvc, trainingX, trainingY, scoring=scoring, cv=5)
	if cvScores.mean() > bestScore:
		bestScore = cvScores.mean()
		bestParam = param
	print(cvScores.mean())

# bestParam = params[0]
print(bestScore)
print(bestParam)
lsvc = svm.LinearSVC(C=bestParam[0], tol=1e-6)
lsvc.fit(trainingX, trainingY)
predictLabel = lsvc.predict(testingX) if track == 'track2' else lsvc.predict_proba(testingX)

print(predictLabel)

# output result to file
with open('Linear_CV_timeFeature_'+track+'.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for label in predictLabel:
		if track == 'track2':
			writer.writerow([label])
		else:
			writer.writerow([label[1]])




