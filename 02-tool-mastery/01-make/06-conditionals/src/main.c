#include <stdio.h>

int main(void) {
#ifdef DEBUG
    puts("Running in DEBUG mode");
#else
    puts("Running in RELEASE mode");
#endif
    return 0;
}
