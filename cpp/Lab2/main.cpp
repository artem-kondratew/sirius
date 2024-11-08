#include <iostream>

#include "parser.hpp"
#include "poly.hpp"


int main(int argc, char** argv) {
    if (argc != 2) {
        std::cout << "wrong usage" << std::endl;
        exit(0);
    }

    auto file = openFile(argv[1]);

    if (!file.is_open()) {
        std::cout << "file is not opened" << std::endl;
        exit(0);
    }

    auto data = readData(file);

    std::vector<Poly> P;

    for (auto i = 0; i < data.size(); i++) {
        P.push_back(Poly{data[i]});
    }

    Poly result = ((P[0] + P[1]) * P[2] - P[3]) % P[4];
    result.print();

    return 0;
}
