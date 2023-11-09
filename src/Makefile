$(info please run this Makefile on Linux)

MAKEFLAGS:=-j2

default: api ui

api:
	cd backend; ./main.py 0.0.0.0 6081

ui:
	cd frontend; busybox httpd -f -vv -p 0.0.0.0:6080 -h .

# https://datatables.net/download/
download:
	cd frontend/external/; ./download.zsh
