clear;

T_train = readtable('enrollment_train.csv');

course_id = T_train.course_id;
username = T_train.username;
enrollement_id = T_train.enrollment_id;

course_list = unique(course_id);

%  count student num of each course
course_num = zeros(size(course_list));
for i = 1:length(course_list)
    course_num(i) = sum( strcmp(course_list{i}, course_id) );
end

truth_train = readtable('truth_train.csv');
truth_train = truth_train.drop;
%  count drop num of each course
drop_num = zeros(size(course_list));
for i = 1:length(course_list)
    index = strcmp(course_id, course_list{i});
    drop_num(i) = sum(truth_train( index ));
end

%  drop ratio
drop_ratio = zeros(size(course_list));
drop_ratio = drop_num./course_num;

B = table(course_list,drop_ratio,'VariableNames',{'course_id' 'course_drop_ratio'});

train_result = join(T_train,B);
writetable(train_result, 'train_course_drop.csv');

T_test = readtable('enrollment_test.csv');
test_result = join(T_test, B);
writetable(test_result, 'test_course_drop.csv');




