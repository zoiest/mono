#include "parity.h"
#include <cassert>
#include <iostream>

int main() {
    assert(parity::ComputeParity(0b1011) == 1);
    assert(parity::ComputeParity(0b10001) == 0);
    assert(parity::ComputeParity(0) == 0);
    std::cout << "All C++ parity tests passed!" << std::endl;
    return 0;
}
