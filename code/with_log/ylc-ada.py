import csv
import numpy
import sys
import datetime
from sklearn import ensemble
from sklearn import cross_validation as CV

# chekc track is specified
if(len(sys.argv) < 5): #track, train_fileName, test_fileName, output_fileName
	print("please specify track = {track1, track2}, training data(x.csv), testing data(x.csv), output file(witout .csv)")
	exit(1)

timeStr = datetime.datetime.now().strftime("%m%d-%I%M%S")
log_file_name = timeStr+"_ada.log"
log_f = open(log_file_name, 'w', 0)

#assign variables
track = sys.argv[1]
train_fName=sys.argv[2]
test_fName=sys.argv[3]
output_fName=sys.argv[4]

print('Log file name: '+log_file_name)
print >>log_f, timeStr+'-ada'
print >>log_f, track+" "+train_fName+" "+test_fName+" "+output_fName 


# load sample feature (training)
with open(train_fName, 'r') as train_x_csv:
	reader = csv.reader(train_x_csv, delimiter=',')
	col_name=next(reader) #remove the first row(column name)
	print >>log_f, 'col used:'+str(col_name) #log column name used
	x=list(reader)
	trainingX=numpy.array(x).astype('double')

print >>log_f, '-----------'

# load labels (training)
with open('truth_train.csv', 'r') as train_y_csv:
	reader = csv.reader(train_y_csv, delimiter=',')
	x=list(reader) #remove the first row(column name)
	trainingY=numpy.array(x).astype('double')


# load sample feature (testing)
with open(test_fName, 'r') as test_x_csv:
	reader = csv.reader(test_x_csv, delimiter=',')
	next(reader) #remove the first row(column name)
	x=list(reader)
	testingX=numpy.array(x).astype('double')

# PCA decomposition 
# pca = PCA(n_components=12)
# trainingX = pca.fit_transform(trainingX)
# testingX = pca.fit_transform(testingX)

params = []
for n_esti in [200,500,1000,2000]:
	params.append([n_esti])

bestParam = [0]
bestScore = 0

# assign sample weight = 1/take_course_num
sampleWeight = 1/trainingX[:, 1] if track=='track2' else numpy.array([1]*trainingX.shape[0])
fit_params = dict()
#fit_params['sample_weight'] = sampleWeight;

scoring = 'accuracy'  if track=='track2' else 'average_precision'

# trim unused column
trainingX=trainingX[:, 2:] #id & take_course_num
trainingY=trainingY[:, 1] #id
testingX=testingX[:, 2:] #id & take_course_num

print('load trainingX with shape = ' + str(trainingX.shape))
print('load testingX with shape = ' + str(testingX.shape))
print >>log_f, 'load trainingX with shape = ' + str(trainingX.shape)
print >>log_f, 'load testingX with shape = ' + str(testingX.shape)



# Cross-validation
print >>log_f, '-----------'
for param in params:
	print(param)
	print >>log_f, str(param)+":"+datetime.datetime.now().strftime("%m%d-%I%M%S")
	# AdaBoost
	adac = ensemble.AdaBoostClassifier(n_estimators=param[0], random_state=1126)
	cvScores = CV.cross_val_score(adac, trainingX, trainingY, scoring=scoring, cv=5, n_jobs=5, fit_params=fit_params)
	if cvScores.mean() > bestScore:
		bestScore = cvScores.mean()
		bestParam = param

	print >>log_f, adac
	print(cvScores.mean())
	print >>log_f, ' ='+str(cvScores.mean())+','+datetime.datetime.now().strftime("%m%d-%I%M%S")+'\n'

# bestParam = params[0]
print(str(bestParam)+' '+str(bestScore))
print >>log_f, 'best:'+str(bestParam)+' '+str(bestScore)
adac = ensemble.AdaBoostClassifier(n_estimators=bestParam[0], random_state=1126)
adac.fit(trainingX, trainingY, sample_weight=sampleWeight)
predictLabel = adac.predict(testingX) if track == 'track2' else adac.predict_proba(testingX)

print(predictLabel)

# output result to file
with open(output_fName+'_ada_'+track+'.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for label in predictLabel:
		if track == 'track2':
			writer.writerow([label])
		else:
			writer.writerow([label[1]])
print(log_f)
log_f.close()




