#include <stdio.h>

#include "config.h"
#include "logic.h"

int main(void) {
    printf("%s\n", LABEL);
    printf("value=%d\n", compute(5));
    return 0;
}
