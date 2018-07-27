#include <stdio.h>

int main(int argc, char *argv[])
{
    char appMain[] = "/run/media/rizwan/Work/Work/Hash-Checker-Dev/main.py";
    char launcher[100];

    if(argc == 2) {
        sprintf(launcher, "python3 %s %s", appMain, argv[1]);
        printf("%s", argv[1]);
        system(launcher);
    }
    else {
        sprintf(launcher, "python3 %s", appMain);
        system(launcher);
    }
    return 0;
}
