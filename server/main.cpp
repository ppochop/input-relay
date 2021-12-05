#include "relay.cpp"

int main() {
    relay<keyboard_input> rl;
    rl.load();
    for (int i=0; i<500; ++i) {
        rl.execute();
    }
}