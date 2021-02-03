#include "SHTC3.h"
#include <bcm2835.h>
#include <stdio.h>

int main() {
  uint8_t state;
  printf("\n SHTC3 Sensor Test Program ...\n");
  if (!bcm2835_init())
    return 1;
  bcm2835_i2c_setSlaveAddress(SHTC3_I2C_ADDRESS);
  bcm2835_i2c_set_baudrate(10000);
  SHTC_SOFT_RESET();
  while (1) {
    state = SHTC3_Read_DATA();
    state |= SHTC3_SLEEP();
    state |= SHTC3_WAKEUP();
    if (state)
      printf("\n SHTC3 Sensor Error\n");
    else
      printf("Temperature = %6.2f°C , Humidity = %6.2f%% \r\n", TH_Value,
             RH_Value);
  }
  return 0;
}
