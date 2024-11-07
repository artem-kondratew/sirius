#ifndef TEMPLATE_HPP
#define TEMPLATE_HPP


#include <cmath>
#include <iostream>
#include <map>
#include <stack>
#include <string>
#include <vector>


namespace calculator {

inline std::stack<double> stack;
inline std::stack<double> user_stack;


struct Operator {
    virtual ~Operator() {}
    virtual void calc() = 0;
};


template <typename S>
struct TOperator : Operator {
    virtual ~TOperator() {}
    static S* instance();
};


struct Add : TOperator<Add> {
    void calc() override;
};


struct Sub : TOperator<Sub> {
    void calc() override;
};


struct Mul : TOperator<Mul> {
    void calc() override;
};


struct Div : TOperator<Div> {
    void calc() override;
};


struct Exp : TOperator<Exp> {
    void calc() override;
};


struct Ln : TOperator<Ln> {
    void calc() override;
};


struct Lg : TOperator<Lg> {
    void calc() override;
};


struct Log : TOperator<Log> {
    void calc() override;
};


struct Sin : TOperator<Sin> {
    void calc() override;
};


struct Cos : TOperator<Cos> {
    void calc() override;
};


struct Sqrt : TOperator<Sqrt> {
    void calc() override;
};


struct Pow : TOperator<Pow> {
    void calc() override;
};


struct Put : TOperator<Put> {
    void calc() override;
};


struct Get : TOperator<Get> {
    void calc() override;
};


struct OperationTable final {
    static OperationTable& instance();
    Operator& getOperator(std::string word);
    void addOperator(std::string word, Operator* op);

private:
    OperationTable();

    std::map<std::string, Operator*> op_table;
};


struct Calculator final {
    static Calculator& instance();
    bool is_double(std::string word);

    double calc(std::vector<std::string> expr);

private:
    Calculator() {}
};

}  // namespace calculator


#endif  // TEMPLATE_HPP
