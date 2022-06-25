#include <stdio.h>
#include <stdlib.h>

int main(void) {

    char c;
    FILE *fp = fopen(__FILE__, "r");
    while ((c = fgetc(fp)) != EOF) putchar(c);
    fclose(fp);
    return 0;
}
