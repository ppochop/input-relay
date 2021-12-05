CC=g++
CFLAGS=-I/usr/include/libevdev-1.0 -std=c++17

LIBS=-levdev

build: main.cpp input.cpp relay.cpp
	${CC} -o bin/main main.cpp $(LIBS) $(CFLAGS)