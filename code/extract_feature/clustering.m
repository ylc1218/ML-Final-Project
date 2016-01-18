clear;

train_mix = csvread('reg_mix_train.csv', 1, 0);
train_truth = csvread('../../truth_train.csv', 1, 0);
% test_mix = csvread('reg_mix_test.csv', 1, 0);

k = 3;
cluster = KmeansClustering(train_mix(:, 3:end), k);

% test_cluster_1 = table(test_mix(cluster == 1, :));
% test_cluster_2 = table(test_mix(cluster == 2, :));
% test_cluster_3 = table(test_mix(cluster == 3, :));
% % test_cluster_4 = table(test_mix(cluster == 4, :));
% % test_cluster_5 = table(test_mix(cluster == 5, :));
% 
% writetable( test_cluster_1, 'test_cluster_1.csv');
% writetable( test_cluster_2, 'test_cluster_2.csv');
% writetable( test_cluster_3, 'test_cluster_3.csv');
% % writetable( test_cluster_4, 'test_cluster_4.csv');
% % writetable( test_cluster_5, 'test_cluster_5.csv');

train_cluster_1 = table(train_mix(cluster == 1, :));
train_cluster_1_truth = table(train_truth(cluster == 1, :));
train_cluster_2 = table(train_mix(cluster == 2, :));
train_cluster_2_truth = table(train_truth(cluster == 2, :));
train_cluster_3 = table(train_mix(cluster == 3, :));
train_cluster_3_truth = table(train_truth(cluster == 3, :));
% train_cluster_4 = table(train_mix(cluster == 4, :));
% train_cluster_4_truth = table(train_truth(cluster == 4, :));
% train_cluster_5 = table(train_mix(cluster == 5, :));
% train_cluster_5_truth = table(train_truth(cluster == 5, :));
% 
writetable( train_cluster_1, 'train_cluster_1.csv');
writetable( train_cluster_1_truth, 'train_cluster_1_truth.csv');
writetable( train_cluster_2, 'train_cluster_2.csv');
writetable( train_cluster_2_truth, 'train_cluster_2_truth.csv');
writetable( train_cluster_3, 'train_cluster_3.csv');
writetable( train_cluster_3_truth, 'train_cluster_3_truth.csv');
% writetable( train_cluster_4, 'train_cluster_4.csv');
% writetable( train_cluster_4_truth, 'train_cluster_4_truth.csv');
% writetable( train_cluster_5, 'train_cluster_5.csv');
% writetable( train_cluster_5_truth, 'train_cluster_5_truth.csv');