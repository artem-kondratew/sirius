#include "calculator.hpp"


namespace calculator {

template <typename S>
S* TOperator<S>::instance() {
    static S op;
    return &op;
}


void Add::calc() {
    double v1 = stack.top();
    stack.pop();
    double v2 = stack.top();
    stack.pop();
    stack.push(v2 + v1);
}


void Sub::calc() {
    double v1 = stack.top();
    stack.pop();
    double v2 = stack.top();
    stack.pop();
    stack.push(v2 - v1);
}


void Mul::calc() {
    double v1 = stack.top();
    stack.pop();
    double v2 = stack.top();
    stack.pop();
    stack.push(v2 * v1);
}


void Div::calc() {
    double v1 = stack.top();
    stack.pop();
    double v2 = stack.top();
    stack.pop();
    stack.push(v2 / v1);
}


void Exp::calc() {
    double v = stack.top();
    stack.pop();
    stack.push(std::exp(v));
}


void Ln::calc() {
    double v = stack.top();
    stack.pop();
    stack.push(std::log(v));
}


void Lg::calc() {
    double v = stack.top();
    stack.pop();
    stack.push(std::log10(v));
}


void Log::calc() {
    double v1 = stack.top();
    stack.pop();
    double v2 = stack.top();
    stack.pop();
    stack.push(std::log(v1) / std::log(v2));
}


void Sin::calc() {
    double v = stack.top();
    stack.pop();
    stack.push(std::sin(v));
}


void Cos::calc() {
    double v = stack.top();
    stack.pop();
    stack.push(std::cos(v));
}


void Sqrt::calc() {
    double v = stack.top();
    stack.pop();
    stack.push(std::sqrt(v));
}


void Pow::calc() {
    double v1 = stack.top();
    stack.pop();
    double v2 = stack.top();
    stack.pop();
    stack.push(std::pow(v2, v1));
}


void Put::calc() {
    double v = stack.top();
    user_stack.push(v);
}


void Get::calc() {
    double v = user_stack.top();
    user_stack.pop();
    stack.push(v);
}


OperationTable::OperationTable() {
    op_table["+"] = Add::instance();
    op_table["-"] = Sub::instance();
    op_table["*"] = Mul::instance();
    op_table["/"] = Div::instance();
    op_table["exp"] = Exp::instance();
    op_table["ln"] = Ln::instance();
    op_table["lg"] = Lg::instance();
    op_table["log"] = Log::instance();
    op_table["sin"] = Sin::instance();
    op_table["cos"] = Cos::instance();
    op_table["sqrt"] = Sqrt::instance();
    op_table["pow"] = Pow::instance();
    op_table["put"] = Put::instance();
    op_table["get"] = Get::instance();
}


OperationTable& OperationTable::instance() {
    static OperationTable ot;
    return ot;
}


Operator& OperationTable::getOperator(std::string word) {
    return *op_table[word];
}


void OperationTable::addOperator(std::string word, Operator* op) {
    op_table[word] = op;
}


Calculator& Calculator::instance() {
    static Calculator c;
    return c;
}


bool Calculator::is_double(std::string word) {
    if (!std::isdigit(word[0])) {
        if (word[0] != '+' && word[0] != '-' && word[0] != '.') {
            return false;
        }
        else if (word.size() == 1) {
            return false;
        }
    }

    for (auto i = 1; i < word.size(); i++) {
        if (!std::isdigit(word[i]) && word[i] != '.') {
            return false;
        }
    }

    return true;
}


double Calculator::calc(std::vector<std::string> expr) {
    static OperationTable& op_table = OperationTable::instance();

    for (const auto& word : expr) {
        if (is_double(word)) {
            stack.push(std::stod(word));
            continue;
        }
        op_table.getOperator(word).calc();
    }

    double res = stack.top();
    stack.pop();
    return res;
}

}  // namespace calculator
