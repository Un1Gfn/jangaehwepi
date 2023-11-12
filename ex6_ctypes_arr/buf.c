#include <stdint.h>

void buf(int32_t *const latency, int32_t n){
  for(int32_t i=0; i<n; ++i)
    latency[i] = 1000+n*i;
}
