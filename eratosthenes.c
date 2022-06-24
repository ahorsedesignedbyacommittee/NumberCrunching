#include <stdio.h>
#include <stdlib.h>
#define CEILING 5000 // Maximum integer up to which primes are found

void strike_multiples(int n, int *storage); // Function prototype

int main(void) {
    int *ptr = malloc(sizeof(int) * CEILING);  // Create buffer in memory
    int no_of_primes_found = 0;
    for (int i = 0; i < CEILING; i++) {  // Initialise all elements in buffer to zero
        ptr[i] = 0;
    }
    
    for (int j = 2; j < (CEILING / 2) + 1; j++) {
        if (ptr[j] == 0) {
            strike_multiples(j, ptr);
        }
    }
    
    for (int k = 2; k < CEILING; k++) {
        if (ptr[k] == 0) {
            no_of_primes_found++;
            printf("%i\n", k);
        }
    }
    
    printf("%i primes found\n", no_of_primes_found);
    
    free(ptr);
    return 0;
}


void strike_multiples(int n, int *storage) {  // This function strikes all multiples of a given integer within the range
    for (int i = 2; i < (CEILING / n) + 1; i++) {   // (striking means setting the value of the corresponding index in the allocated memory to one)
        storage[i*n] = 1;
    }
}
