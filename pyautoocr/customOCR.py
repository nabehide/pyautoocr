# -*- coding:utf-8 -*-

import pyocr
import pyocr.builders
import sys
from PIL import Image
import pyautogui
import cv2
import numpy as np

from pyautoocr import customGCV

tools = pyocr.get_available_tools()
builder = pyocr.builders.WordBoxBuilder(tesseract_layout=6)


def getPositionFromText(strings,
                        up=0, down=899, left=700, right=1399,
                        nameOutputImage="output.png", key=None,
                        flagDebug=False, flagSavePicture=False, flagMouseMove=False, flagGCV=True):

    nameImage = "screenshot.png"
    result = []

    __checkOCR(tools)

    if flagMouseMove:
        pyautogui.moveTo([750, 40])

    image = pyautogui.screenshot()
    image = np.asarray(image)
    image = image[up:down, left:right]
    cv2.imwrite(nameImage, image)

    if flagGCV:
        result = customGCV.searchStrings(strings, nameImage, flagDebug=flagDebug, key=key)
    else:
        tool = tools[1]
        res = tool.image_to_string(Image.open(nameImage),
                                   lang="jpn",
                                   builder=builder)

        out = cv2.imread(nameImage)
        # out = cv2.imread(image)
        for d in res:
            cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), 2) 
            flagFind = True
            for s in strings:
                if s not in d.content:
                    flagFind = False
                    break
            if flagFind:
                result.append(d.position)
            if flagDebug:
                print(d.content)
                print(d.position)
        result = np.asarray(result)

        if flagSavePicture:
            # cv2.imwrite("screenshot.png", image)
            cv2.imwrite(nameOutputImage, out)

    position = []
    for i in range(len(result)):
        position.append([(result[i][0][0] + result[i][1][0]) / 2 + left,
                         (result[i][0][1] + result[i][1][1]) / 2 + up])

        # result[i][0][0] += up
        # result[i][0][1] += left
        # result[i][1][0] += up
        # result[i][1][1] += left

    return position


def __checkOCR(tools):
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)


if __name__ == '__main__':
    from private import KEY

    strings = [u'水をまく']
    up = 300
    down = 700
    left = 800
    right = 1399

    result = getPositionFromText(strings=strings, up=up, down=down, left=left, right=right, flagDebug=True, flagSavePicture=True, flagMouseMove=True, key=KEY)
    # result = getPositionFromText(string=string, flagDebug=True, flagSavePicture=True)

