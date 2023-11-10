$(info please run this Makefile on Linux)

MAKEFLAGS:=-j2

default:
	$(MAKE) ps
	$(MAKE) api ui

ps:
	ps aux | grep -i -e trojan -e httpd

api:
	cd backend; ./main.py 0.0.0.0 6081

ui:
	cd frontend; busybox httpd -f -vv -p 0.0.0.0:6080 -h .

# https://datatables.net/download/
download:
	cd frontend/external/; ./download.zsh
