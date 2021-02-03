#include "LPS22HB.h"
#include <bcm2835.h>

char I2C_readByte(char reg) {
  char buf[] = {reg};
  bcm2835_i2c_read_register_rs(buf, buf, 1);
  return buf[0];
}
unsigned short I2C_readU16(char reg) {
  char buf[] = {reg, 0};
  bcm2835_i2c_read_register_rs(buf, buf, 2);
  int value = buf[1] * 0x100 + buf[0];
  return value;
}
void I2C_writeByte(char reg, char val) {
  char buf[] = {reg, val};
  bcm2835_i2c_write(buf, 2);
}
void LPS22HB_RESET() {
  uint8_t Buf;
  Buf = I2C_readU16(LPS_CTRL_REG2);
  Buf |= 0x04;
  I2C_writeByte(LPS_CTRL_REG2, Buf); // SWRESET Set 1
  while (Buf) {
    Buf = I2C_readU16(LPS_CTRL_REG2);
    Buf &= 0x04;
  }
}
void LPS22HB_START_ONESHOT() {
  uint8_t Buf;
  Buf = I2C_readU16(LPS_CTRL_REG2);
  Buf |= 0x01; // ONE_SHOT Set 1
  I2C_writeByte(LPS_CTRL_REG2, Buf);
}
uint8_t LPS22HB_INIT() {
  bcm2835_i2c_begin();
  bcm2835_i2c_setSlaveAddress(LPS22HB_I2C_ADDRESS); //切记不能把I2C关掉
  bcm2835_i2c_set_baudrate(10000);
  if (I2C_readByte(LPS_WHO_AM_I) != LPS_ID)
    return 0;      // Check device ID
  LPS22HB_RESET(); // Wait for reset to complete
  I2C_writeByte(LPS_CTRL_REG1,
                0x02); // Low-pass filter disabled , output registers not
                       // updated until MSB and LSB have been read , Enable Block
                       // Data Update , Set Output Data Rate to 0
  return 1;
}
