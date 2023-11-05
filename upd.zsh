#!/bin/zsh

source /usr/local/share/homebrew/compat.zshrc
source jangaehwepi.zshrc

U=`decrypt Z1U2r+hMhogAoLCz2bI7SrfaDEq8EAY6RyTNNGiC/NyzsitQH/5nfYQvcr+1aeApeQ3oWy01sfU4HqP6AwDdtr1m5sHQX5RMLD0fOjXHDzsCRx+VuXHgaSZdqlfU8zljB+73rW06aOapUWcLXDuamGZfysVWhfR2fR3dfHUXqye9nj/A2tMoidDqauAPZ7xGiVmhxcFhQZs3WDx9dHOhVs1BK+lIDFBesxVNhHEdcUw/08PyrWHfIwAzhRwqc8dRy/c6DAuWimtjPAgeMNJLIuq0gdJTC4wh01HTV11hG76LJGU6/2elz5LIhNFfcWEHu3kvnnyz3V7vC96BvA9yJA==`

curl -x socks5h://127.0.0.1:1080 -o trojan.txt $U
cp -v trojan{,_`date +%s`}.txt
# curl -x socks5h://127.0.0.1:1080 $U
