function [user_hist, video_hist, problem_hist, discussion_hist] = time_interval(log_file, min_time_path, interval)

    enrollment_id = log_file.enrollment_id;
    id_list = unique(enrollment_id);

    min_time = readtable(min_time_path);
    min_time = min_time.min_time;

    user_hist = zeros(length(id_list) ,ceil(30/interval) );
    video_hist = zeros(length(id_list) ,ceil(30/interval) );
    problem_hist = zeros(length(id_list) ,ceil(30/interval) );
    discussion_hist = zeros(length(id_list) ,ceil(30/interval) );
    
    fprintf('there are %d users\n', length(id_list));
    for i = 1:length(id_list)

        if( mod(i, 1000) ==  0 )
            fprintf('doing %dth user... \n', i);
        end
        T = log_file( log_file.enrollment_id == id_list(i), {'enrollment_id', 'time', 'event'});
        time = T.time;
        event = T.event;

        ref = datevec(min_time(i), 'yyyy-mm-ddTHH:MM:SS');
        for j = 1:length(time)
            d1 = datevec(time(j), 'yyyy-mm-ddTHH:MM:SS');
            time_diff = floor( etime(d1, ref)/60/60/24 );
            user_hist(i, floor(time_diff/interval) + 1) = user_hist(i, floor(time_diff/interval) + 1) + 1;
            if strcmp(event(j), 'video')
                video_hist(i, floor(time_diff/interval) + 1) = video_hist(i, floor(time_diff/interval) + 1) + 1;
            elseif strcmp(event(j), 'problem')
                problem_hist(i, floor(time_diff/interval) + 1) = problem_hist(i, floor(time_diff/interval) + 1) + 1;
            elseif strcmp(event(j), 'discussion')
                discussion_hist(i, floor(time_diff/interval) + 1) = discussion_hist(i, floor(time_diff/interval) + 1) + 1;
            end
        end

    end

end