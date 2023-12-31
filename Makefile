ifeq ($(shell uname -s),Darwin)
  $(info loading homebrew compat $$PATH ...)
  include /usr/local/share/make/compat.mk
else
  $(error Root Makefile on macOS, sub Makefile on Linux)
endif

MAKEFLAGS:=-j1

default:
	true

rsync:
	ssh root@820g3 systemctl start rsyncd.service
	while true; do sleep 1; find . -type f | entr ./rsync.zsh . rsync://820g3/hudrpl/jangaehwepi@820g3; done

ssh:
	ssh root@820g3 -t sudo -u rsync /bin/bash --rcfile /RSYNC/jangaehwepi@820g3/ssh.bashrc || true

clean:
	./rsync.zsh --delete . rsync://820g3/hudrpl/jangaehwepi@820g3

# delete files but keep directory structure to avoid "cd $PWD"
skeleton:
	ssh root@820g3 sudo -i -u rsync find /RSYNC/jangaehwepi@820g3 ! -type d -print -delete

purge:
	ssh root@820g3 rm -rfv /RSYNC/jangaehwepi@820g3
