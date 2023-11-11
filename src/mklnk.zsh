#!/usr/bin/env zsh

case `uname -s` in
  Linux)
    ln -sfv /etc/jangaehwepi.conf.py backend/lnk_conf.py
    ln -sfv /etc/jangaehwepi.conf.js frontend/lnk_conf.js
    ;;
  Darwin)
    gln -sfv /usr/local/etc/jangaehwepi.conf.py backend/lnk_conf.py
    gln -sfv /usr/local/etc/jangaehwepi.conf.js frontend/lnk_conf.js
    ;;
esac
