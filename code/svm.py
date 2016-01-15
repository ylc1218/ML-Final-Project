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
with open('data/mix36_train.csv', 'r') as train_x_csv:
	reader = csv.reader(train_x_csv, delimiter=',')
	next(reader)
	x=list(reader)
	trainingX=numpy.array(x).astype('double')

# assign sample weight = 1/take_course_num
if track == 'track2':
	sampleWeight = 1/trainingX[:, 3]
else:
	sampleWeight = numpy.array([1]*trainingX.shape[0])

# remove the 4th column (take_course_num)
trainingX = numpy.delete(trainingX, 3, 1)
print('load trainingX with shape = ' + str(trainingX.shape))

# load labels (training)
with open('data/truth_train.csv', 'r') as train_y_csv:
	reader = csv.reader(train_y_csv, delimiter=',')
	x=list(reader)
	trainingY=numpy.array(x).astype('double')

trainingY=trainingY[:, 1]
# print(trainingY)


# load sample feature (testing)
with open('data/mix36_test.csv', 'r') as test_x_csv:
	reader = csv.reader(test_x_csv, delimiter=',')
	next(reader)
	x=list(reader)
	testingX=numpy.array(x).astype('double')

# remove the 4th column (take_course_num)
testingX = numpy.delete(testingX, 3, 1)
print('load testingX with shape = ' + str(testingX.shape))

# scale data to zero mean, 1 std var
scaler = pp.StandardScaler()
trainingX = scaler.fit_transform(trainingX)
testingX = scaler.fit_transform(testingX)
print('scaled')

params = []
for C in [0.5, 0.7]:
	for gamma in [20, 30, 40, 50, 60, 70]:
		params.append([C, gamma])


bestParam = []
bestScore = 0
scoring = 'accuracy' if track == 'track2' else 'average_precision'

# Cross-validation
for param in params:
	print(param)
	# Support Vector Machine
	svc = svm.SVC(C=param[0], gamma=param[1], cache_size=2048, max_iter=1000000)
	cvScores = CV.cross_val_score(svc, trainingX, trainingY, scoring=scoring, cv=5, n_jobs=5)
	if cvScores.mean() > bestScore:
		bestScore = cvScores.mean()
		bestParam = param
	print(cvScores.mean())

# bestParam = params[0]
print(bestScore)
print(bestParam)
svc = svm.SVC(C=bestParam[0], gamma=bestParam[1], cache_size=2048, max_iter=1000000)
svc.fit(trainingX, trainingY)
predictLabel = svc.predict(testingX) if track == 'track2' else svc.predict_proba(testingX)

print(predictLabel)

# output result to file
with open('SVM_CV_mix36_'+track+'.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for label in predictLabel:
		if track == 'track2':
			writer.writerow([label])
		else:
			writer.writerow([label[1]])

