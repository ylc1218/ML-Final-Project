function user_hist = time_interval_day(log_file, min_time_path, interval)

    enrollment_id = log_file.enrollment_id;
    id_list = unique(enrollment_id);

    min_time = readtable(min_time_path);
    min_time = min_time.min_time;

    user_hist = zeros(length(id_list) ,ceil(30/interval) );
    
    fprintf('there are %d users\n', length(id_list));
    for i = 1:length(id_list)

        if( mod(i, 1000) ==  0 )
            fprintf('doing %dth user... \n', i);
        end
        T = log_file( log_file.enrollment_id == id_list(i), {'enrollment_id', 'time'});
        time = T.time;

        ref = datevec(min_time(i), 'yyyy-mm-dd');
        current = -1;       
        week = 0;
        for j = 1:length(time)
            d1 = datevec(time(j), 'yyyy-mm-dd');
            day_diff = floor( etime(d1, ref)/60/60/24 );
            if mod(day_diff, interval) == current && week == (floor(day_diff/interval) + 1)
                continue;
            end
            week = floor(day_diff/interval) + 1;
            current = mod(day_diff, interval);
            user_hist(i, week) = user_hist(i, week) + 1;
        end

    end

end