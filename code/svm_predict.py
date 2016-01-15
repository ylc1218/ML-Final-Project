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
if(len(sys.argv) < 3):
	print("please specify #n_esti #depth mode")
	exit(1)
C = int(sys.argv[2])
gamma = int(sys.argv[3])

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

svc = svm.SVC(C=C, gamma=gamma, cache_size=8192, max_iter=1000000)
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

