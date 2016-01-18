% clear;
% log_test = readtable('log_test.csv');
% log_train = readtable('log_train.csv');
% id_course_test = readtable('enrollment_test.csv');
% id_course_train = readtable('enrollment_train.csv');
% object_module = readtable('object.csv');

course_list = unique(id_course_train.course_id);
video_total_cnt = zeros(length(course_list), 1);

event_type = 'problem';
for i = 1:length(course_list)
    
    fprintf('doing %dth course...\n', i);
    
    test_take_course = id_course_test( strcmp(id_course_test.course_id, course_list(i)), {'enrollment_id'});
    train_take_course = id_course_train( strcmp(id_course_train.course_id, course_list(i)), {'enrollment_id'});
    T_test = log_test( ismember(log_test.enrollment_id, test_take_course.enrollment_id)...
        & strcmp(log_test.event, event_type), {'object'});
    T_train = log_train( ismember(log_train.enrollment_id, train_take_course.enrollment_id)...
        & strcmp(log_train.event, event_type), {'object'});
    T_object = object_module( strcmp(object_module.course_id, course_list(i))...
        & strcmp(object_module.category, event_type), {'module_id'});
    
    total_object = unique(cat(1, T_test.object, T_train.object, T_object.module_id));
    video_total_cnt(i) = length(total_object);
end

B = table(course_list, video_total_cnt);
B.Properties.VariableNames{'course_list'} = 'course_id';
A = join(id_course_train, B);



