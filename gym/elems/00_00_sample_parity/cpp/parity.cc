#include "parity.h"

namespace parity {
short ComputeParity(unsigned long long x) {
    short result = 0;
    while (x) {
        result ^= (x & 1);
        x >>= 1;
    }
    return result;
}
}  // namespace parity
