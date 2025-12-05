#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_RANGES 2000
#define MAX_IDS 2000
#define MAX_LINE_LENGTH 50

typedef struct {
    long long start;
    long long end;
} Range;

int main() {
    FILE *file = fopen("input.txt", "r");
    if (!file) {
        printf("Error opening file.\n");
        return 1;
    }

    Range ranges[MAX_RANGES];
    int range_count = 0;
    long long ids[MAX_IDS];
    int id_count = 0;
    
    char line[MAX_LINE_LENGTH];
    int parsing_ranges = 1; 
    
    while (fgets(line, sizeof(line), file)) {
        line[strcspn(line, "\r\n")] = '\0';
        if (strlen(line) == 0) {
            parsing_ranges = 0;
            continue;
        }
        
        if (parsing_ranges) {
            long long start, end;
            if (sscanf(line, "%lld-%lld", &start, &end) == 2) {
                ranges[range_count].start = start;
                ranges[range_count].end = end;
                range_count++;
            } else {
                printf("Failed to parse range: %s\n", line);
            }
        } else {
            long long id;
            if (sscanf(line, "%lld", &id) == 1) {
                ids[id_count] = id;
                id_count++;
            } else {
                printf("Failed to parse ID: %s\n", line);
            }
        }
    }
    
    fclose(file);
    
    printf("Parsed %d ranges and %d IDs\n", range_count, id_count);
    long long fresh_count = 0;
    for (int i = 0; i < id_count; i++) {
        long long id = ids[i];
        int fresh = 0;
        
        for (int j = 0; j < range_count; j++) {
            if (id >= ranges[j].start && id <= ranges[j].end) {
                fresh = 1;
                break;
            }
        }
        
        if (fresh) {
            fresh_count++;
        }
    }
    
    printf("Fresh ingredient IDs: %lld\n", fresh_count);
    return 0;
}