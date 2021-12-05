extern "C" {
    #include <xdo.h>
}
#include <chrono>
#include <thread>

int main() {
    using namespace std::chrono_literals;
    xdo_t *Display = xdo_new(nullptr);
    while(true) {
        std::this_thread::sleep_for(30ms);
        xdo_move_mouse_relative(Display, 10, 10);
    }
}