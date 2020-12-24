#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import io
import math
import cmath
import numpy as np
from PIL import Image

def make_image(raw_data, power_data, angle_data):
    line_data = np.arange(256)
    hue = np.tile(line_data, (256,1))
    sat = np.transpose(hue)
    val = np.full_like(hue, 255)

    mat = np.stack([hue, sat, val], 2)

    im = Image.fromarray(np.uint8(mat), 'HSV')
    #im.show()  # 画像を表示する場合
    im_rgb = im.convert('RGB')
    im_rgb.save('out1.png')




def process_line(line):
    index = line.find("\"") + 1
    line = line[index:len(line) - 2]
    items = eval(line)
#    print(items)
    raw_data = []
    power_data = []
    angle_data = []
    for j in range(9):
        raw_data.append([])
        power_data.append([])
        angle_data.append([])
    for i in range(234):
        for j in range(9):
            val = items[j + i * 9]
            raw_data[j].append(val)
            power_data[j].append(abs(val))
            angle_data[j].append(cmath.phase(val))
    print(angle_data)
    return raw_data, power_data, angle_data


parser = argparse.ArgumentParser(description="excel hoge hoge")
parser.add_argument("filename", help="filename hog hoge")
args = parser.parse_args()
filename = args.filename
f = open(filename, "r")
line = f.readline()
line = f.readline()
while line:
#    print(line)
    a, b, c = process_line(line)
    line = f.readline()
    make_image(a, b, c)
    exit(1)


