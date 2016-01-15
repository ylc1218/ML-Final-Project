import csv
import numpy
import sys
from sklearn import ensemble
from sklearn import cross_validation as CV
from sklearn import preprocessing as pre

# chekc track is specified
if(len(sys.argv) < 2):
	print("please specify track, track = {track1, track2}")
	exit(1)
track = sys.argv[1]


# load sample feature (training)
with open('data/mix85_train.csv', 'r') as train_x_csv:
	reader = csv.reader(train_x_csv, delimiter=',')
	next(reader)
	x=list(reader)
	trainingData=numpy.array(x).astype('double')

# assign sample weight = 1/take_course_num
if track == 'track2':
	sampleWeight = 1/trainingData[:, 1]
else:
	sampleWeight = numpy.array([1]*trainingData.shape[0])

# load labels (training)
with open('data/truth_train.csv', 'r') as train_y_csv:
	reader = csv.reader(train_y_csv, delimiter=',')
	x=list(reader)
	trainingY=numpy.array(x).astype('double')
# trainingY = [1, -1]
trainingY=trainingY[:, 1]
# print(trainingY)

# load sample feature (testing)
with open('data/mix85_test.csv', 'r') as test_x_csv:
	reader = csv.reader(test_x_csv, delimiter=',')
	next(reader)
	x=list(reader)
	testingData=numpy.array(x).astype('double')

featureIndices = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 23, 47, 48, 49, 50, 57, 58, 59, 60, 61, 62, 63, 65, 66, 26]
featureCandidates = [16, 17, 18, 19, 20, 21, 22, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 51, 52, 53, 54, 55, 56, 64, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87]
bestFeature = 0
randomSeed = 1126
print('randomSeed = ' + str(randomSeed))	

for i in range(len(featureCandidates)):
	nowFeatures = featureIndices + [featureCandidates[i]]
	print('adding feature' + str(featureCandidates[i]))
	# add the specific column
	trainingX = trainingData[:, nowFeatures]
	# print('load trainingX with shape = ' + str(trainingX.shape))
	testingX = testingData[:, nowFeatures]
	# print('load testingX with shape = ' + str(testingX.shape))

	bestCV = 0
	params = []
	for n_esti in [400]:
		for depth in [4]:
			for max_feature in ['auto']: # 'auto' = None
				params.append([n_esti, depth, max_feature])

	scoring = 'accuracy' if track == 'track2' else 'average_precision'

	# Cross-validation
	for param in params:
		# print(param)

		gbc = ensemble.GradientBoostingClassifier(n_estimators=param[0], max_depth=param[1], max_features=param[2], random_state=randomSeed)
		cvScores = CV.cross_val_score(gbc, trainingX, trainingY, scoring=scoring, cv=5, n_jobs=5)
		if cvScores.mean() > bestCV:
			bestCV = cvScores.mean()
			bestParam = param
			bestFeature = featureCandidates[i]
		print(cvScores.mean())


print(bestScore)
print(bestParam)
gbc = ensemble.GradientBoostingClassifier(n_estimators=bestParam[0], max_depth=bestParam[1], max_features=bestParam[2], random_state=randomSeed)
gbc.fit(trainingX, trainingY)
predictLabel = gbc.predict(testingX) if track == 'track2' else gbc.predict_proba(testingX)

if track == 'track2':
	predictLabel = predictLabel.astype(numpy.int64)
print(predictLabel)

# output result to file
with open('result/GB_FS_mix85_'+track+'.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for label in predictLabel:	
		if track == 'track2':
			writer.writerow([label])
		else:
			writer.writerow([label[1]])

