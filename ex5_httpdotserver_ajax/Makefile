$(info please run this Makefile on Linux)

MAKEFLAGS:=-j2

default: api

default: api ui

api:
	backend/api.py 0.0.0.0 6081

ui:
	busybox httpd -f -vv -p 0.0.0.0:6080 -h frontend/
