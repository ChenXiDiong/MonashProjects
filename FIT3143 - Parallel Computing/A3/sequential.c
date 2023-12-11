#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

#define N 10000
#define WIDTH 100

void random_ints(int *arr, int size){
    for(int i = 0; i < size; i++){
        arr[i] = (i+1) % 1000;
    }
}

int main() {
    int *a, *b, *c;
    int size = N * sizeof(int);
    struct timespec start, end;
    double time_taken = 0.0;

    printf("Running Serial Matrix Multiplication\n");

    // Setup input values
    a = (int *)malloc(size * sizeof(int));
    b = (int *)malloc(size * sizeof(int));
    c = (int *)malloc(size * sizeof(int));

    // Initialize input values
    random_ints(a, N);
    random_ints(b, N);

    for(int i = 0; i < WIDTH; i++){
        for(int j = 0; j < WIDTH; j++){
            c[i * WIDTH + j] = 0;
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &start);

    // perform 2D matrix multiplication in serial
    #pragma omp parallel for num_threads(1)
    for(int i = 0; i < WIDTH; i++){
        for(int j = 0; j < WIDTH; j++){
            for(int k = 0; k < WIDTH; k++){
                c[i * WIDTH + j] += a[i * WIDTH + k] * b[k * WIDTH + j];
            }
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    time_taken = end.tv_sec - start.tv_sec;
    time_taken += (end.tv_nsec - start.tv_nsec) / 1000000.0;
    printf("Total time taken (milliseconds): %.8f\n", time_taken);

    FILE *fp;
    fp = fopen("seq_output.txt", "w");
    for(int i=0; i<N; i++) {
        fprintf(fp, "%d ", c[i]);
        if((i + 1) % WIDTH == 0) fprintf(fp, "\n");
    }
    fclose(fp);

    
    // Cleanup
    free(a); free(b); free(c);

    return 0;
}