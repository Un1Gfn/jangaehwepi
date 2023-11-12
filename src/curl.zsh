#!/usr/bin/env zsh

sep(){
  echo
  echo "--------------------------------"
  echo
}

sep
# curl -v http://192.168.0.223:6081/g_list/; echo; sep
# curl -v http://192.168.0.223:6081/g_activate/23; sep
curl -v http://192.168.0.223:6081/g_benchmark/; sep
