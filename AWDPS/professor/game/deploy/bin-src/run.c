#define _GNU_SOURCE
#include <linux/seccomp.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <syscall.h>
#include <sys/prctl.h>
#include <sys/wait.h>
#include <sys/mman.h>

char *sig_name[] = {
    "0",
    "SIGHUP",
    "SIGINT",
    "SIGQUIT",
    "SIGILL",
    "SIGTRAP",
    "SIGABRT",
    "7",
    "SIGFPE",
    "SIGKILL",
    "SIGBUS",
    "SIGSEGV",
    "SIGSYS",
    "SIGPIPE",
    "SIGALRM",
    "SIGTERM",
    "SIGURG",
    "SIGSTOP",
    "SIGTSTP",
    "SIGCONT",
    "SIGCHLD",
    "SIGTTIN",
    "SIGTTOU",
    "SIGPOLL",
    "SIGXCPU",
    "SIGXFSZ",
    "SIGVTALRM",
    "SIGPROF",
    "SIGWINCH",
    "29",
    "SIGUSR1",
    "SIGUSR2",
    "__SIGRTMIN"
};

static void install_seccomp()
{
    static unsigned char filter[] = {32, 0, 0, 0, 4, 0, 0, 0, 21, 0, 0, 10, 62, 0, 0, 192, 32, 0, 0, 0, 0, 0, 0, 0, 53, 0, 8, 0, 0, 0, 0, 64, 21, 0, 7, 0, 61, 1, 0, 0, 21, 0, 6, 0, 101, 0, 0, 0, 21, 0, 5, 0, 157, 0, 0, 0, 21, 0, 4, 0, 57, 0, 0, 0, 21, 0, 3, 0, 58, 0, 0, 0, 21, 0, 2, 1, 62, 0, 0, 0, 6, 0, 0, 0, 5, 0, 5, 0, 6, 0, 0, 0, 0, 0, 255, 127, 6, 0, 0, 0, 0, 0, 0, 0};
    struct prog
    {
        unsigned short len;
        unsigned char *filter;
    } rule = {
        .len = sizeof(filter) >> 3,
        .filter = filter};
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0)
    {
        perror("prctl(PR_SET_NO_NEW_PRIVS)");
        exit(EXIT_FAILURE);
    }
    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &rule) < 0)
    {
        perror("prctl(PR_SET_SECCOMP)");
        exit(EXIT_FAILURE);
    }
}

void readn(int fd, char *buf, int size)
{
    int result = 0, pi = 0;
    while(pi < size)
    {
        result = read(fd, buf + pi, size - pi);
        if(result <= 0)
        {
            perror("read");
            exit(EXIT_FAILURE);
        }
        pi += result;
    }
}

void writen(int fd, char *buf, int size)
{
    int result = 0, pi = 0;
    while(pi < size)
    {
        result = write(fd, buf + pi, size - pi);
        if(result <= 0)
        {
            perror("write");
            exit(EXIT_FAILURE);
        }
        pi += result;
    }
}

int main(int argc, char *argv[])
{
    pid_t pid;
    int memfd = 0;
    int wstatus;
    int size = 0;
    char *buf = NULL;
    int fd = 0;

    setbuf(stdout, NULL);

    if (argc != 2)
    {
        printf("usage: %s elf_to_run\n", argv[0]);
        return -1;
    }

    pid = fork();
    if(pid == 0)
    {
        memfd = memfd_create("main", MFD_CLOEXEC);
        if((fd = open(argv[1], O_RDONLY)) == -1)
        {
            perror("open");
            exit(EXIT_FAILURE);
        }
        if((size = lseek(fd, 0, SEEK_END)) == -1)
        {
            perror("lseek");
            exit(EXIT_FAILURE);
        }
        if(lseek64(fd, 0, SEEK_SET) == -1)
        {
            perror("lseek");
            exit(EXIT_FAILURE);
        }
        buf = calloc(1, size);
        if(buf == NULL)
        {
            perror("calloc");
            exit(EXIT_FAILURE);
        }
        readn(fd, buf, size);
        if(close(fd) == -1)
        {
            perror("close");
            exit(EXIT_FAILURE);
        }
        writen(memfd, buf, size);

        system("rm -rf /tmp/test 1>/dev/null 2>/dev/null");

        puts("run");

        if(prctl(PR_SET_PDEATHSIG, SIGKILL, 0, 0, 0) == -1)
        {
            perror("prctl(PR_SET_PDEATHSIG)");
            exit(EXIT_FAILURE);
        }
        install_seccomp();
        
        syscall(SYS_execveat, memfd, "", NULL, NULL, AT_EMPTY_PATH);

        while(1)
            exit(EXIT_FAILURE);
    }
    
    if(waitpid(pid, &wstatus, 0) == pid)
    {
        if (WIFEXITED(wstatus)) {
            switch(WEXITSTATUS(wstatus))
            {
            case EXIT_SUCCESS:
                printf("exited|EXIT_SUCCESS\n");
                break;
            case EXIT_FAILURE:
                printf("exited|EXIT_FAILURE\n");
                break;
            default:
                printf("exited|%d\n", WEXITSTATUS(wstatus));
                break;
            }
        } else if (WIFSIGNALED(wstatus)) {
            if(WTERMSIG(wstatus) < sizeof(sig_name)/sizeof(char*))
            {
                printf("killed|%s\n", sig_name[WTERMSIG(wstatus)]);
            }
            else
            {
                printf("killed|%d\n", WTERMSIG(wstatus));
            }
        } else if (WIFSTOPPED(wstatus)) {
            if(WSTOPSIG(wstatus) < sizeof(sig_name)/sizeof(char*))
            {
                printf("stopped|%s\n", sig_name[WSTOPSIG(wstatus)]);
            }
            else
            {
                printf("stopped|%d\n", WSTOPSIG(wstatus));
            }
        } else if (WIFCONTINUED(wstatus)) {
            printf("continued\n");
        }
    }
    
    return 0;
}
