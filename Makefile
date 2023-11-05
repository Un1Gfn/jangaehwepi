ifeq ($(shell uname -s),Darwin)
  $(info loading homebrew compat $$PATH ...)
  include /usr/local/share/make/compat.mk
endif

MAKEFLAGS:=-j1

default:
	$(MAKE) httping

httping:
	[ x"$$(uname -s)" = xLinux ] || false
	gcc -std=gnu17 -Wall -O3 -o httping.out $(shell curl-config --cflags) httping.c $(shell curl-config --libs)
	./httping.out

rsync:
	find . -type f | entr ./rsync.zsh . rsync://820g3/hudrpl/jangaehwepi@820g3

clean:
	./rsync.zsh --delete . rsync://820g3/hudrpl/jangaehwepi@820g3
