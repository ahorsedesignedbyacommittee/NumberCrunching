#include <stdio.h>
#include <stdlib.h>

int main(void) {

    char c;
    FILE *fp = fopen("quine.c", "r");
    while ((c = fgetc(fp)) != EOF) putchar(c);
    return 0;
}
