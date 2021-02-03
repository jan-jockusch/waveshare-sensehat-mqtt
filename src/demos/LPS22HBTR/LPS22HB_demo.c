#include "LPS22HB.h"
#include <bcm2835.h>
#include <stdio.h>

int main() {
  float PRESS_DATA = 0;
  float TEMP_DATA = 0;
  uint8_t u8Buf[3];
  if (!bcm2835_init())
    return 1;
  printf("\nPressure Sensor Test Program ...\n");
  if (!LPS22HB_INIT()) {
    printf("\nPressure Sensor Error\n");
    return 0;
  }
  printf("\nPressure Sensor OK\n");
  while (1) {
    LPS22HB_START_ONESHOT(); // Trigger one shot data acquisition
    if ((I2C_readByte(LPS_STATUS) & 0x01) ==
        0x01) // a new pressure data is generated
    {
      u8Buf[0] = I2C_readByte(LPS_PRESS_OUT_XL);
      u8Buf[1] = I2C_readByte(LPS_PRESS_OUT_L);
      u8Buf[2] = I2C_readByte(LPS_PRESS_OUT_H);
      PRESS_DATA =
          (float)((u8Buf[2] << 16) + (u8Buf[1] << 8) + u8Buf[0]) / 4096.0f;
    }
    if ((I2C_readByte(LPS_STATUS) & 0x02) ==
        0x02) // a new pressure data is generated
    {
      u8Buf[0] = I2C_readByte(LPS_TEMP_OUT_L);
      u8Buf[1] = I2C_readByte(LPS_TEMP_OUT_H);
      TEMP_DATA = (float)((u8Buf[1] << 8) + u8Buf[0]) / 100.0f;
    }

    printf("Pressure = %6.2f hPa , Temperature = %6.2f °C\r\n", PRESS_DATA,
           TEMP_DATA);
  }
  return 0;
}
