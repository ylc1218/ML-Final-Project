import csv
import numpy
import sys
from sklearn import ensemble
from sklearn.decomposition import PCA
from sklearn import cross_validation as CV

# chekc track is specified
if(len(sys.argv) < 2):
	print("please specify track, track = {track1, track2}")
	exit(1)
track = sys.argv[1]

# load sample feature (training)
with open('data/mix_train.csv', 'r') as train_x_csv:
	reader = csv.reader(train_x_csv, delimiter=',')
	next(reader)
	x=list(reader)
	trainingX=numpy.array(x).astype('double')

# selectedFeatures = [2, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 24, 25, 26, 28, 29, 33]

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
with open('data/mix_test.csv', 'r') as test_x_csv:
	reader = csv.reader(test_x_csv, delimiter=',')
	next(reader)
	x=list(reader)
	testingX=numpy.array(x).astype('double')

# remove the 4th column (take_course_num)
testingX = numpy.delete(testingX, 3, 1)
print('load testingX with shape = ' + str(testingX.shape))
# testingX=testingX[:, selectedFeatures]

# print(testingX)


# PCA decomposition 
# pca = PCA(n_components=12)
# trainingX = pca.fit_transform(trainingX)
# testingX = pca.fit_transform(testingX)

params = []
for n_esti in [8000, 10000, 12000]:
	for depth in [8, 10, 12, 14]:
		params.append([n_esti, depth])

# rfc.fit(trainingX, trainingY)

bestParam = []
bestScore = 0
scoring = 'accuracy' if track == 'track2' else 'average_precision'
	
fit_params = dict()
fit_params['sample_weight'] = sampleWeight;

# Cross-validation
for param in params:
	print(param)
	# random forest
	rfc = ensemble.RandomForestClassifier(n_estimators=param[0], n_jobs=16, max_depth=param[1])
	cvScores = CV.cross_val_score(rfc, trainingX, trainingY, scoring=scoring, cv=5, fit_params=fit_params)
	if cvScores.mean() > bestScore:
		bestScore = cvScores.mean()
		bestParam = param
	print(cvScores.mean())

# bestParam = params[0]
print(bestScore)
print(bestParam)
rfc = ensemble.RandomForestClassifier(n_estimators=bestParam[0], n_jobs=20, max_depth=bestParam[1])
rfc.fit(trainingX, trainingY, sample_weight=sampleWeight)
predictLabel = rfc.predict(testingX) if track == 'track2' else rfc.predict_proba(testingX)

print(predictLabel)

# output result to file
with open('RF_CV_mix_weight_'+track+'.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for label in predictLabel:
		if track == 'track2':
			writer.writerow([label])
		else:
			writer.writerow([label[1]])

