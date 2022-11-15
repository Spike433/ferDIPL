#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <signal.h>
#include <string.h>
#include <time.h>

int key, msqid;

struct my_msgbuf
{
    long mtype;
    char mtext[200];
};

void retreat(int failure)
{
    if (msgctl(msqid, IPC_RMID, NULL) == -1)
    {
        perror("msgctl");
        exit(1);
    }
    exit(0);
}

void run_visitors()
{
    for (int i = 0; i < 8; ++i)
    {
        switch (fork())
        {
        case -1:
            printf("Ne mogu kreirati novi proces\n");
            break;
        case 0:
            execl("./posjetitelj", "posjetitelj", NULL);
            exit(1);
        }
    }
}

void push(char *text)
{
    struct my_msgbuf buf;
    buf.mtype = 1;
    strcpy(buf.mtext, text);

    if (msgsnd(msqid, (struct msgbuf *)&buf, strlen(text) + 1, 0) == -1)
        perror("msgsnd");
}

int main(int argc, char *argv[])
{
    srand(getpid() * time(NULL));

    key = getuid();
    if ((msqid = msgget(key, 0600 | IPC_CREAT)) == -1)
    {
        perror("msgget");
        exit(1);
    }

    sigset(SIGINT, retreat);

    run_visitors();

    push("c0000");

    for (;;)
    {
    }
}