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
    freopen("test_id_mintime_objmintime.txt", "r", stdin);
    FILE* out = fopen("test_course_access_diff.csv", "w");

    int eid;
    char min_time[100], min_obj[100];
    int y, mth, d, h, m, s;
    int y_obj, mth_obj, d_obj, h_obj, m_obj, s_obj;
    float time_diff;
    struct tm log_time, obj_time;
    int tmp = 0;

    scanf("%*s%*s%*s");
    while(~scanf("%d%s%s", &eid, min_time, min_obj)){
        sscanf(min_time, "%d-%d-%dT%d:%d:%d", &y, &mth, &d, &h, &m, &s);
        sscanf(min_obj, "%d-%d-%dT%d:%d:%d", &y_obj, &mth_obj, &d_obj, &h_obj, &m_obj, &s_obj);

        log_time = {s, m, h, d, mth-1, y-1900};
        obj_time = {s_obj, m_obj, h_obj, d_obj, mth_obj-1, y_obj-1900};
        time_diff = secDiff(obj_time, log_time)/60/60/24;

        time_diff = time_diff < 0 ? 0 : time_diff;
        fprintf(out, "%f\n", time_diff);
    }

    return 0;
}
