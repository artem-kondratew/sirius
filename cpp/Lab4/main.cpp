#include <iostream>
#include <sstream>
#include <vector>

#include "template.hpp"


int main(int argc, char** argv) {
    if (argc != 2) {
        std::cout << "wrong input" << std::endl;
        exit(0);
    }

    auto calc = calculator::Calculator::instance();

    auto iss = std::istringstream{argv[1]};


    std::vector<std::string> expr;
    std::string str;

    while (std::getline(iss, str, ' ')) {
        expr.push_back(str);
    }

    double res = calc.calc(expr);

    std::cout << res << std::endl;

    return 0;
}
