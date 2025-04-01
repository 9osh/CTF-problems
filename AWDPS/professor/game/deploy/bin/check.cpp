#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cstdlib>
#include <cstring>
 
int malloc_times = 0;
int realloc_times = 0;
int calloc_times = 0;
int free_times = 0;
#define GIFTSIZE 300

typedef struct {
    int flags;
    int size;
    char *content;
}Gift;

extern Gift gifts[GIFTSIZE];
extern int cont;
class MyFinalizer {
public:
    ~MyFinalizer() {
        int flag = 1;
        printf("malloctimes: %d    freetimes: %d\n",malloc_times,free_times);
        for(int i=0;i<GIFTSIZE;i++){
            if(gifts[i].content!=NULL)
                flag = 0;
        }
        if(malloc_times==2 && free_times==2 && flag == 1)
            printf("check free success");
        std::cout << "Finalizing..." << std::endl;
    }
};

MyFinalizer globalFinalizer;

void* operator new(size_t size) {
    void* ptr = std::malloc(size);
    if (ptr != nullptr) {
        std::memset(ptr, 0x0, size);
    }
    malloc_times++;
    if(free_times==1)
        printf("gift[1]: %p",gifts[1].content);
    return ptr;
}

void operator delete(void* ptr) noexcept {
    std::free(ptr);
    free_times++;
}
