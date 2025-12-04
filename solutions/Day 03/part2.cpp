#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

std::string getMax12DigitNumber(const std::string& bank) {
    int n = bank.length();
    int k = 12;  
    std::string result;
    int start = 0;
    
    for (int i = 0; i < k; i++) {
        int maxPos = start;
        char maxDigit = bank[start];
        
        for (int j = start; j <= n - (k - i); j++) {
            if (bank[j] > maxDigit) {
                maxDigit = bank[j];
                maxPos = j;
            }
        }
        
        result.push_back(maxDigit);
        start = maxPos + 1;
    }
    
    return result;
}

long long calculateTotalJoltage(const std::string& filename) {
    std::ifstream inputFile(filename);
    if (!inputFile.is_open()) {
        std::cerr << "Error opening input file!" << std::endl;
        return -1;
    }
    
    std::string line;
    long long totalJoltage = 0;
    int lineCount = 0;
    
    while (std::getline(inputFile, line)) {
        if (!line.empty() && line[line.length() - 1] == '\r') {
            line.erase(line.length() - 1);
        }
        
        // Skip empty lines
        if (line.empty()) continue;
        std::string max12Digit = getMax12DigitNumber(line);
        long long joltage = 0;
        for (char c : max12Digit) {
            joltage = joltage * 10 + (c - '0');
        }
        
        totalJoltage += joltage;
        lineCount++;
    }
    
    inputFile.close();
    
    std::cout << "Processed " << lineCount << " banks" << std::endl;
    return totalJoltage;
}

int main() {
    std::string filename = "C:\\Computing\\AOC\\solutions\\Day 03\\input.txt";
    long long totalJoltage = calculateTotalJoltage(filename);
    
    if (totalJoltage >= 0) {
        std::cout << "Total output joltage: " << totalJoltage << std::endl;
    }
    
    return 0;
}