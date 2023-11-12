#!/bin/zsh

CMD=(

  /opt/homebrew/opt/rsync/bin/rsync

  -v # verbose

  --open-noatime
  --update

  # -a # -rlptgo
  --recursive
  --links # keep symlink
  --times # keep mtime
  --perms # keep permission
  # -g # keep group
  # -o # keep owner
  # -D # --devices --specials

  # -z # compress

  -S # --sparse

  --exclude=.git
  --exclude=.gitignore
  --exclude=lnk_conf.js
  --exclude=lnk_conf.py

)

# for i in ex*_* garbage*; do
#   CMD+=(--exclude=$i)
# done

exec $CMD[@] $@
