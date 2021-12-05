#include <chrono>
#include <thread>

#include <libevdev/libevdev.h>
#include <libevdev/libevdev-uinput.h>

#include "input.cpp"

template <typename T>
class relay {
    libevdev *dev;
    libevdev_uinput *uidev;
    input_data data;
    std::unique_ptr<T> in;  // might want to have more of them later on

public:
    relay(): in(std::make_unique<T>()) {
        dev = libevdev_new();
        libevdev_set_name(dev, "test device");
        libevdev_enable_event_type(dev, EV_REL);
        libevdev_enable_event_code(dev, EV_REL, REL_X, NULL);
        libevdev_enable_event_code(dev, EV_REL, REL_Y, NULL);
        libevdev_enable_event_type(dev, EV_KEY);
        libevdev_enable_event_code(dev, EV_KEY, BTN_LEFT, NULL);
        libevdev_enable_event_code(dev, EV_KEY, BTN_MIDDLE, NULL);
        libevdev_enable_event_code(dev, EV_KEY, BTN_RIGHT, NULL);
    }
    int load() {
        in->init();
        return libevdev_uinput_create_from_device(dev,
                                         LIBEVDEV_UINPUT_OPEN_MANAGED,
                                         &uidev);
    }
    void execute() {
        if (in->read(data) == NO_PARSE) {
            return;
        }
        libevdev_uinput_write_event(uidev, EV_REL, REL_X, data.move_x);
        libevdev_uinput_write_event(uidev, EV_REL, REL_Y, data.move_y);
        libevdev_uinput_write_event(uidev, EV_SYN, SYN_REPORT, 0);
        data.clean();
        std::this_thread::sleep_for(std::chrono::milliseconds(40));
    }
    ~relay() {
        libevdev_uinput_destroy(uidev);
        libevdev_free(dev);
        //close fd
    }
};