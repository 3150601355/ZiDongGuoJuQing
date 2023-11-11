# 一定要先装好轮子哦
#                   -- 作者：mihu

import cv2                              # pip install opencv-python
import numpy                            # pip install numpy
from PIL import ImageGrab               # pip install pillow
import sys, time, ctypes                # python自带 不用安装
from random import random               # python自带 不用安装

img_templ = cv2.imread('play_button.jpg' ) #加载模板图片
THRESHOLD = 0.97


def mainLoop():
    #截图
    img_src = ImageGrab.grab( bbox=(80, 45, 110, 85) ) # x1, y1, x2, y2
    # img_src.save("capture.jpg") # for debug
    img_src = cv2.cvtColor(numpy.asarray(img_src), cv2.COLOR_RGB2BGR)

    #模板匹配
    result = cv2.matchTemplate(img_src, img_templ, cv2.TM_CCOEFF_NORMED)
    min_max = cv2.minMaxLoc(result)  #计算匹配度
    print('result.min_max:', min_max)

    # 如果匹配度很高，则认为找到菱形，于是模拟鼠标单击
    if min_max[1] > THRESHOLD :
        print('处于对话状态，模拟鼠标单击')
        ctypes.windll.user32.mouse_event(2)
        time.sleep(0.05 + 0.1 * random())
        ctypes.windll.user32.mouse_event(4)

    
if __name__ == '__main__':
    # 判断当前进程是否以管理员权限运行
    if ctypes.windll.shell32.IsUserAnAdmin() :
        print('当前已是管理员权限')
        while True:
            mainLoop()
            time.sleep(0.3 + 0.2 * random())
    else:
        print('当前不是管理员权限，以管理员权限启动新进程...')
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)


