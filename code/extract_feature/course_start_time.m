clear;   
course_min_time = readtable('cid_minstart.csv');
id_course = readtable('enrollment_train.csv');
id_min_max_time = readtable('train_mintime_maxtime.csv');

T = join(id_min_max_time, id_course);
T = join(T, course_min_time);

myTable = T(:, [1,2,7]);


% course_min_time = readtable('cid_minstart.csv');
% id_course = readtable('enrollment_test.csv');
% id_min_max_time = readtable('test_mintime_maxtime.csv');
% 
% T = join(id_min_max_time, id_course);
% T = join(T, course_min_time);
% 
% myTable = T(:, [1,2,8]);