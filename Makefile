ifeq ($(shell uname -s),Darwin)
  $(info loading homebrew compat $$PATH ...)
  include /usr/local/share/make/compat.mk
else
  $(error Root Makefile on macOS, sub Makefile on Linux)
endif

MAKEFLAGS:=-j1

default:
	true

ssh:
	ssh root@820g3 -t sudo -u rsync /bin/bash --rcfile /RSYNC/jangaehwepi@820g3/ssh.bashrc

rsync:
	find . -type f | entr ./rsync.zsh . rsync://820g3/hudrpl/jangaehwepi@820g3

distclean:
	ssh root@820g3 rm -rfv /RSYNC/jangaehwepi@820g3

clean:
	./rsync.zsh --delete . rsync://820g3/hudrpl/jangaehwepi@820g3

# https://datatables.net/download/
download:
	F="jquery.dataTables.css"; test -e "$$F" || curl "https://cdn.datatables.net/1.13.7/css/jquery.dataTables.css" -o "$$F"
	F="select.dataTables.css"; test -e "$$F" || curl "https://cdn.datatables.net/select/1.7.0/css/select.dataTables.css" -o "$$F"
	F="jquery.js";             test -e "$$F" || curl "https://code.jquery.com/jquery-3.7.0.js" -o "$$F"
	F="jquery.dataTables.js";  test -e "$$F" || curl "https://cdn.datatables.net/1.13.7/js/jquery.dataTables.js" -o "$$F"
	F="dataTables.select.js";  test -e "$$F" || curl "https://cdn.datatables.net/select/1.7.0/js/dataTables.select.js" -o "$$F"
