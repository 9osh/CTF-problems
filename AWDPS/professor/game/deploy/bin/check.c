#include <stdio.h>
#include <stdlib.h>
#include <string.h>
 
extern void * __libc_malloc(size_t size);
extern void * __libc_realloc(void *ptr, size_t size);
extern void * __libc_calloc(size_t count, size_t size);
extern void * __libc_free(void *ptr);
 
int malloc_times = 0;
int realloc_times = 0;
int calloc_times = 0;
int free_times = 0;
 
#define CHUNK_LENGTH 0x100
void *chunk[CHUNK_LENGTH];
 
void *malloc(size_t size)
{
    char *ptr = NULL;
    int i = 0;
    malloc_times ++;
    ptr = __libc_malloc(size);
    if (ptr)
    {
        for (i = 0; i < CHUNK_LENGTH; i++)
        {
            if (chunk[i] == NULL)
            {
                chunk[i] = ptr;
                break;
            }
        }
    }
    return ptr;
}
 
void *realloc(void *ptr, size_t size)
{
    char *tmp = NULL;
    int i;
 
    realloc_times ++;
    if (ptr)
    {
        for (i = 0; i < CHUNK_LENGTH; i++)
        {
            if (chunk[i] == ptr)
            {
                chunk[i] = NULL;
                break;
            }
        }
    }
    tmp = __libc_realloc(ptr, size);
    if (tmp)
    {
        for (i = 0; i < CHUNK_LENGTH; i++)
        {
            if (chunk[i] == NULL)
            {
                chunk[i] = tmp;
                break;
            }
        }
    }
    return tmp;
}
 
void *calloc(size_t count, size_t size)
{
    char *ptr = NULL;
    int i = 0;
    calloc_times ++;
    ptr = __libc_calloc(count, size);
    if (ptr)
    {
        for (i = 0; i < CHUNK_LENGTH; i++)
        {
            if (chunk[i] == NULL)
            {
                chunk[i] = ptr;
                break;
            }
        }
    }
    return ptr;
}
 
void free(void *ptr)
{
    int i = 0;
    free_times++;
    if (ptr)
    {
        for (i = 0; i < CHUNK_LENGTH; i++)
        {
            if (chunk[i] == ptr)
            {
                chunk[i] = NULL;
                break;
            }
        }
 
        if (i == CHUNK_LENGTH)
        {
            printf("free check\n");
            exit(EXIT_FAILURE);
        }
    }
    __libc_free(ptr);
}

__attribute__((destructor))
static void check_fini()
{
    int i;
    setvbuf(stdout, NULL, _IONBF, 0);
    printf("check_fini\n");
 
    for(i = 0; i < CHUNK_LENGTH; i++)
    {
        if (chunk[i])
        {
            break;
        }
    }
#ifdef DEBUG
    printf("malloc_times: %d, realloc_times: %d, calloc_times: %d, free_times: %d, i: %d\n", malloc_times, realloc_times, calloc_times, free_times, i);
#endif
    if(i == CHUNK_LENGTH && malloc_times == 6 && realloc_times == 0 && calloc_times == 0 && free_times == 6)
    {
        printf("check_free\n");
    }
}