/*
S2 2023 FIT3143 Parallel Computing Assignment 1
Name: Chen Xi Diong
Student ID: 32722656
Email: cdio0004@student.monash.edu

Parallel Code File.
This is the parallel algorithm to count unique instances in word files using OpenMP. 
The string pattern matching algorithm implemented is the Z-algorithm.

References:
1. The unique word count algorithm is referenced from the code provided in the Moodle tab for this unit.
2. All word files are sourced from the Moodle tab for this unit.
-MOBY_DICK.txt
-LITTLE_WOMEN.txt
-SHAKESPEARE.txt
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>
#include <string.h>
#include <ctype.h>
#include <omp.h>

#define MAX_WORD_SIZE 100
#define NUM_OF_FILES 3

// Function Prototype
void z_array(char *str, int **pz);
bool stringPatternMatch(char *pat, char *txt);
bool isUnique(char *word, char **uniqueWordList, int uniqueCount);
int countUnique(char **wordList, char ***puniqueWordList, int inputSize);
bool ReadFromFile(char *pFilename, char ***pwordList, int inputSize);
bool WriteToFile(char *pFilename, char **uniqueWordList, int uniqueCount);

// Global Variables
char* inputFileNames[3] = {"MOBY_DICK.txt", "LITTLE_WOMEN_MOBY_DICK.txt", "SHAKESPEARE.txt"};
int inputFileSizes[3] = {215724,411191,965465};
char *outputFileNames[3] = {"output_M.txt", "output_L.txt", "output_S.txt"};
char **puniqueWordList[1] = {0};
char **pwordList[1] = {0};
int uniqueCounts[3] = {0, 0, 0};

int main()
{
    //variables to time the program
    struct timespec start, end, startComp, endComp;
	double time_taken;

    printf("Main program started\n");

    for (int i = 0; i < NUM_OF_FILES; i++){
        // Get current clock time to measure overall time
	    clock_gettime(CLOCK_MONOTONIC, &start);

        // Reading from text files and storing into the word lists
        printf("Reading from text file: %s\n", inputFileNames[i]);
        ReadFromFile(inputFileNames[i], &pwordList[0], inputFileSizes[i]);
        printf("Reading complete\n");

        // Get current clock time to measure computational time only
        clock_gettime(CLOCK_MONOTONIC, &startComp);

        //run pattern match algorithm (Z-algorithm) to find and count unique words
        printf("Counting unique words in file %s\n", inputFileNames[i]);
        uniqueCounts[i] = countUnique(pwordList[0], &puniqueWordList[0], inputFileSizes[i]);
        puniqueWordList[0] = (char **)realloc(puniqueWordList[0], sizeof(char*) * uniqueCounts[i]);

        //Get the clock current time again
        // Subtract end from start to get the CPU time used for computation.
        clock_gettime(CLOCK_MONOTONIC, &endComp);
        time_taken = (endComp.tv_sec - startComp.tv_sec) * 1e9;
        time_taken = (time_taken + (endComp.tv_nsec - startComp.tv_nsec)) * 1e-9;
        printf("Unique String Counting complete - Computational time only(s): %lf\n", time_taken);

        printf("Total unique words: %d\n", uniqueCounts[i]);

        printf("Writing results to file %s\n", outputFileNames[i]);
        WriteToFile(outputFileNames[i], puniqueWordList[0], uniqueCounts[i]);

        // Get the clock current time again
        // // Subtract end from start to get the overall time used.
        clock_gettime(CLOCK_MONOTONIC, &end);
        time_taken = (end.tv_sec - start.tv_sec) * 1e9;
        time_taken = (time_taken + (end.tv_nsec - start.tv_nsec)) * 1e-9;
        printf("Overall time (Including read, match and write)(s): %lf\n", time_taken);

        //Clean up
        printf("Cleaning up\n");
        free(puniqueWordList[0]);
        free(pwordList[0]);

        printf("Main program ended\n");

    }

    return 0;
}

void z_array(char *str, int **pz)
/*
This is the main implementation of the Z-algorithm.
Input:
    str: The string to be processed.
    pz: A pointer to the z array.
Result:
    The z array is stored in pz[0].
*/
{
    int len = strlen(str);
    int *z = malloc(sizeof(int) * len);

    //Initialise z array
    for(int i = 0; i<len; i++)
    {
        z[i] = 0;
    }
    z[0] = len;

    //Z-algorithm
    int l = 0, r = 0;
    for (int i = 1; i < len; i++)
    {
        // Case 1
        if (i > r)
        {
            l = r = i;
            while (r < len && str[r - l] == str[r])
                r++;
            z[i] = r - l;
            r--;
        }
        // Case 2
        else
        {
            int k = i - l;
            // Case 2a
            if (z[k] < r - i + 1)
                z[i] = z[k];
            // Case 2b
            else
            {
                l = i;
                while (r < len && str[r - l] == str[r])
                    r++;
                z[i] = r - l;
                r--;
            }
        }
    }

    //Save results
    *pz = z;
    
    
}

