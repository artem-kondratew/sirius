#ifndef PARSER_HPP
#define PARSER_HPP


#include <vector>
#include <string>
#include <fstream>
#include <sstream>


std::ifstream openFile(std::string filename) {
   return std::ifstream(filename);
}


void deleteSpaces(std::vector<std::string>& data) {
    std::vector<char> allowed_symbols = {',', '.', '+', '-'};

    for (auto i = 0; i < data.size(); i++) {
        std::string& str = data[i];
        std::string new_str;
        
        for (auto s : str) {
            if (isdigit(s)) {
                new_str.push_back(s);
                continue;
            }
            for (auto symbol : allowed_symbols) {
                if (symbol == s) {
                    new_str.push_back(s);
                    break;
                }
            }
        }

        str = new_str;
    }
}


std::vector<std::vector<double>> readData(std::ifstream& file) {
    std::vector<std::string> strings;
    std::vector<std::vector<double>> data;
    
    std::string s;
    while(std::getline(file, s)) {
        strings.push_back(s);
    }
        
    deleteSpaces(strings);

    data.resize(strings.size());
    for (auto  i = 0; i < strings.size(); i++) {
        auto iss = std::istringstream{strings[i]};
        std::string s;
        while (std::getline(iss, s, ',')) {
            data[i].push_back(std::stod(s));
        }
    }

    return data;
}


#endif  // PARSER_HPP
