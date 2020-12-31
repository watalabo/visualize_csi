#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import io
import math
import cmath
import numpy as np
from PIL import Image
from PIL import ImageDraw


def get_color(val, min, max, palette):
    size = len(palette)
    val = val - min
    max = max - min
    p = val / max
    p = p * (size - 1)
    index = round(p)
    print(index)
    return palette[index]



def make_color_palette():
    palette = []

    # 赤～黄色
    for i in range(256):
        palette.append((255, i, 0))
    
    # 黄～緑
    for i in range(256):
        val = 255 - i
        palette.append((val, 255, 0))

    # 緑～水色
    for i in range(256):
        palette.append((0, 255, i))

    # 水色～青
    for i in range(256):
        val = 255 - i
        palette.append((0, val, 255))

    # 青～黒
    for i in range(256):
        val = 255 - i
        palette.append((0, val, 255))

    # 1280
    palette.reverse()

    return palette


def make_color_palette_val():
    palette = []

    # 赤～黒
    for i in range(256):
        val = 255 - i
        palette.append((val, 0, 0))
    
    # 青～黒
    for i in range(256):
        val = 255 - i
        palette.append((0, 0, i))

    palette.reverse()

    return palette



def make_color_palette_power():
    palette = []

    # 赤～白
    for i in range(256):
        val = 255 - i
        palette.append((255, i, i))    


    for i in range(256):
        val = 255 - i
        palette.append((val, val, 255))    


    # 1280
    palette.reverse()

    return palette


def make_color_palette_angle():
    palette = []

    # 黒～赤
    for i in range(256):
        palette.append((i, 0, 0))
    
    # 赤～白
    for i in range(256):
        palette.append((255, i, i))

    # 白～青
    for i in range(256):
        val = 255 - i
        palette.append((val, val, 255))

    # 青～黒
    for i in range(256):
        palette.append((i, i, 255))

    # 1280
    palette.reverse()

    return palette



def make_image(raw_data, power_data, angle_data):
    line_data = np.arange(256)
    hue = np.tile(line_data, (256,1))
    sat = np.transpose(hue)
    val = np.full_like(hue, 255)

    mat = np.stack([hue, sat, val], 2)

    im = Image.fromarray(np.uint8(mat), 'HSV')
    #im.show()  # 画像を表示する場合
    im_rgb = im.convert('RGB')
    size = im_rgb.size
    print(size)
    for i in range(256):
        r, g, b = im_rgb.getpixel((i, 255))
        print(i)
        print(r, g, b)
    im_rgb.save('out1.png')


def plot_image(figname, raw_data, power_data, angle_data, palette_val, palette, palette_angle):
    img = Image.new("RGB", (5 * 234, 250), (0, 0, 0))
    draw = ImageDraw.Draw(img)


    j = 0
    for items in raw_data:
        i = 0
        for item in items:
            print(item)
            color = get_color(item.real, -1.0, 1.0, palette_val)
            draw.rectangle((i * 5, j * 5, i * 5 + 5, j * 5 + 5), fill=color, width=0)
            i = i + 1
        j = j + 1

    j = 0
    for items in raw_data:
        i = 0
        for item in items:
            print(item)
            color = get_color(item.imag, -1.0, 1.0, palette_val)
            draw.rectangle((i * 5, j * 5 + 50, i * 5 + 5, j * 5 + 5 + 50), fill=color, width=0)
            i = i + 1
        j = j + 1


    j = 0
    for items in power_data:
        print("items")
        print(items)
        i = 0
        for item in items:
            print(item)
            color = get_color(item, 0.0, 1.0, palette)
            draw.rectangle((i * 5, j * 5 + 50 * 2, i * 5 + 5, j * 5 + 5 + 50 * 2), fill=color, width=0)
            i = i + 1
        j = j + 1

    j = 0
    for items in angle_data:
        print("items")
        print(items)
        i = 0
        for item in items:
            print(item)
            color = get_color(item, - math.pi, + math.pi, palette_angle)
            draw.rectangle((i * 5, j * 5 + 50 * 3, i * 5 + 5, j * 5 + 5 + 50 * 3), fill=color, width=0)
            i = i + 1
        j = j + 1

    j = 0
    for items in angle_data:
        print("items")
        print(items)
        i = 0
        for item in items:
            print("diff angle")
            print(item)
            print(item - angle_data[0][i])
            diff = item - angle_data[0][i]
            if diff > math.pi:
                diff = diff - 2 * math.pi
            if diff < - math.pi:
                diff = diff + 2 * math.pi

            color = get_color(diff, - math.pi, + math.pi, palette_angle)
            draw.rectangle((i * 5, j * 5 + 50 * 4, i * 5 + 5, j * 5 + 5 + 50 * 4), fill=color, width=0)
            i = i + 1
        j = j + 1



    img.save(figname)


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
#    print(angle_data)
    return raw_data, power_data, angle_data



parser = argparse.ArgumentParser(description="excel hoge hoge")
parser.add_argument("filename", help="filename hog hoge")
args = parser.parse_args()

palette = make_color_palette_power()
palette_val = make_color_palette_val()
palette_angle = make_color_palette_angle()
ret = get_color(0.25, 0, 1.0, palette)


filename = args.filename
f = open(filename, "r")
line = f.readline()
line = f.readline()
num = 0
while line:
#    print(line)
    a, b, c = process_line(line)
    line = f.readline()
#    make_image(a, b, c)
    figname = "%06d.png" % (num)
    plot_image(figname, a, b, c, palette_val, palette, palette_angle)
    num = num + 1


