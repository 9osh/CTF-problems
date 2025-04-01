#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

int main() {
    char *argv[] = {"python3","/root/make_and_run.py",NULL};
    char *envp[] = {"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin","TERM=xterm-256color","LANG=C.UTF-8",NULL};
    signal(SIGINT, SIG_IGN);
    setuid(0);
    setgid(0);
    execve("/usr/bin/python3",argv,envp);
    return 0;
}
