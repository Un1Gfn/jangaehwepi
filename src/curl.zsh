#!/usr/bin/env zsh

sep(){
  echo
  echo "--------------------------------"
  echo
}

sep
curl -v http://192.168.0.223:6081/list; echo; sep
# curl -v http://192.168.0.223:6081/activate/0; sep
