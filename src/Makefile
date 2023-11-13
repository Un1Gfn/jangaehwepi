$(info please run this Makefile on Linux)

MAKEFLAGS:=-B -j2

default:
	./mklnk.zsh
	# $(MAKE) prep
	$(MAKE) httping
	$(MAKE) run.frontend run.backend

# -dynamiclib
# -shared
httping:
	[ x"$$(uname -s)" = xLinux ] || false
	cd backend; gcc \
	  -std=gnu17 -Wall -O3 -shared -fpic -o httping.so \
	  $(shell curl-config --cflags) httping.c $(shell curl-config --libs)

prep:
	./mklnk.zsh
	rm -fv backend/active.json
	rm -fv backend/blacklist.json
	rm -fv backend/clash.yaml
	rm -fv backend/storage.json

systemd:
	[ x"$$(uname -s)" = xLinux ] || false
	[ x"$$(whoami)" = xroot ] || false
	cp -fv jangaehwepi-backend.service jangaehwepi-frontend.service /etc/systemd/system/
	systemctl daemon-reload
	systemctl enable jangaehwepi-backend.service jangaehwepi-frontend.service
	systemctl status jangaehwepi-backend.service jangaehwepi-frontend.service

run.frontend:
	cd frontend; python -m http.server -b 0.0.0.0 6080 >/dev/null 2>&1

run.backend:
	if pgrep trojan; then false; else true; fi
	cd backend; ./main.py

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
