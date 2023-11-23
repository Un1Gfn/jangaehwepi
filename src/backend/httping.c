// httping.c

// https://curl.se/libcurl/c/libcurl-errors.html

// identical on darwin and linux
// struct timespec {
//   time_t tv_sec;
//   long   tv_nsec;
// }

// int32_t  [-2^31, +2^31-1]
// uint32_t [ 0,    +2^32-1]
// 3 s = 3*10^9 ns > (2^31-1)
// 5 s = 5*10^9 ns > (2^32-1)
// thus we need int64_t

#include <assert.h>
#include <curl/curl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/utsname.h>
#include <time.h>
#include <time.h>

static CURL *c=NULL;

static size_t cb(char*, size_t size, size_t nmemb, void*){
  return size * nmemb;
}

void init(){

  struct timespec r={};
  assert(0==clock_getres(CLOCK_REALTIME, &r));
  assert(0==r.tv_sec);

  struct utsname u={};
  assert(0==uname(&u));

  if(0) {;}
  else if(0==strcmp("Darwin", u.sysname)) { assert(1000==r.tv_nsec); }
  else if(0==strcmp("Linux", u.sysname)) { assert(1==r.tv_nsec); }
  else { assert(0); }

  curl_global_init(CURL_GLOBAL_DEFAULT);
  c=curl_easy_init();
  assert(c);
  curl_easy_setopt(c, CURLOPT_WRITEFUNCTION, cb);

  // curl_easy_cleanup(c);
  // curl_global_cleanup();

}

int64_t ff(const char *const url, const char *const proxy, const long timeout_ms){

  assert(CURLE_OK==curl_easy_setopt(c, CURLOPT_URL, url));
  assert(CURLE_OK==curl_easy_setopt(c, CURLOPT_PROXY, proxy));
  assert(CURLE_OK==curl_easy_setopt(c, CURLOPT_SOCKS5_AUTH, (long)CURLAUTH_NONE));
  assert(CURLE_OK==curl_easy_setopt(c, CURLOPT_TIMEOUT_MS, timeout_ms));

  struct timespec t1={}, t2={};
  clock_gettime(CLOCK_REALTIME, &t1);
  const CURLcode n=curl_easy_perform(c);
  clock_gettime(CLOCK_REALTIME, &t2);

  switch(n){

    case CURLE_COULDNT_CONNECT:    fprintf(stderr, "CURLE_COULDNT_CONNECT\n");
    case CURLE_GOT_NOTHING:        fprintf(stderr, "CURLE_GOT_NOTHING\n");
    case CURLE_OPERATION_TIMEDOUT: fprintf(stderr, "CURLE_OPERATION_TIMEDOUT\n");
      return -1LL*n;
      break;

    case CURLE_OK:
      return (
        (int64_t)(t2.tv_sec  - t1.tv_sec) * 1000LL * 1000LL * 1000LL +
        (int64_t)(t2.tv_nsec - t1.tv_nsec)
      );
      break;

    default:
      fprintf(stderr, "request failed with error [%u] %s\n", n, curl_easy_strerror(n));
      assert(0);
      break;

  }

}
