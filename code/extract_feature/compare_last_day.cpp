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
    freopen("train_mintime_maxtime.txt", "r", stdin);
    FILE* out = fopen("train_diff_time.csv", "w");

    int current_eid = -1, eid;
    int current_diff = -1, current_week = 0;
    int interval = 7;
    int min_y, min_d, min_mth, last_y, last_mth, last_d;
    int day_diff, week;
    struct tm max_time, last_access_time;
    char str1[100], str2[100];
    int tmp = 0;

    scanf("%*s%*s%*s%*s");
    while(~scanf("%d%s%s%*s", &eid, str1, str2)){

        sscanf(str1, "%d-%d-%dT%*d:%*d:%*d", &min_y, &min_mth, &min_d);
        sscanf(str2, "%d-%d-%dT%*d:%*d:%*d", &last_y, &last_mth, &last_d);


        //printf("%s||%s\n", str1, str2);
        //printf("%d-%d-%d, %d-%d-%d\n", min_y, min_mth, min_d, last_y, last_mth, last_d);

        max_time = {0, 0, 0, min_d+29, min_mth-1, min_y-1900};
        last_access_time = {0, 0, 0, last_d, last_mth-1, last_y-1900};
        day_diff = secDiff(last_access_time, max_time)/60/60/24;

        fprintf(out, "%d\n", day_diff);

    }
    return 0;
}
