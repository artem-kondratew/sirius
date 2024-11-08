#ifndef POLY_HPP
#define POLY_HPP


#include <cfloat>
#include <iostream>
#include <vector>


class Poly {
private:
    std::vector<double> v_;

public:
    Poly() = default;
    Poly(const std::vector<double>& v) : v_{v} {}
    Poly(const double& c) : Poly(std::vector<double>{c}) {}

    Poly& operator=(const double& c) { *this = Poly{c}; return *this; }

    Poly operator-() const;

    Poly& operator+=(const Poly& other);
    Poly& operator-=(const Poly& other);
    Poly& operator*=(const Poly& other);
    Poly& operator/=(const Poly& other);
    Poly& operator%=(const Poly& other);

    void resize(size_t size, double value=0.0) { v_.resize(size, value); }

private:
    static std::pair<Poly, Poly> divide(const Poly& dividend, const Poly& divisor);

public:
    Poly operator*(const double& k) const;

    Poly operator>>(const size_t k) const;
    Poly operator<<(const size_t k) const;

    void print() const;
    std::vector<double>& data() { return v_; }
    const std::vector<double>& data() const { return v_; }

private:
    void trim();

public:
    size_t deg() const { return v_.size()-1; }
    double head() const { return v_[deg()]; }

    static Poly x(size_t degree);
};


Poly operator+(const Poly& p1, const Poly& p2);
Poly operator-(const Poly& p1, const Poly& p2);
Poly operator*(const Poly& p1, const Poly& p2);
Poly operator/(const Poly& p1, const Poly& p2);
Poly operator%(const Poly& p1, const Poly& p2);

bool operator==(const Poly& p1, const Poly& p2);


Poly Poly::operator-() const {
    Poly poly = *this;

    for (auto i = 0; i < poly.v_.size(); i++) {
        poly.v_[i] *= -1;
    }

    return poly;
}


Poly& Poly::operator+=(const Poly& other) {
    size_t common_size, max_size;

    if (this->v_.size() > other.v_.size()) {
        common_size = other.v_.size();
        max_size = this->v_.size();
    }
    else {
        common_size = this->v_.size();
        max_size = other.v_.size();
    }

    for (auto i = 0; i < max_size; i++) {
        if (i < common_size) {
            this->v_[i] += other.v_[i];
        }
        else if (other.v_.size() > this->v_.size()) {
            this->v_.push_back(other.v_[i]);
        }
    }

    trim();

    return *this;
}


Poly& Poly::operator-=(const Poly& other) {
    *this += -other;
    trim();
    return *this;
}


Poly& Poly::operator*=(const Poly& other) {
    std::vector<double> v;
    v.resize(this->v_.size() + other.v_.size() - 1, 0);
    
    for (auto i = 0; i < this->v_.size(); i++) {
        for (auto j = 0; j < other.v_.size(); j++) {
            v[i+j] += this->v_[i] * other.v_[j];
        }
    }

    this->v_ = v;

    trim();

    return *this;
}


Poly& Poly::operator/=(const Poly& other) {
    *this = divide(*this, other).first;
    return *this;
}


Poly& Poly::operator%=(const Poly& other) {
    *this = divide(*this, other).second;
    return *this;
}


std::pair<Poly, Poly> Poly::divide(const Poly& poly, const Poly& divisor) {
    Poly dividend = poly;

    if (dividend.deg() < divisor.deg()) {
        return std::pair<Poly, Poly>{Poly{std::vector<double>{0}}, dividend};
    }

    Poly quotient;
    quotient.resize(dividend.deg() - divisor.deg() + 1);

    while (dividend.deg() >= divisor.deg()) {
        double k = dividend.head() / divisor.head();
        quotient.v_[dividend.deg() - divisor.deg()] = k;
        auto shifted = (divisor * k) >> (dividend.deg() - divisor.deg());
        dividend -= shifted;
    }

    return std::pair<Poly, Poly>{quotient, dividend};
}


Poly operator+(const Poly& p1, const Poly& p2) {
    Poly poly = p1;
    return poly += p2;
}


Poly operator-(const Poly& p1, const Poly& p2) {
    Poly poly = p1;
    return poly -= p2;
}


Poly operator*(const Poly& p1, const Poly& p2) {
    Poly poly = p1;
    return poly *= p2;
}


Poly operator/(const Poly& p1, const Poly& p2) {
    Poly poly = p1;
    return poly /= p2;
}


Poly operator%(const Poly& p1, const Poly& p2) {
    Poly poly = p1;
    return poly %= p2;
}


Poly Poly::operator*(const double& k) const {
    Poly poly = *this;

    for (auto i = 0; i < v_.size(); i++) {
        poly.v_[i] *= k;
    }

    return poly;
}


bool operator==(const Poly& p1, const Poly& p2) {
    return p1.data() == p2.data();
}


Poly Poly::operator>>(const size_t k) const {
    Poly poly;
    poly.resize(this->v_.size() + k);

    for (auto i = k; i < poly.v_.size(); i++) {
        poly.v_[i] = this->v_[i-k];
    }

    return poly;
}


Poly Poly::operator<<(const size_t k) const {
    auto n = this->v_.size() - k;
    Poly poly;
    poly.resize(n > 0 ? n : 0);

    for (auto i = 0; i < poly.v_.size(); i++) {
        poly.v_[i] = this->v_[i+k];
    }

    return poly;
}


void Poly::print() const {
    std::cout << "[";
    for (auto i = 0; i < v_.size() - 1; i++) {
        std::cout << v_[i] << ", ";
    }
    std::cout << v_.back() << "]" << std::endl;
}


void Poly::trim() {
    while (!v_.empty() && std::abs(v_.back()) < FLT_EPSILON) {
        v_.pop_back();
    }
}


Poly Poly::x(size_t degree) {
    Poly poly;
    poly.resize(degree + 1);
    poly.v_.back() = 1.0;
    return poly;
}


#endif  // POLY_HPP
