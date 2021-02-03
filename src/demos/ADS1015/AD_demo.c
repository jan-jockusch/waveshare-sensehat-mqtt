#include "AD.h"
#include <bcm2835.h>
#include <stdio.h>

int main() {
  int16_t AIN0_DATA, AIN1_DATA, AIN2_DATA, AIN3_DATA;
  printf("\nADS1015 Test Program ...\n");
  if (!bcm2835_init())
    return 1;
  if (ADS1015_INIT() != 0x8000) {
    printf("\nADS1015 Error\n");
    return 0;
  }
  bcm2835_delay(10);
  printf("\nADS1015 OK\n");
  while (1) {
    AIN0_DATA = ADS1015_SINGLE_READ(0);
    AIN1_DATA = ADS1015_SINGLE_READ(1);
    AIN2_DATA = ADS1015_SINGLE_READ(2);
    AIN3_DATA = ADS1015_SINGLE_READ(3);
    printf("\nAIN0 = %d(%dmv) ,AIN1 = %d(%dmv) ,AIN2 = %d(%dmv) AIN3 = "
           "%d(%dmv)\n\r",
           AIN0_DATA, AIN0_DATA * 2, AIN1_DATA, AIN1_DATA * 2, AIN2_DATA,
           AIN2_DATA * 2, AIN3_DATA, AIN3_DATA * 2);
    bcm2835_delay(500);
  }
  return 1;
}
