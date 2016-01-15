import csv
import numpy
import sys
from sklearn import ensemble
from sklearn import cross_validation as CV


if(len(sys.argv) < 4):
	print("usage: python "+ sys.argv[0] +" {track} {#n_esti} {#depth} {mode}")
	exit(1)
track = sys.argv[1]
n_esti = int(sys.argv[2])
depth = int(sys.argv[3])
mode = sys.argv[4]

# load sample feature (training)
with open('data/mix77_train.csv', 'r') as train_x_csv:
	reader = csv.reader(train_x_csv, delimiter=',')
	next(reader)
	x=list(reader)
	trainingX=numpy.array(x).astype('double')

# assign sample weight = 1/take_course_num
if track == 'track2':
	sampleWeight = 1/trainingX[:, 1]
else:
	sampleWeight = numpy.array([1]*trainingX.shape[0])

# remove the first two columns
# trainingX = numpy.delete(trainingX, 3, 1)
trainingX = trainingX[:, 2:]
print('load trainingX with shape = ' + str(trainingX.shape))
# trainingX = [[1, 2], [3, 4]]

# load labels (training)
with open('data/truth_train.csv', 'r') as train_y_csv:
	reader = csv.reader(train_y_csv, delimiter=',')
	x=list(reader)
	trainingY=numpy.array(x).astype('double')
# trainingY = [1, -1]
	trainingY=trainingY[:, 1]
# print(trainingY)

# load sample feature (testing)
with open('data/mix77_test.csv', 'r') as test_x_csv:
	reader = csv.reader(test_x_csv, delimiter=',')
	next(reader)
	x=list(reader)
	testingX=numpy.array(x).astype('double')

# remove the first two columns
# testingX = numpy.delete(testingX, 3, 1)
testingX = testingX[:, 2:]
print('load testingX with shape = ' + str(testingX.shape))
# print(testingX)
# testingX = [[3, 4], [3, 4], [1, 2], [1, 2]]

randomSeed = 1126
print('randomSeed = ' + str(randomSeed))

gbc = ensemble.GradientBoostingClassifier(n_estimators=n_esti, max_depth=depth, max_features=mode, random_state=randomSeed)
gbc.fit(trainingX, trainingY)
predictLabel = gbc.predict(testingX) if track == 'track2' else gbc.predict_proba(testingX)

print('feautre importance:')
print(gbc.feature_importances_)

if track == 'track2':
	predictLabel = predictLabel.astype(numpy.int64)
print(predictLabel)

# output result to file
with open('result/GB_'+str(n_esti)+'_'+str(depth)+'_'+str(mode)+'_mix75_'+track+'.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for label in predictLabel:
		if track == 'track2':
			writer.writerow([label])
		else:
			writer.writerow([label[1]])

