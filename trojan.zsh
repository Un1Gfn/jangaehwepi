#!/bin/zsh

source /usr/local/share/homebrew/compat.zshrc
source ~/jangaehwepi/jangaehwepi.zshrc

cat <<EOF >/tmp/trojan.json
{
  "run_type": "client",
  "local_addr": "127.0.0.1",
  "local_port": 1080,
  "remote_addr": "`decrypt pLoKSdUtMhoyr5bVkHqxQOXTU9xyfz9FWWRp357j3DsWAOT+92XEsYeX16lEQ251O3tYFvFHTRztmmJGBVcLzniNpXqTs0Oi/ZPCAM7WykKekx2J+G0gmcbF6RQ7ZWV0T4nUCR1n6OSVKFkDMPIFQsV+c6VprcjLJ6W8qpRTAFmlCE4DY+LiuAYlufppzF+x/GEoZGTqsI8nVkoe681BLnC+VIY6RNKHdZSOXfvMHQNiGiBQGUSetWowIOqCnZx65XWsU/Y75yGrn9xqsiKaUzeISoDourYkv3mr9v0sONqXqNkvIgWH0S0/H6LveDIV1Tt410AdYx9QNtCa8iSTTQ==`",
  "remote_port": `decrypt RdtVDUu/DI98byALw79KDdee5QYO9gAtC6rmwMR+G/khM1+ZKXE3wibl3TqdoYM8LE92vyatiGbhRUTexd62GVs4NoczI7R3b+n1BvaH5thH9bong1e0QPV2vUk5H0szxanasCOB3/RSXyaqRca5t8uZlsgNwJiQquW/10hcPfhhfRgd3ZRuuD6cbJk9L9LVER6gFpZckfsXVuKUSCyjblKMtYbgV5HW1ujxrTpM9EZwlg6clE0XK3ZBC0yk5xaKSMLU4B/rM0xiQ5d/FKmhOm7GcS/iyjC2HJy6uZ/5gQJkWFXO6QFfInvj8qB3zAWpEzJ91S4UHI155RZoX5iVUQ==`,
  "password": [
      "`decrypt yV7OC7hIOeKO5MSAHrMFxAfrTGHpUr/lsgcwY7Wttb1SqjOAulxMVZTjI/RW+ja3AhEnhhtbFy9Th8MDa0LyhFXewQI+iMhP2P0VxMSlSt87ngjLHtwuk9bmj1m/bCWgNPYqmYg71dBOQEa6OZk+eWfMpZ2TNVye9dGAvJJExFSBxjf2CMyhNlZyF/YjdJbBBPRYCWSwPi09Psgtm6UzJnxlcygZ5WqdQWpW7geWYpvxxfRxhENfSNW2J6aNJFJur4FIAJPSIsQPp1PruHBabVMHCzaeP0l3Isln4GcKV5g06eQ2xola18ndaCydCDjd2uIwuGBp7KjbIWQm3IE6Jg==`"
  ],
  "log_level": 1,
  "ssl": {
      "verify": false,
      "verify_hostname": false,
      "cert": "",
      "sni": "microsoft.com",
      "alpn": [
          "h2",
          "http/1.1"
      ],
      "reuse_session": true,
      "session_ticket": false,
      "curves": ""
  },
  "tcp": {
      "no_delay": true,
      "keep_alive": true,
      "reuse_port": false,
      "fast_open": false,
      "fast_open_qlen": 20
  }
}
EOF

trojan-go -config /tmp/trojan.json
