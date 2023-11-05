#!/bin/zsh

CMD=(

  /opt/homebrew/opt/rsync/bin/rsync

  -v # verbose

  --open-noatime
  --update

  # -a # -rlptgo
  --recursive
  --links # keep symlink
  --perms # keep permission
  --times # keep mtime
  # -g # keep group
  # -o # keep owner
  # -D # --devices --specials

  # -z # compress

)

$CMD[@] $@
