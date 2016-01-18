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
    freopen("log_test.csv", "r", stdin);
    FILE* out = fopen("test_session_cnt.csv", "w");

    int current_eid = -1, eid;
    int current_diff = -1, current_week = 0;
    int interval = 7;
    int y, mth, d, h, m, s;
    int day_diff, week, hour_diff;
    struct tm log_time, prev_time;
    char str1[100], str2[100];
    int tmp = 0;
    int session_cnt = 0;

    scanf("%*s,%*s,%*s,%*s,%*s");
    while(~scanf("%d,%d-%d-%dT%d:%d:%d,%*s,%*s,%*s", &eid, &y, &mth, &d, &h, &m, &s)){

        if(current_eid != eid){
            fprintf(out, "%d\n", session_cnt);

            session_cnt = 1;
            prev_time = {s, m, h, d, mth-1, y-1900};
            current_eid = eid;
        }

        log_time = {s, m, h, d, mth-1, y-1900};
        hour_diff = secDiff(prev_time, log_time)/60/60;

        if(hour_diff >= 2){
            session_cnt++;
        }

        prev_time = log_time;
    }

    fprintf(out, "%d\n", session_cnt);
    return 0;

}
