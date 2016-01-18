#include<cstdio>
#include<cstdlib>
#include<iostream>
#include<ctime>
using namespace std;

int main(){
    int eid;
    struct tm s,e;
    time_t tms, tme;

    freopen("cid_mintime_maxtime.txt", "r", stdin);
    freopen("out.txt", "w", stdout);
    int sy,sm,sd,ey,em,ed;
    while(~scanf("%d %d-%d-%d%*s %d-%d-%d%*s", &eid, &sy,&sm,&sd,&ey,&em,&ed)){
        struct std::tm a = {0,0,0,sd,sm-1,sy-1900}; /* June 24, 2004 */
        struct std::tm b = {0,0,0,ed,em-1,ey-1900}; /* July 5, 2004 */
        std::time_t x = std::mktime(&a);
        std::time_t y = std::mktime(&b);
        if ( x != (std::time_t)(-1) && y != (std::time_t)(-1) )
        {
            double difference = std::difftime(y, x) / (60 * 60 * 24);
            /*std::cout << std::ctime(&x);
            std::cout << std::ctime(&y);*/
            std::cout << eid << "\t" << difference << std::endl;
        }

    }

    return 0;
}
