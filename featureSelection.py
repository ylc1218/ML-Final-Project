import csv
import numpy
import sys
from sklearn import ensemble
from sklearn import svm
from sklearn import feature_selection as fs
from sklearn import preprocessing as pp

# chekc track is specified
if(len(sys.argv) < 2):
	print("please specify track, track = {track1, track2}")
	exit(1)
track = sys.argv[1]


# load sample feature (training)
with open('mix_train.csv', 'r') as train_x_csv:
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
with open('mix_test.csv', 'r') as test_x_csv:
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

scoring = 'accuracy' if track == 'track2' else 'average_precision'

lsvc = svm.LinearSVC()
selector = fs.RFECV(lsvc, step=1, cv=5, scoring=scoring)
selector.fit(trainingX, trainingY)

print(selector.get_support())
