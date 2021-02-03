# MQTT Publishers for the Waveshare Sense HAT B for Raspberry Pi

This project attempts to turn the rather crude sensor readers provided as
example code with the Waveshare Sense HAT into an MQTT publisher using the
mosquitto library.

This publisher should read out the slowly reacting sensors about once per
second and the accelerometer and gyroscope at a much faster rate, collecting
samples and sending them in bulk once each second.

Up to now, the demo code using the bcm2835 library has been cleaned up and
separated so that each block can be used like a library.

References:

http://www.airspayce.com/mikem/bcm2835/index.html

https://github.com/matthiasbock/bcm2835

https://www.waveshare.com/wiki/Sense_HAT_(B)
