#include <iostream>
#include <string>
#include <vector>


std::vector<std::string> in = {"1", "|0", "0"};
std::vector<std::string> out = {"0|", "0||", ""};


std::string MarkovChain(std::string s) {
    bool proc = true;
    
    while (proc) {
        proc = false;
        for (auto i = 0; i < in.size(); i++) {
            auto found = s.find(in[i]);
            if (found == std::string::npos) {
                continue;
            }
            s.replace(found, in[i].size(), out[i]);
            proc = true;
            break;
        }
    }

    return s;
}


int main(int argc, char** argv) {
    if (argc != 2) {
        std::cout << "wrong input" << std::endl;
        exit(0);
    }
    
    std::string s = argv[1];

    s = MarkovChain(s);

    std::cout << s << std::endl;

    return 0;
}
