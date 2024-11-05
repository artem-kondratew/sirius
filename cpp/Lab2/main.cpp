#include <iostream>
#include <vector>
#include <fstream>


#define DEBUG false


std::vector<std::string> readData(std::ifstream& file) {
    std::vector<std::string> data;
    std::string s;
    while(std::getline(file, s)) {
        data.push_back(s);
    }
    return data;

    
}


void addSpaces(std::vector<std::string>& data, size_t max_length) {
    for (auto& s : data) {
        while (s.length() < max_length) {
            s.push_back(' ');
        }
    }
}


std::vector<std::string> transpose(std::vector<std::string>& data) {
    size_t max_length = 0;
    for (const auto& s : data) {
        if (s.length() > max_length) {
            max_length = s.length();
        }
    }

    addSpaces(data, max_length);

    std::vector<std::string> transposed;
    transposed.resize(max_length, "");

    for (auto i = 0; i < data.size(); i++) {
        for (auto j = 0; j < max_length; j++) {
            transposed[j].push_back(data[i][j]);
        }
    }

    return transposed;
}


void doubleTransposeTest(std::vector<std::string> data) {
    
    auto new_data1 = transpose(data);
    auto new_data2 = transpose(new_data1);

    for (auto s : data) {
        std::cout << s << std::endl;
    }

    std::cout << std::endl;

    for (auto s : new_data1) {
        std::cout << s << std::endl;
    }

    std::cout << std::endl;

    for (auto s : new_data2) {
        std::cout << s << std::endl;
    }
}


int main(int argc, char** argv) {
    if (argc != 2) {
        std::cout << "wrong usage" << std::endl;
        exit(0);
    }

    auto file = std::ifstream(argv[1]);

    if (!file.is_open()) {
        std::cout << "file is not opened" << std::endl;
        exit(0);
    }

    auto data = readData(file);

#if DEBUG
    doubleTransposeTest(data);
#else
    for (auto s : transpose(data)) {
        std::cout << s << std::endl;
    }
#endif

    return 0;
}
