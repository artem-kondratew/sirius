#include <iostream>


#ifndef A_VALUE
    constexpr int64_t A_VALUE = 1;
#endif
#ifndef B_VALUE
    constexpr int64_t B_VALUE = 1;
#endif
#ifndef Y1_VALUE
    constexpr int64_t Y1_VALUE = 1;
#endif
#ifndef Y2_VALUE
    constexpr int64_t Y2_VALUE = 1;
#endif
#ifndef N_VALUE
    constexpr size_t N_VALUE = 5;
#endif


template <size_t N>
typename std::enable_if_t<(N == 1), int64_t> rec() {
    return Y1_VALUE;
}


template <size_t N>
typename std::enable_if_t<(N == 2), int64_t> rec() {
    return Y2_VALUE;
}


template <size_t N>
typename std::enable_if_t<(N > 2), int64_t> rec() {
    return A_VALUE * rec<N - 1>() + B_VALUE * rec<N - 2>();
}


int main() {
    std::cout << "res = " << rec<N_VALUE>() << std::endl;
    return 0;
}
