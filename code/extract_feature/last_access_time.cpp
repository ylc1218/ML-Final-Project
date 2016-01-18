#include<cstdio>
#include<cstdlib>
#include<iostream>
#include<ctime>
#include<cstring>
#include <math.h>

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
    FILE* out = fopen("train_last_access.csv", "w");

    int eid;
    int y, mth, d, h, m, s;
    float time_diff;
    struct tm first_time, log_time;
    int tmp = 0;

    scanf("%*s%*s%*s%*s");
    scanf("%d%*s%d-%d-%dT%d:%d:%d%*s", &eid, &y, &mth, &d, &h, &m, &s);
    first_time = {s, m, h, d, mth-1, y-1900};
    //printf("%d %d %d %d %d %d %d\n", eid, y, mth, d, h, m, s);

    while(~scanf("%d%*s%d-%d-%dT%d:%d:%d%*s", &eid, &y, &mth, &d, &h, &m, &s)){

        log_time = {s, m, h, d, mth-1, y-1900};
        time_diff = secDiff(first_time, log_time)/60/60/24;

        fprintf(out, "%f\n", time_diff);
        //printf("%d\n", time_diff);
    }

    return 0;
}
