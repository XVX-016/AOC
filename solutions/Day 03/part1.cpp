#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

int getMaxJoltage(const std::string& bank) {
    int maxJoltage = 0;
    int n = bank.length();
    
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int current = (bank[i] - '0') * 10 + (bank[j] - '0');
            if (current > maxJoltage) {
                maxJoltage = current;
            }
        }
    }
    
    return maxJoltage;
}

int main() {
    std::ifstream inputFile("C:\\Computing\\AOC\\solutions\\Day 03\\input.txt");
    if (!inputFile.is_open()) {
        std::cerr << "Error opening input file!" << std::endl;
        return 1;
    }
    
    std::string line;
    int totalJoltage = 0;
    int lineCount = 0;
    
    while (std::getline(inputFile, line)) {
        if (!line.empty() && line[line.length() - 1] == '\r') {
            line.erase(line.length() - 1);
        }
        if (line.empty()) continue;
        
        int maxJoltage = getMaxJoltage(line);
        totalJoltage += maxJoltage;
        lineCount++;
    }
    
    inputFile.close();
    
    std::cout << "Total output joltage: " << totalJoltage << std::endl;
    
    return 0;
}