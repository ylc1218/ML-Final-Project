function unique_cnt = unique_cnt(log_file)

    enrollment_id = log_file.enrollment_id;
    id_list = unique(enrollment_id);

    % video, problem, discussion
    unique_cnt = zeros(length(id_list), 3);
    event = {'video', 'problem', 'discussion'};
   
    fprintf('there are %d users\n', length(id_list));
    for i = 1:length(id_list)
        if( mod(i, 1000) ==  0 )
            fprintf('doing %dth user... \n', i);
        end
        T = log_file( log_file.enrollment_id == id_list(i), {'event', 'object'});
        for j = 1:3
            tmp = T( strcmp(T.event,event(j)), {'object'});
            unique_cnt(i, j) = length( unique(tmp.object) );
        end
    end

end