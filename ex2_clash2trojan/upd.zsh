#!/bin/zsh

source /usr/local/share/homebrew/compat.zshrc
source ~/jangaehwepi/jangaehwepi.zshrc

U=`decrypt Er9Fo/cJhKjQINkW3JimUwgVLXur6Hy2nsvRbHokldGU5AMLIPmci9l9+fDomoIWfdBRFBXVuulINHsJCwWSds8CtJvtjb83XGZeC8belrI+z95VL2mF0oeIHyi0Z4wEQjxg4NuvwPc0qUzHIZW5C0M4HUm6QaapQ534OCsg00WAe+AzHRQZzmhtimwhU6Y/cBAk5/GEbK9cTfcQzZavDImCZnRv1eXPN5UeGfDAD3PrFP56FqgYP05Lnrr48SLPiqJjoW6llYyVi8bD0c5/ajUMuppOMVG9A53Iv55ZbqQmLRe0TZVd60jIciNVDTsWk1pXj+q9YcRadDm6O+SC/g==`

curl -x socks5h://127.0.0.1:1080 -o clash.yaml $U
cp -v clash{,_`date +%s`}.yaml
# curl -x socks5h://127.0.0.1:1080 $U
