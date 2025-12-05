#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_RANGES 2000

typedef struct {
    long long start;
    long long end;
} Range;

int compare_ranges(const void *a, const void *b) {
    Range *r1 = (Range *)a;
    Range *r2 = (Range *)b;
    
    if (r1->start < r2->start) return -1;
    if (r1->start > r2->start) return 1;
    if (r1->end < r2->end) return -1;
    if (r1->end > r2->end) return 1;
    return 0;
}

int main() {
    FILE *file = fopen("input.txt", "r");
    if (!file) {
        printf("Error opening file\n");
        return 1;
    }
    
    Range ranges[MAX_RANGES];
    int count = 0;
    char line[100];
    int in_first_section = 1;
    while (fgets(line, sizeof(line), file)) {
        line[strcspn(line, "\r\n")] = 0;
        if (strlen(line) == 0) {
            break;
        }
        long long start, end;
        if (sscanf(line, "%lld-%lld", &start, &end) == 2) {
            ranges[count].start = start;
            ranges[count].end = end;
            count++;
        }
    }
    
    fclose(file);
    
    printf("Read %d ranges\n", count);
    qsort(ranges, count, sizeof(Range), compare_ranges);
    Range merged[MAX_RANGES];
    int merged_count = 0;
    
    if (count > 0) {
        merged[0] = ranges[0];
        merged_count = 1;
        
        for (int i = 1; i < count; i++) {
            Range *last = &merged[merged_count - 1];
            if (ranges[i].start <= last->end + 1) {
                if (ranges[i].end > last->end) {
                    last->end = ranges[i].end;
                }
            } else {
                merged[merged_count] = ranges[i];
                merged_count++;
            }
        }
    }
    long long total = 0;
    for (int i = 0; i < merged_count; i++) {
        total += (merged[i].end - merged[i].start + 1);
    }
    
    printf("After merging: %d ranges\n", merged_count);
    printf("Total fresh ingredient IDs: %lld\n", total);
    
    return 0;
}