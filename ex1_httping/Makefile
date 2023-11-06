$(info please run this Makefile on Linux)

MAKEFLAGS:=-j1

# force linux
default:
	[ x"$$(uname -s)" = xLinux ] || false
	gcc -std=gnu17 -Wall -O3 -o httping.out $(shell curl-config --cflags) httping.c $(shell curl-config --libs)
	./httping.out
