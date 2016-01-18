#include<cstdio>
#include<cstdlib>
#include<iostream>
#include<ctime>
#include<cstring>
#include <math.h>
#define LOWB 60
#define UPB 7200
using namespace std;

int dayofweek(int d, int m, int y)
{
    static int t[] = { 0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4 };
    y -= m < 3;
    return ( y + y/4 - y/100 + y/400 + t[m-1] + d) % 7;
}
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
    freopen("test_mintime_maxtime.txt", "r", stdin);
    FILE* out = fopen("test_enroll.csv", "w");

    int current_eid = -1, eid;
    int current_diff = -1, current_week = 0;
    int interval = 7;
    int y, mth, d;
    int day_diff, week;
    struct tm max_time, last_access_time;
    char str1[100], str2[100];
    int tmp = 0;

    scanf("%*s%*s%*s%*s");
    while(~scanf("%d%s%*s%*s", &eid, str1)){

        sscanf(str1, "%d-%d-%dT%*d:%*d:%*d", &y, &mth, &d);

        fprintf(out, "%d, %d, %d, %d\n", y, mth, dayofweek(d, mth, y), d);

    }
    return 0;
}
