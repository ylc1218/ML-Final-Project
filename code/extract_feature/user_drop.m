clear;

T = readtable('enrollment_train.csv');

course_id = T.course_id;
username = T.username;
enrollement_id = T.enrollment_id;

course_list = unique(course_id);
[user_list, ia, ic] = unique(username);
user_take_course_num = accumarray(ic(:), 1);

truth_train = readtable('truth_train.csv');
truth_train = truth_train.drop;

tic;
drop_num = zeros(size(user_list));
for i = 1:length(user_list)
    index = strcmp(username, user_list{i});
    drop_num(i) = sum(truth_train( index ));
end
toc

%  drop ratio
drop_ratio = zeros(size(user_list));
drop_ratio = drop_num./user_take_course_num;

B = table(user_list,drop_ratio,'VariableNames',{'username' 'user_drop_ratio'});

result = join(T, B);

