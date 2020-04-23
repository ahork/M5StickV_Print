import sensor
import image
import lcd
import time
import sys
import utime
from machine import I2C,UART

from fpioa_manager import fm

#uart initial
fm.register(35, fm.fpioa.UART2_TX, force=True)
fm.register(34, fm.fpioa.UART2_RX, force=True)

uart_Port = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)


clock = time.clock()
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.set_hmirror(1)
sensor.run(1)
sensor.skip_frames(20)

KO = 1
while True:
    clock.tick()
    img = sensor.snapshot()
    data = str(uart_Port.readline())
    colone = 0
    info = [0,0,0,0,0,0,0,0]
    if data[2] == "/" :
        i = -1
        lg = 0
        img2 = sensor.snapshot()
        print(img2.width())
        print(img2.height())
        for y in range(0, 240):
            for x in range(0, 320):
                i = i + 1
                col = img2.get_pixel(x,y)
                if col > 127 :
                    info[i]= 0
                else:
                    info[i]= 1
                if i == 7 :
                    result = info[0] * 128 + info[1] * 64 + info[2] * 32 + info[3] * 16 + info[4] * 8+ info[5] * 4 + info[6] * 2 + info[7] * 1
                    uart_Port.write("{}".format(result))
                    if (x != 320 and y != 10) :
                         uart_Port.write(",")
                    i = -1
                    info = [0,0,0,0,0,0,0,0]
                    colone = colone +1
            lg = lg + 1
            if lg == 10 :
                lg = 0
                utime.sleep(2)
        utime.sleep(10)
    lcd.display(img)
