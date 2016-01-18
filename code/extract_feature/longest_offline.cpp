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
    FILE* out = fopen("train_continuous_day.csv", "w");

    int current_eid = -1, eid;
    int max_day = 1, min_day = 100, day_cnt;
    char current_day[100], prev_day[100];
    int y, mth, d, h, m, s;
    int day_diff, week;

    struct tm prev_time, log_time, last_time;
    int tmp = 0;

    scanf("%*s,%*s,%*s,%*s,%*s");
    while(~scanf("%d,%d-%d-%dT%*d:%*d:%*d,%*s,%*s,%*s", &eid, &y, &mth, &d)){
        //printf("%d %d %d %d %d %d %d\n", eid, y, mth, d, h, m, s);
        if(eid != current_eid){
            // final check
            day_diff = secDiff(prev_time, last_time)/60/60/24;
            max_day = (day_diff > max_day)?day_diff:max_day;
            fprintf(out, "%d\n", max_day);

            prev_time = {0, 0, 0, d, mth-1, y-1900};
            last_time = {0, 0, 0, d+29, mth-1, y-1900};
            current_eid = eid;
            max_day = -1;
        }

        log_time = {0, 0, 0, d, mth-1, y-1900};
        day_diff = secDiff(prev_time, log_time)/60/60/24;
        max_day = (day_diff > max_day)?day_diff:max_day;

        prev_time = {0, 0, 0, d, mth-1, y-1900};

    }

    day_diff = secDiff(prev_time, last_time)/60/60/24;
    max_day = (day_diff > max_day)?day_diff:max_day;
    fprintf(out, "%d\n",max_day);

    return 0;
}