bool stringPatternMatch(char *pat, char *txt)
/*
Helper function that uses the Z-algorithm to check for exact string matches.
Input:
    pat: The pattern to be matched.
    txt: The text to be searched.
Output:
    Returns true if there is an exact match, false otherwise.
*/
{
    //Check if the strings are valid
    if(pat == NULL || txt == NULL)
        return false;

    //Concatenate strings in the form pat$txt for Z-algorithm
    char *str = (char *)malloc(sizeof(char) * MAX_WORD_SIZE);
    strcpy(str, pat);
    strcat(str, "$");
    strcat(str, txt);

    //Run Z-algorithm
    int **pz = malloc(sizeof(int*));
    z_array(str, pz);

    //Check if exact match
    int index = strlen(pat)+1;
    if (pz[0][index] == strlen(pat)){   
        free(pz[0]);
        free(pz);
        free(str);    
        return true;
    }
    
    //Clean up
    free(pz[0]);
    free(pz);
    free(str);

    return false;
}

bool isUnique(char *word, char **uniqueWordList, int uniqueCount)
/*
Helper function that checks the existence of a word in the unique word list to determine its uniqueness.
Input:
    word: The word to be checked.
    uniqueWordList: The list of unique words.
    uniqueCount: The number of unique words in the current list.
Output:
    Returns true if the word is unique (not in the list), false otherwise.
*/
{    
    for(int i=0; i<uniqueCount; i++)
    {
        if(stringPatternMatch(word, uniqueWordList[i])){
            return false;
        }
    }
    return true;
}

int countUnique(char **wordList, char ***puniqueWordList, int inputSize)
/*
This is the main function that counts the number of unique words in the word list.
Input:
    wordList: The list of words to be processed.
    puniqueWordList: A pointer to the list of unique words.
    inputSize: The number of words in the word list.
Output:
    Returns the number of unique words in the word list.
Result:
    The list of unique words is stored in puniqueWordList[0].
*/
{
    int uniqueCount = 0;
    char** uniqueWordList = malloc(sizeof(char*) * inputSize);
    
    #pragma omp parallel for shared(wordList, uniqueWordList) reduction(+:uniqueCount)
    for(int i=0; i<inputSize; i++)
    {
        
        if(isUnique(wordList[i], uniqueWordList, uniqueCount))
        {
            uniqueWordList[uniqueCount] = strdup(wordList[i]);
            uniqueCount++;
        }
    }

    uniqueWordList = (char**)realloc(uniqueWordList, sizeof(char*) * uniqueCount);
    *puniqueWordList = uniqueWordList;
    
    return uniqueCount;
}

bool ReadFromFile(char *pFilename, char ***pwordList, int inputSize)
/*
The function that reads from the text file and stores the words into the word list.
Input:
    pFilename: The name of the file to be read.
    pwordList: A pointer to the list of words.
    inputSize: The number of words in the file.
Output:
    Returns true if the file is found and read from, false otherwise.
Result:
    The list of words is stored in pwordList[0].
*/
{
    FILE *pFile = fopen(pFilename, "r");
    if(pFile == NULL){
        printf("File not found\n");
        return false;
    }
    
    char buffer[MAX_WORD_SIZE];
    char **wordList = malloc(sizeof(char*) * inputSize);

    for(int i=0; i<inputSize; i++)
    {
        fscanf(pFile, "%s", buffer);
        wordList[i] = strdup(buffer);
        for (int j = 0; wordList[i][j]; j++) {
		    wordList[i][j] = tolower(wordList[i][j]);
		}
    }
    fclose(pFile);

    *pwordList = wordList; 
    
    return true;
}

bool WriteToFile(char *pFilename, char **uniqueWordList, int uniqueCount)
/*
The function that writes the unique words to a text file.
Input:
    pFilename: The name of the file to be written to.
    uniqueWordList: The list of unique words.
    uniqueCount: The number of unique words in the list.
Output:
    Returns true if the file is found and written to, false otherwise.
*/
{
    FILE *fp = fopen(pFilename, "w");
    if(fp == NULL){
        printf("File not found\n");
        return false;
    }

    fprintf(fp, "%d\n", uniqueCount);

    for(int i=0; i<uniqueCount; i++)
    {
        fprintf(fp, "%s\n", uniqueWordList[i]);
    }
        
    fclose(fp);
    return true;
}