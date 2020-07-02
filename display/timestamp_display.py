# Source - https://github.com/jumejume1/raspberry-oled-monitor

# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import requests

from definitions import ROOT_DIR

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from datetime import datetime
import fontawesome as fa
import subprocess



class Display():

    # To toggle blinks
    def toggle(self, blink:bool):
        return (not blink)

    def __init__(self):
        self.ip = "localhost"
        # Raspberry Pi pin configuration:
        RST = None     # on the PiOLED this pin isnt used
        # Note the following are only used with SPI:
        #DC = 23
        #SPI_PORT = 0
        #SPI_DEVICE = 0
    
    
        # 128x32 display with hardware I2C:
        # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
    
        # 128x64 display with hardware I2C:
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
    
        # Note you can change the I2C address by passing an i2c_address parameter like:
        # disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
    
        # Alternatively you can specify an explicit I2C bus number, for example
        # with the 128x32 display you would use:
        # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)
    
        # 128x32 display with hardware SPI:
        # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
    
        # 128x64 display with hardware SPI:
        # disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
    
        # Alternatively you can specify a software SPI implementation by providing
        # digital GPIO pin numbers for all the required display pins.  For example
        # on a Raspberry Pi with the 128x32 display you might use:
        # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)
    
        # Initialize library.
        self.disp.begin()
    
        # Clear display.
        self.disp.clear()
        self.disp.display()
    
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))
    
        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)
    
    def fill(self):
        # Draw a black filled box to clear the image.
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
    
        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        top = padding
        bottom = self.height-padding
        # Move left to right keeping track of the current x position for drawing shapes.
        x = 0
    
    
        # Load default font.
        font = ImageFont.load_default()
    
        # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
        # Some other nice fonts to try: http://www.dafont.com/bitmap.php
       
        font = ImageFont.truetype(f'{ROOT_DIR}/display/Montserrat-Regular.ttf', 20)
        font_icon = ImageFont.truetype(f'{ROOT_DIR}/display/fontawesome-webfont.ttf', 18)
        font_text_small = ImageFont.truetype(f'{ROOT_DIR}/display/Montserrat-Medium.ttf', 8)
        font_live_date = ImageFont.truetype(f'{ROOT_DIR}/display/Montserrat-Medium.ttf', 10)
    
        # Alternate blink so that we know the display is not frozen
        indoor_blink = True
        outdoor_blink = False
        while True:
    
            # Draw a black filled box to clear the image.
            self.draw.rectangle((0,0,self.width, self.height), outline=0, fill=0)
            #draw.line([(width/2,10),(width/2, height)], fill=255)
            # Icons
            icon_y = top
            if indoor_blink: 
                self.draw.text((x+15, icon_y),   str(fa.icons['pagelines']), font=font_icon, fill=255)
            if outdoor_blink:
                self.draw.text((x+90, icon_y),   str(fa.icons['pagelines']),  font=font_icon, fill=255)
            
            indoor_blink = self.toggle(indoor_blink)
            outdoor_blink = self.toggle(outdoor_blink)
    
            # Location
            time_y = top +18 
            self.draw.text((x+ 75, time_y), str("Indoor"), font=font_text_small, fill=255)
            self.draw.text((x+10, time_y), str("Outdoor"), font=font_text_small, fill=255)
            
            # Count
            count_y = top + 25
            try:
                resp = requests.get("http://"+self.ip+"/stats").json()
                self.draw.text((x+15, count_y), str(f'{resp["Motor Outdoor"]["today"]}/{resp["Motor Outdoor"]["total"]}'),  font=font, fill=255)
                self.draw.text((x+70, count_y), str(f'{resp["Motor Indoor"]["today"]}/{resp["Motor Indoor"]["total"]}'),  font=font, fill=255)
            except Exception:
                self.draw.text((x+1, count_y), str("0/0"),  font=font, fill=255)
                self.draw.text((x+70, count_y),    str("0/0"),  font=font, fill=255)
            
            # Live date
            self.draw.text((x+10,top + 56), str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), font = font_live_date, fill=255)
            
            # Display image.
            self.disp.image(self.image)
            self.disp.display()
            time.sleep(1)
    

