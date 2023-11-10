$(info please run this Makefile on Linux)

MAKEFLAGS:=-j2

default:
	$(MAKE) sanitycheck
	$(MAKE) both

sanitycheck:
	@echo
	ps aux | grep -i -e trojan -e httpd
	@echo
	@ls -X1 ./backend
	@echo
	@file backend/storage.json; true
	@file backend/blacklist.json; true
	@echo

both:
	cd backend; ./main.py -a 0.0.0.0 -f 6080 -b 6081

# https://datatables.net/download/
download:
	cd frontend/external/; ./download.zsh

# ui:
# 	cd frontend; busybox httpd -f -p 0.0.0.0:6080 -h .
