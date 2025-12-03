#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *fp = fopen("input.txt", "r");
    if (!fp) {
        perror("Failed to open input file");
        return 1;
    }

    int current = 50; // starting dial
    int password = 0;

    char line[16];
    while (fgets(line, sizeof(line), fp)) {
        if (line[0] == '\n' || line[0] == '\0') continue;

        char dir = line[0];
        int steps = atoi(&line[1]);

        for (int i = 0; i < steps; i++) {
            if (dir == 'R') {
                current = (current + 1) % 100;
            } else if (dir == 'L') {
                current = (current - 1 + 100) % 100;
            } else {
                fprintf(stderr, "Invalid direction: %c\n", dir);
                return 1;
            }

            if (current == 0) password++;
        }
    }

    fclose(fp);
    printf("Part 2 Password: %d\n", password);
    return 0;
}
