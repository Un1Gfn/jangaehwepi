#include <assert.h>
#include <stdio.h>
#include <curl/curl.h>
#include <time.h>
#include <stdlib.h>
#include "connectivitycheck.h"

struct timespec tb={}, te={};

size_t write_callback(char*, size_t size, size_t nmemb, void*){
  return size * nmemb;
}

char *timediff(){
  // ++te.tv_sec;
  long ms = (te.tv_sec - tb.tv_sec) * 1000 + (te.tv_nsec - tb.tv_nsec) / 1000000;
  char *s=NULL;
  // asprintf(&s, "%ld s %ld ns\n" "%ld s %ld ns\n" "%ld ms", tb.tv_sec, tb.tv_nsec, te.tv_sec, te.tv_nsec, ms); assert(s);
  asprintf(&s, "response time %ld ms", ms); assert(s);
  return s;
}

char *httping(const char *const url, const char *const s5hpxy){

  curl_global_init(CURL_GLOBAL_DEFAULT);
  CURL* c=curl_easy_init(); assert(c);

  assert(CURLE_OK==curl_easy_setopt(c, CURLOPT_URL, url));
  assert(CURLE_OK==curl_easy_setopt(c, CURLOPT_PROXY, s5hpxy));
  assert(CURLE_OK==curl_easy_setopt(c, CURLOPT_SOCKS5_AUTH, (long)CURLAUTH_NONE));
  curl_easy_setopt(c, CURLOPT_WRITEFUNCTION, write_callback);
  curl_easy_setopt(c, CURLOPT_TIMEOUT_MS, 15000);

  struct timespec r={};
  assert(0==clock_getres(CLOCK_REALTIME, &r));
  assert(0==r.tv_sec);
  assert(1==r.tv_nsec);

  clock_gettime(CLOCK_REALTIME, &tb);
  const CURLcode n=curl_easy_perform(c);
  clock_gettime(CLOCK_REALTIME, &te);

  char *s=NULL;
  if(CURLE_OK==n)
    s=timediff();
  else
    asprintf(&s, "request failed with error %s\n", curl_easy_strerror(n));

  curl_easy_cleanup(c);
  curl_global_cleanup();

  return s;

}

int main(){
  char *s=httping(CONNECTIVITYCHECK, "socks5h://127.0.0.1:7890");
  puts(s);
  free(s); s=NULL;
  return 0;
}
