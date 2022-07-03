#include <stdio.h>
#include <string.h>
#define CEILING 10000


unsigned long long collatz(unsigned long long n, int i) {
    if (n == 1)
    {
        return i;
    }
    else if (n % 2 == 0)
    {
        i++;
        collatz((n / 2), i);
    }
    else 
    {
        i++;
        collatz(( 3 * n + 1), i);
    }
}

int main(void)
{   
    FILE *fp = fopen("collatz_data.txt", "w");
    for (int j = 1; j <= CEILING; j++) {
        fprintf(fp,"%d,%llu\n", j, collatz(j, 0));
    }
    fclose(fp);
    return 0;
}
