from microbit import *
import radio
radio.config(group=1)
radio.on()


# 加速度を取得し、定数をかける事でプログラム内での移動距離を求める
def get_xy():
    y = accelerometer.get_y() * accelerometer_sensitivity  #y方向
    x = accelerometer.get_x() * accelerometer_sensitivity  #x方向
    return int(max(-1, min(x, 1))), int(max(-1, min(y, 1)))  #値返却


accelerometer_sensitivity = 1 / 300
while True:
    if button_a.was_pressed():
        radio.send('A\n')
        display.show('A')
        sleep(300)
    elif button_b.was_pressed():
        radio.send('B\n')
        display.show('B')
        sleep(300)
    else:
        x, y = get_xy()
        radio.send('XY,' + str(x) + ',' + str(y) + '\n')
        sleep(1000)
        display.clear()
