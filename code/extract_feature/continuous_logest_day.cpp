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
    FILE* check = fopen("check", "w");

    int current_eid = -1, eid;
    int max_day = 1, min_day = 100, day_cnt;
    char current_day[100], prev_day[100];
    int y, mth, d, h, m, s;
    int day_diff, week;

    struct tm prev_time, log_time;
    int tmp = 0;

    scanf("%*s,%*s,%*s,%*s,%*s");
    while(~scanf("%d,%d-%d-%dT%*d:%*d:%*d,%*s,%*s,%*s", &eid, &y, &mth, &d)){

        if(eid != current_eid){
            fprintf(out, "%d\n", max_day);

            prev_time = {0, 0, 0, d, mth-1, y-1900};
            day_cnt = 1;
            max_day = 1;

            current_eid = eid;
            //tmp ++;
            //if( tmp == 2) break;
        }

        log_time = {0, 0, 0, d, mth-1, y-1900};
        day_diff = secDiff(prev_time, log_time)/60/60/24;
        prev_time = {0, 0, 0, d, mth-1, y-1900};
        //if( current_eid == 51 )
         //   fprintf(check, "eid: %d\ttime: %d-%d-%d\tday_diff: %d\tdat_cnt: %d\n", current_eid, y, mth, d,day_diff, day_cnt);

        if( day_diff == 0) continue;

        if(day_diff == 1){
            day_cnt++;
        }
        else{
            // not continuous
            max_day = (day_cnt > max_day)?day_cnt:max_day;
            day_cnt = 1;
        }

    }

    fprintf(out, "%d\n", max_day);

    return 0;
}
