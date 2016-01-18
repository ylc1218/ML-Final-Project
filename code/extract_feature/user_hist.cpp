#include<cstdio>
#include<cstdlib>
#include<iostream>
#include<ctime>
#include<cstring>
#include <math.h>
#define LOWB 60
#define UPB 7200
using namespace std;

double secDiff(struct tm a, struct tm b){
    double difference=-1;
    time_t x = mktime(&a);
    time_t y = mktime(&b);
    if ( x != (time_t)(-1) && y != (time_t)(-1) )
    {
        difference = difftime(y, x);
    }
    return difference;
}

int main(){
    freopen("log_train.csv", "r", stdin);
    FILE* out = fopen("train_log_day.csv", "w");

    int current_eid = -1, eid;
    int current_diff = -1, current_week = 0;
    int interval = 7;
    int y, mth, d, h, m, s;
    int day_diff, week;
    int user_hist[6];
    struct tm first_time, log_time;
    int tmp = 0;

    scanf("%*s,%*s,%*s,%*s,%*s");
    while(~scanf("%d,%d-%d-%dT%d:%d:%d,%*s,%*s,%*s", &eid, &y, &mth, &d, &h, &m, &s)){
        //printf("%d %d %d %d %d %d %d\n", eid, y, mth, d, h, m, s);
        if(eid != current_eid){
            fprintf(out, "%d,%d,%d,%d,%d,%d\n", user_hist[0], user_hist[1],user_hist[2],
               user_hist[3],user_hist[4]);
            //printf("%d\n", eid);

            memset(user_hist, 0, sizeof(user_hist));
            first_time = {0, 0, 0, d, mth-1, y-1900};
            current_eid = eid;
            current_diff = -1;
            week = 0;
            user_hist[week]++;
            continue;
        }

        log_time = {0, 0, 0, d, mth-1, y-1900};
        day_diff = secDiff(first_time, log_time)/60/60/24;
        //printf("day_diff:%d, current_diff:%d, week:%d, current_week:%d\n", day_diff, current_diff, week, current_week);
        week = day_diff/interval;

        if( ((day_diff%interval) == current_diff) && (week == current_week) ){
            continue;
        }

        current_diff = day_diff%interval;
        current_week = week;

        //printf("current_week: %d\n", current_week);
        user_hist[current_week]++;

    }
    fprintf(out, "%d,%d,%d,%d,%d,%d\n", user_hist[0], user_hist[1],user_hist[2],
               user_hist[3],user_hist[4]);
    return 0;
}
