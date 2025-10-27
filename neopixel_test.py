#-------------------------------------------------------
# neopixel_test.py
# A test to control NeoPixel rings with 12 LEDs
# (c) 2025 @RR_Inyo
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php
#-------------------------------------------------------

import time
import pigpio

class NeoPixel:
    # Class variables
    __SPI_CHANNEL   = 0
    __BAUD_RATE     = 2500000
    __SPI_MODE      = 3
    __CODE_0        = 0b10000000
    __CODE_1        = 0b11100000

    # Constructor
    def __init__(self, pi):
        self.__pi = pi

    # Destructor
    def __del__(self):
        self.__pi.stop()

    # Send to one LED
    def singleRGB(self, r, g, b):
        # Create frame data
        frame = []

        # Green
        for i in range(8):
            frame.append(NeoPixel.__CODE_1 if g & (0b10000000 >> i) != 0 else NeoPixel.__CODE_0)

        # Red
        for i in range(8):
            frame.append(NeoPixel.__CODE_1 if r & (0b10000000 >> i) != 0 else NeoPixel.__CODE_0)

        # Blue
        for i in range(8):
            frame.append(NeoPixel.__CODE_1 if b & (0b10000000 >> i) != 0 else NeoPixel.__CODE_0)

        # Send to SPI (MOSI)
        self.__h = self.__pi.spi_open(0, NeoPixel.__BAUD_RATE, NeoPixel.__SPI_MODE)
        self.__pi.spi_write(self.__h, frame)
        self.__pi.spi_close(self.__h)
        time.sleep(0.001)

    def multiRGB(self, colors):
        # Create frame data
        frame = []

        for color in colors:
            # Green
            for i in range(8):
                frame.append(NeoPixel.__CODE_1 if color[1] & (0b10000000 >> i) != 0 else NeoPixel.__CODE_0)

            # Red
            for i in range(8):
                frame.append(NeoPixel.__CODE_1 if color[0] & (0b10000000 >> i) != 0 else NeoPixel.__CODE_0)

            # Blue
            for i in range(8):
                frame.append(NeoPixel.__CODE_1 if color[2] & (0b10000000 >> i) != 0 else NeoPixel.__CODE_0)

        # Send to SPI (MOSI)
        self.__h = self.__pi.spi_open(0, NeoPixel.__BAUD_RATE, NeoPixel.__SPI_MODE)
        self.__pi.spi_write(self.__h, frame)
        self.__pi.spi_close(self.__h)
        time.sleep(0.001)

    def turnOff(self, num):
        dark = [[0, 0, 0]] * num
        self.multiRGB(dark)

# Test bench
if __name__ == '__main__':

    # Triangular wave
    def triangle(u):
        if u < 4:
            y = u
        else:
            y = 8 - u if u <= 8 else 0

        return y

    # Get pigpio handle
    pi = pigpio.pi()

    # Get NeoPixel handle
    neopixel = NeoPixel(pi)

    # Create color pattern
    colors = []
    for i in range(12):
        colors.append([triangle(i) * 4, triangle((i + 4) % 12) * 4, triangle((i + 8) % 12) * 4])

try:

    # Send to 12-LED ring and rotating colors
    for i in range(1000):
        neopixel.multiRGB(colors)
        colors = [colors[-1]] + colors[:-1]
        time.sleep(0.5 - i / 2000)

    # End test
    neopixel.turnOff(12)
    pi.stop()

except:
    # Close pigpio
    neopixel.turnOff(12)
    pi.stop()
