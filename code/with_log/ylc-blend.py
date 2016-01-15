import csv
import numpy
import sys
import datetime
import numpy as np
from sklearn import ensemble
from sklearn import cross_validation as CV
from sklearn.linear_model import LogisticRegression

# chekc track is specified
if(len(sys.argv) < 5): #track, train_fileName, test_fileName, output_fileName
	print("please specify track = {track1, track2}, training data(x.csv), testing data(x.csv), output file(witout .csv)")
	exit(1)

timeStr = datetime.datetime.now().strftime("%m%d-%I%M%S")
log_file_name = timeStr+"_blend.log"
log_f = open(log_file_name, 'w', 0)

#assign variables
track = sys.argv[1]
train_fName=sys.argv[2]
test_fName=sys.argv[3]
output_fName=sys.argv[4]+'_log_blend_'+track+'.csv'

print('Log file name: '+log_file_name)
print >>log_f, timeStr+'-blend'
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


# trim unused column
trainingX=trainingX[:, 2:] #id & take_course_num
trainingY=trainingY[:, 1] #id
testingX=testingX[:, 2:] #id & take_course_num

print('load trainingX with shape = ' + str(trainingX.shape))
print('load testingX with shape = ' + str(testingX.shape))
print >>log_f, 'load trainingX with shape = ' + str(trainingX.shape)
print >>log_f, 'load testingX with shape = ' + str(testingX.shape)

shuffle=False
#create CV flods
if shuffle:
    idx = np.random.permutation(trainingY.size)
    trainingX = trainingX[idx]
    trainingY = trainingY[idx]

skf = list(CV.StratifiedKFold(trainingY, 5))
rf_param=[2000,12] #n_est, depth
gb_param=[400,4,'auto'] #n_est, depth
ada_param=[1000] #n_est

clfs = [ensemble.RandomForestClassifier(n_estimators=rf_param[0], n_jobs=16, max_depth=rf_param[1], max_features=0.5, random_state=1126),
        ensemble.GradientBoostingClassifier(n_estimators=gb_param[0], max_depth=gb_param[1], max_features=gb_param[2], random_state=1126),
        ensemble.AdaBoostClassifier(n_estimators=ada_param[0], random_state=1126)
        ]

dataset_blend_train = np.zeros((trainingX.shape[0], len(clfs)))
dataset_blend_test = np.zeros((testingX.shape[0], len(clfs)))

# Cross-validation
for j, clf in enumerate(clfs):
    print j, clf
    print >>log_f, clf
    dataset_blend_test_j = np.zeros((testingX.shape[0], len(skf)))
    for i, (train, test) in enumerate(skf):
        print "Fold", i
        X_fold_train = trainingX[train]
        y_fold_train = trainingY[train]
        X_fold_test = trainingX[test]
        y_fold_test = trainingY[test]
        clf.fit(X_fold_train, y_fold_train)
        if track=='track1':
        	y_submission = clf.predict_proba(X_fold_test)[:,1]
        	dataset_blend_train[test, j] = y_submission
        	dataset_blend_test_j[:, i] = clf.predict_proba(testingX)[:,1]
        else:
        	y_submission = clf.predict(X_fold_test)
        	dataset_blend_train[test, j] = y_submission
        	dataset_blend_test_j[:, i] = clf.predict(testingX)
    if track=='track1':
    	dataset_blend_test[:,j] = dataset_blend_test_j.mean(1)
    else:
    	test_sum=np.sum(dataset_blend_test_j, 1)
    	test_sum[test_sum>=test_sum.size/2]=1
    	dataset_blend_test[:,j] = test_sum

#blend
clf = LogisticRegression()
clf.fit(dataset_blend_train, trainingY)
if track=='track1':
	y_submission = clf.predict_proba(dataset_blend_test)[:,1]
	#Linear stretch of predictions to [0,1]
	y_submission = (y_submission - y_submission.min()) / (y_submission.max() - y_submission.min())
else:
	y_submission = clf.predict(dataset_blend_test)

print >>log_f, clf
np.savetxt(fname=output_fName, X=y_submission, fmt='%f')
print(log_f)
log_f.close()
