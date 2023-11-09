#!/usr/bin/env zsh

sep(){
  echo
  echo "--------------------------------"
  echo
}

sep
curl -v http://192.168.0.223:6081/list; echo; sep
curl -v http://192.168.0.223:6081/err0; sep
curl -v http://192.168.0.223:6081/err1; sep
curl -v http://192.168.0.223:6081/err2; sep
