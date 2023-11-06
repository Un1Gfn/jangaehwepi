// https://en.cppreference.com/w/c/language/operator_precedence
// cast [(type)] and dereference [*]
// same level of precedence
// L<-R associativity

#include <assert.h>
#include <unistd.h>
#include <pthread.h>
#include <stdlib.h>

void *sr(void *pv){
  int *const pn=pv;
  const useconds_t MX=1900;
  const useconds_t Mn=1;
  for(;;){
    // sleep(1);
    useconds_t ms=Mn+random()%(MX+1-Mn);
    usleep(ms*1000);
    *pn=ms;
  }
  return NULL;
}

void bgtask(int *arg){
// void bgtask(){

  // assert(0);

  pthread_attr_t ta={};
  assert(0==pthread_attr_init(&ta));

  pthread_t th = -1;
  assert(0==pthread_create(&th, &ta, sr, arg));
  // assert(0==pthread_create(&th, &ta, routine, arg);

}
