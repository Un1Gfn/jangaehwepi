#!/usr/bin/env zsh

download(){
  rm $1
  curl -o $1 $2
}

download jquery.dataTables.css  "https://cdn.datatables.net/1.13.7/css/jquery.dataTables.css"
download buttons.dataTables.css "https://cdn.datatables.net/buttons/2.4.2/css/buttons.dataTables.css"
download select.dataTables.css  "https://cdn.datatables.net/select/1.7.0/css/select.dataTables.css"

download jquery.js              "https://code.jquery.com/jquery-3.7.0.js"
download jquery.dataTables.js   "https://cdn.datatables.net/1.13.7/js/jquery.dataTables.js"
download dataTables.buttons.js  "https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.js"
download dataTables.select.js   "https://cdn.datatables.net/select/1.7.0/js/dataTables.select.js"
