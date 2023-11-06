#!/dev/null

encrypt(){
    ssh-keygen -f ~/.ssh/id_rsa.pub -e -m PKCS8 > /tmp/id_rsa.pem.pub
    openssl pkeyutl -encrypt -pubin -inkey /tmp/id_rsa.pem.pub <<<"$1" | base64 -w 0
}

decrypt(){
    base64 -d <<<"$1" | openssl pkeyutl -decrypt -inkey ~/.ssh/id_rsa
}
