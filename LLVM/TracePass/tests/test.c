#include <stdio.h>

static int add(int a, int b) {
  return a + b;
}

void helper(void) {
  volatile int x = add(2, 3);
  (void)x;
}

int main(void) {
  helper();
  printf("LOG: main is done\n");
  return 0;
}

