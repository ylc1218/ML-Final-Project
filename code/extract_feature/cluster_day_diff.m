clear;

train_mix  = readtable('reg_mix_train.csv');
test_mix  = readtable('reg_mix_test.csv');
test_mix.Properties.VariableNames('ID') = {'enrollment_id'};
train_mix.Properties.VariableNames('ID') = {'enrollment_id'};

truth = readtable('../../truth_train.csv');
T = join(train_mix, truth);
% T = test_mix;

day_diff_1 = T(T.day_diff <= 9, 1:end-1);
day_diff_1_truth = T(T.day_diff <= 9, [1, end]);
day_diff_2 = T(T.day_diff >= 10 & T.day_diff <= 19, 1:end-1);
day_diff_2_truth = T(T.day_diff >= 10 & T.day_diff <= 19, [1, end]);
day_diff_3 = T(T.day_diff >= 20, 1:end-1);
day_diff_3_truth = T(T.day_diff >= 20, [1, end]);

writetable( day_diff_1, 'train_day_diff_1.csv');
writetable( day_diff_1_truth, 'train_day_diff_1_truth.csv');
writetable( day_diff_2, 'train_day_diff_2.csv');
writetable( day_diff_2_truth, 'train_day_diff_2_truth.csv');
writetable( day_diff_3, 'train_day_diff_3.csv');
writetable( day_diff_3_truth, 'train_day_diff_3_truth.csv');