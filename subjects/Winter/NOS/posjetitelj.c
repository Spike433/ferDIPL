#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <signal.h>
#include <time.h>
#include <string.h>

int key, msqid;

struct my_msgbuf
{
    long mtype;
    char mtext[200];
};

void push(char *text)
{
    struct my_msgbuf buf;
    buf.mtype = 1;
    strcpy(buf.mtext, text);

    if (msgsnd(msqid, (struct msgbuf *)&buf, strlen(text) + 1, 0) == -1)
        perror("msgsnd");
}

void pop(char *dest)
{
    usleep((20 + rand() % 80));
    struct my_msgbuf buf;
    if (msgrcv(msqid, (struct msgbuf *)&buf, sizeof(buf) - sizeof(long),
               0, 0) == -1)
    {
        perror("msgrcv");
        exit(1);
    }

    strcpy(dest, buf.mtext);
}

char sjedi = 0;

int main()
{
    srand(getpid() * time(NULL));

    key = getuid();
    if ((msqid = msgget(key, 0600 | IPC_CREAT)) == -1)
    {
        perror("msgget");
        exit(1);
    }

    // printf("aaa %d\n", getpid());

    for (int i = 0; i < 3;)
    {
        usleep(1000ll * (200 + rand() % 800));

        char a[200];

        pop(a);

        // printf("pid %d: %s\n", getpid(), a);

        if (a[0] == 'c' && !sjedi)
        {
            char f = 0;
            for (int i = 1; i < 5; ++i)
            {
                if (a[i] == '0')
                {
                    a[i] = '1';

                    sprintf(a, "%s %d", a, getpid());
                    push(a);
                    f = 1;

                    sjedi = 1;
                    ++i;
                    printf("%d sjeo\n", getpid());
                    break;
                }
            }
            if (f == 0)
            {
                printf("%d pokrenuo\n", getpid());
                usleep(1000ll * (1000 + rand() % 2000));

                printf("%d zaustavlja\n", getpid());

                a[0] = 's';
                push(a);
            }
        }
        else if (a[0] == 's')
        {
            int n = (a[1] == '1') +
                    (a[2] == '1') +
                    (a[3] == '1') +
                    (a[4] == '1');
            pid_t pids[4] = {0};

            sscanf(a + 5, "%d %d %d %d", pids, pids + 1, pids + 2, pids + 3);

            // printf("%s, %d: ", a, n);
            // for (int j = 0; j < 4; ++j)
            //     printf("%d ", pids[j]);
            // printf("\n");

            // printf("%s %d\n", a, n);

            if (n == 0)
            {
                printf("Svi sišli\n");
                push("c0000");
            }
            else if ((pids[0] == getpid() ||
                      pids[1] == getpid() ||
                      pids[2] == getpid() ||
                      pids[3] == getpid()) &&
                     sjedi)
            {
                sjedi = 0;

                char pos = 0;
                for (int j = 0; j < 4; ++j)
                    if (pids[j] == getpid())
                        pos = j;

                a[1 + pos] = '0';

                printf("%d ustao\n", getpid());
                push(a);
            }
            else
            {
                push(a);
            }
        }
        else
        {
            push(a);
        }
    }

    printf("%d vozio triput\n", getpid());
}