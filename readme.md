## jangaehwepi

## 장애 회피

🕯️ R.I.P. Dreamacro/clash 🕯️

```plain
// <https://poe.com/s/Q81DPj93z7MDBYC54YNM>

// global
pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
int thread_finished = -1;

static void *sr_httping(const void *const d){
    httping();
    pthread_mutex_lock(&m);
    thread_finished = *(const int*)d;
    pthread_cond_signal(&cond);
    pthread_mutex_unlock(&m);
    return NULL;
}

static void *sr_mgmt(void*){
    pthread_mutex_lock(&m);
    for(;;){
        pthread_cond_wait(&cond, &m);
        printf("thread %d done\n", thread_finished);
    }
    pthread_mutex_unlock(&m);
}

void pub_start(int *ctypesbuf){
    th_mgmt=pthread_create(_, _, sr_mgmt, &(int)(0));
    for(int i=1; i<=8; ++i)
        pthread_create(_, _, sr_httping, &(int)(i));
}

void pub_stop(int *ctypesbuf){
    pthread_kill(th_mgmt, _);
}

```

<https://man.archlinux.org/man/core/man-pages/pthreads.7.en>

<https://trojan-gfw.github.io/trojan/config>

parallelism = 1
timeout_ms = 4000
n_httping = 3
total = 0:03:36.626869

```zsh
for id in ...; do
  sleep 0.3
  curl http://820g3:6081/g_ban/$id
done
```
