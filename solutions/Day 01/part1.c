#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *file = fopen("input.txt", "r");
    if (!file) {
        perror("Failed to open input.txt");
        return 1;
    }

    char direction;
    int steps;
    int dial = 50;       
    int count_zero = 0;

    
    while (fscanf(file, " %c%d", &direction, &steps) == 2) {
        if (direction == 'L' || direction == 'l') {
            dial = (dial - steps) % 100;
            if (dial < 0) dial += 100;
        } else if (direction == 'R' || direction == 'r') {
            dial = (dial + steps) % 100;
        }

        if (dial == 0) {
            count_zero++;
        }
    }

    fclose(file);

    printf("Password: %d\n", count_zero);

    return 0;
}
