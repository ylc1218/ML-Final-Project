import csv
import numpy
from sklearn import ensemble
from sklearn.decomposition import PCA
from sklearn import cross_validation as CV

# load sample feature (training)
with open('new_train_x.csv', 'r') as train_x_csv:
	reader = csv.reader(train_x_csv, delimiter=',')
	next(reader)
	x=list(reader)
	trainingX=numpy.array(x).astype('double')

# trainingX = [[1, 2], [3, 4]]
# remove the first column (ID)
trainingX=trainingX[:, 1:]
print('load trainingX with shape = ' + str(trainingX.shape))

# load labels (training)
with open('truth_train.csv', 'r') as train_y_csv:
	reader = csv.reader(train_y_csv, delimiter=',')
	x=list(reader)
	trainingY=numpy.array(x).astype('double')
# trainingY = [1, -1]
	trainingY=trainingY[:, 1]
# print(trainingY)

# load sample feature (testing)
with open('new_test_x.csv', 'r') as test_x_csv:
	reader = csv.reader(test_x_csv, delimiter=',')
	next(reader)
	x=list(reader)
	testingX=numpy.array(x).astype('double')

# remove the first column (ID)
testingX=testingX[:, 1:]
print('load testingX with shape = ' + str(testingX.shape))
#print(testingX)
#testingX = [[3, 4], [3, 4], [1, 2], [1, 2]]

params = []
for n_esti in [8000, 10000, 12000]:
	for depth in [6, 8, 10, 12]:
		params.append([n_esti, depth])

bestParam = [];
bestScore = 0;
# Cross-validation
for param in params:
	print(param)
	# random forest
	rfc = ensemble.RandomForestClassifier(n_estimators=param[0], n_jobs=16, max_depth=param[1])
	cvScores = CV.cross_val_score(rfc, trainingX, trainingY, scoring='average_precision', cv=5)
	if cvScores.mean() > bestScore:
		bestScore = cvScores.mean()
		bestParam = param
	print(cvScores.mean())

print(bestScore)
print(bestParam)

# random forest
rfc = ensemble.RandomForestClassifier(n_estimators=bestParam[0], n_jobs=16, max_depth=bestParam[1])
rfc.fit(trainingX, trainingY)
predictProb = rfc.predict_proba(testingX)

print(predictProb)

# output result to file
with open('RF_CV_track1.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for label in predictProb:
		writer.writerow([label[1]])

