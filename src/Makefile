$(info please run this Makefile on Linux)

MAKEFLAGS:=-j1

default:
	./mklnk.zsh
	rm -fv backend/active.json
	rm -fv backend/blacklist.json
	rm -fv backend/clash.yaml
	rm -fv backend/storage.json
	$(MAKE) run

run:
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
