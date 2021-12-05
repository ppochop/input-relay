#include <fcntl.h>
#include <unistd.h>
#include <cstdlib>
#include <libevdev/libevdev.h>

#define KEY_TO_MOUSE_SPEED 5
#define NO_PARSE 69
#define K_UP 0
#define K_DOWN 1
#define K_RIGHT 2
#define K_LEFT 3


struct input_data {
    int move_x;
    int move_y;
    bool btn_left;
    bool btn_right;
    void clean() {
        move_x = 0;
        move_y = 0;
    }
};

/**
 * @brief 
 * Abstract class as a base for different methods of input
 * e.g. TCP, UDP, Bluetooth, random generated, keyboard
 */
class input {
public:
    virtual void init() = 0;
    virtual int read(input_data &) = 0;
    virtual ~input() {};
};

class random_input: input {
public:
    virtual void init() {
        std::srand(420);
    }
    virtual int read(input_data &in) {
        in.move_x = std::rand() % 64 - 32;
        in.move_y = std::rand() % 64 - 32;
        in.btn_left = 0;
        in.btn_right = 0;
    }
    ~random_input() {}
};

class keyboard_input: input {
    libevdev *dev;
    int fd;
    input_event ie; // initialize
    std::array<bool, 4> pressed;
public:
    keyboard_input(): ie{}, pressed{false, false, false, false} {
        fd = open("/dev/input/event2", O_RDONLY); // figure out which event file to open
        if (fd < 0) {
            //throw exc
        }
        int err = libevdev_new_from_fd(fd, &dev);
        if (err) {
            // throw exc
        }
    }

    virtual void init() { }

    virtual int read(input_data &in) {
        int err = libevdev_next_event(dev, LIBEVDEV_READ_FLAG_BLOCKING, &ie);
        if (err == 0 && ie.type == EV_KEY) {
            switch (ie.code) {
                case KEY_UP: pressed[K_UP] = ie.value > 0; break;
                case KEY_DOWN: pressed[K_DOWN] = ie.value > 0; break;
                case KEY_RIGHT: pressed[K_RIGHT] = ie.value > 0; break;
                case KEY_LEFT: pressed[K_LEFT] = ie.value > 0; break;
                default: break; //return or continue?
            }

            if (pressed[K_UP]) in.move_y = -KEY_TO_MOUSE_SPEED;
            if (pressed[K_DOWN]) in.move_y = KEY_TO_MOUSE_SPEED;
            if (pressed[K_RIGHT]) in.move_x = KEY_TO_MOUSE_SPEED;
            if (pressed[K_LEFT]) in.move_x = -KEY_TO_MOUSE_SPEED; 

        } else {
            return NO_PARSE;
        }
    }

    ~keyboard_input() {
        libevdev_free(dev);
        close(fd);
    }
};