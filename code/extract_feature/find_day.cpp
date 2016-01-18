/* A program to find day of a given date */
#include<stdio.h>
#include<cstdio>
#include<cstdlib>
#include<iostream>
#include<ctime>
#include<cstring>
#include <math.h>
using namespace std;

int dayofweek(int d, int m, int y)
{
    static int t[] = { 0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4 };
    y -= m < 3;
    return ( y + y/4 - y/100 + y/400 + t[m-1] + d) % 7;
}

int main(){
    freopen("log_test.csv", "r", stdin);
    FILE* out = fopen("test_hist_day.csv", "w");

    int eid, current_eid = -1;
    int y, mth, d, h, m, s;
    int day = -1;
    int user_hist[7];

    scanf("%*s,%*s,%*s,%*s");
    while(~scanf("%d,%d-%d-%dT%d:%d:%d,%*s,%*s,%*s", &eid, &y, &mth, &d, &h, &m, &s)){
        if( current_eid != eid){
            fprintf(out, "%d,%d,%d,%d,%d,%d,%d\n", user_hist[1],user_hist[2],
               user_hist[3],user_hist[4],user_hist[5], user_hist[6], user_hist[0]);

            current_eid = eid;
            memset(user_hist, 0, sizeof(user_hist));
        }
        day = dayofweek(d, mth, y);
        user_hist[day]++;

    }
    fprintf(out, "%d,%d,%d,%d,%d,%d,%d\n", user_hist[1],user_hist[2],
               user_hist[3],user_hist[4],user_hist[5], user_hist[6], user_hist[0]);
    return 0;
}
