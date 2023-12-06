#!/usr/bin/env gmake -f

MAKEFLAGS:=-B -j2

default:
	$(MAKE) -B -C "$$(dirname "$$_")" run

run:
	./mklnk.zsh
	# $(MAKE) prep
	$(MAKE) run.frontend run.backend

prep:
	./mklnk.zsh
	rm -fv backend/active.json
	rm -fv backend/blacklist.json
	rm -fv backend/clash.yaml
	rm -fv backend/storage.json
	$(MAKE) "httping.$$(uname -s)"

run.frontend:
	cd frontend; python -m http.server -b 127.0.0.1 6080 >/dev/null 2>&1

run.backend:
	if pgrep trojan; then false; else true; fi
	cd backend; ./main.py

httping.Darwin:
	cd backend; gcc \
	  -std=gnu2x -Wall -O3 -dynamiclib -fpic -o httping.dylib \
	  $(shell curl-config --cflags) httping.c $(shell curl-config --libs)

httping.Linux:
	cd backend; gcc \
	  -std=gnu2x -Wall -O3 -shared -fpic -o httping.so \
	  $(shell curl-config --cflags) httping.c $(shell curl-config --libs)

systemd:
	[ x"$$(uname -s)" = xLinux ] || false
	[ x"$$(whoami)" = xroot ] || false
	cp -fv jangaehwepi-backend.service jangaehwepi-frontend.service /etc/systemd/system/
	systemctl daemon-reload
	systemctl enable jangaehwepi-backend.service jangaehwepi-frontend.service
	systemctl status jangaehwepi-backend.service jangaehwepi-frontend.service

status:
	{ \
	  cd backend; \
	  file blacklist.json; cat $$_; echo; echo; \
	  file active.json; cat $$_; echo; echo; \
	  file storage.json; cat $$_ echo; echo; \
	} | less -SRM +%

# https://datatables.net/download/
download:
	cd frontend/external/; ./download.zsh

# ui:
# 	cd frontend; busybox httpd -f -p 0.0.0.0:6080 -h .
