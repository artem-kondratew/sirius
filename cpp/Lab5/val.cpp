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
int64_t rec = A_VALUE * rec<N - 1> + B_VALUE * rec<N - 2>;


template <>
int64_t rec<1> = Y1_VALUE;


template <>
int64_t rec<2> = Y2_VALUE;


int main() {
    std::cout << "res = " << rec<N_VALUE> << std::endl;
    return 0;
}
