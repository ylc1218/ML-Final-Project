#include<cstdio>
#include<cstdlib>
#include<iostream>
#include<ctime>
#include<cstring>
#define LOWB    60
#define UPB     7200
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
    freopen("train_eid_time_event_cid.txt", "r", stdin);
    freopen("train_video_out.txt", "w", stdout);

    int cureid=-1, eid;
    int y, mth, d, h, m, s;
    int total_time=0;
    char event[20], course[150], curCourse[150];
    bool nowVideo=false;
    struct tm vstart, vend;

    scanf("%*s%*s%*s%*s");
    while(~scanf("%d %d-%d-%dT%d:%d:%d %s %s", &eid, &y, &mth, &d, &h, &m, &s, event, course)){
        //printf("%d %d %d %d %d %d %d %s\n", eid, y, mth, d, h, m, s, event);
        if(eid!=cureid){
            if(cureid!=-1){
                printf("%d\t%d\t%s\t%s\n", cureid, total_time, curCourse, "train");
            }
            cureid=eid;
            strcpy(curCourse, course);
            total_time=0;
            if(event[0]=='v'){
                nowVideo=true;
                vstart={s,m,h,d,mth-1,y-1900};
            }
            else nowVideo=false;
            continue;
        }

        if(nowVideo==true){
            vend={s,m,h,d,mth-1,y-1900};
            int s = secDiff(vstart, vend);
            if(LOWB<=s && s<=UPB){
                total_time+=s;
                //printf("%d\t%d\t%s\t%s\n", eid, s, course, "train");
            }
            nowVideo=false;
        }

        if(event[0]=='v'){
            nowVideo=true;
            vstart={s,m,h,d,mth-1,y-1900};
            continue;
        }

    }
    printf("%d\t%d\t%s\t%s\n", cureid, total_time, curCourse, "train");
    return 0;
}
