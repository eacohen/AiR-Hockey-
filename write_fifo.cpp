#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>


int main() {
    int fd;
    char *fifo = "/tmp/fifo";
    mkfifo(fifo, 0666);

    int a = 1;
    int b = 1;
    int c = a+b;
    fd = open(fifo, O_WRONLY);
    while (1) {
        write(fd, &c, 4);
        printf("just wrote %d to pipe\n", c);
        a = b;
        b = c;
        c = a+b;
        sleep(1);
    }
    return 0;
}
