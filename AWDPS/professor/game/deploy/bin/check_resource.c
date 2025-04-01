#include <stdio.h>
#include <stdio.h>
#include <string.h>
 
extern FILE *_IO_fopen(const char * pathname, const char * mode);
extern int _IO_fclose(FILE *stream);
 
int fopen_times = 0;
int fclose_times = 0;
 
#define LENGTH 0x100
FILE* file[LENGTH];
 
FILE *fopen(const char * pathname, const char * mode)
{
    FILE *fp = _IO_fopen(pathname, mode);
    if (fp)
    {
        for(int i = 0; i < LENGTH; i++)
        {
            if (file[i] == NULL)
            {
                file[i] = fp;
                break;
            }
        }
    }
    fopen_times ++;
    return fp;
}
 
int fclose(FILE *stream)
{
    if (stream)
    {
        for(int i = 0; i < LENGTH; i++)
        {
            if (file[i] == stream)
            {
                file[i] = NULL;
            }
        }
    }
    fclose_times ++;
    return _IO_fclose(stream);
}
 
__attribute__((destructor))
static void check_fini()
{
    int i = 0;
    setvbuf(stdout, NULL, _IONBF, 0);
    printf("check_fini\n");
#ifdef DEBUG
    printf("fopen_times: %d, fclose_times: %d\n", fopen_times, fclose_times);
#endif
    for(i = 0; i < LENGTH; i++)
    {
        if (file[i])
        {
            break;
        }
    }
 
    if (i == LENGTH && fopen_times == 2 && fclose_times == 1)
    {
        printf("check_fclose\n");
    }
}