uthor__ = 'happyin3'
#coding: utf-8

import time

from PIL import Image
from PIL import ImageFilter

class DealImage(object):
    def __init__(self):
        pass

    def binary_image(self, image_path):
        ori_image = Image.open(image_path)
        temp_image = ori_image

        temp_image = temp_image.convert("L")
        #temp_image = temp_image.convert("1")

        #转成黑色
        img_height = temp_image.size[1]
        img_width = temp_image.size[0]
        for x in xrange(0, img_height):
            for y in xrange(0, img_width):
                if temp_image.getpixel((y, x)) != 255:
                    temp_image.putpixel((y, x), 0)
                if y == 0 or y == img_width-1:
                    temp_image.putpixel((y, x), 255)
                elif x == 0 or x == img_height-1:
                    temp_image.putpixel((y, x), 255)

        deal_image = temp_image.copy()

        #3*3去噪
        list_size = [3, 5]
        for i in list_size:
            j = i / 2
            for x in xrange(j, img_height-j):
                for y in xrange(j, img_width-j):
                    if temp_image.getpixel((y, x)) != 255:
                        sum_count = 0
                        for nx in xrange(x-j, x-j+i):
                            for ny in xrange(y-j, y-j+i):
                                sum_count = sum_count + temp_image.getpixel((ny, nx))
                        if sum_count == (i * i - j - 1) * 255 or sum_count == (i * i - j) * 255:
                            deal_image.putpixel((y, x), 255)
            temp_image = deal_image.copy()

        temp_image = deal_image.copy()
        list_size = [3]
        for i in list_size:
            j = i / 2
            for x in xrange(j, img_height-j):
                for y in xrange(j, img_width-j):
                    if temp_image.getpixel((y, x)) != 255:
                        sum_count = 0
                        for nx in xrange(x-j, x-j+i):
                            for ny in xrange(y-j, y-j+i):
                                sum_count = sum_count + temp_image.getpixel((ny, nx))
                        if sum_count == (i * i - j) * 255:
                            deal_image.putpixel((y, x), 255)

        return deal_image

    def split_image(self, image):
        origin_image = image
        temp_image = origin_image

        img_height = temp_image.size[1]
        img_width = temp_image.size[0]

        #分割图片，分三个区域查找分割线
        count_flag = 4
        list_split_image = []
        for i in xrange(count_flag, 0, -1):
            img_width = temp_image.size[0]
            img_height = temp_image.size[1]
            img_width_one = img_width / i / 2 * 1
            img_width_two = img_width / i / 2 * 3
            for j in xrange(img_width_one, img_width_two):
                pixel_flag = img_width
                for k in xrange(0, img_height):
                    if temp_image.getpixel((j, k)) != 255:
                        pixel_flag = j
                        break
                if pixel_flag == img_width:
                    split_image = temp_image.crop((0, 0, j+1, img_height))
                    split_image = split_image.resize((10, 15))
                    list_split_image.append(split_image)

                    temp_image = temp_image.crop((j+1, 0, img_width, img_height))
                    temp_image = self.del_white_left(temp_image)
                    break

        return list_split_image

    def del_white_left(self, image):
        temp_image = image
        img_height = image.size[1]
        img_width = image.size[0]

        flag = -1
        left_flag = 0
        for y in xrange(0, img_width):
            for x in xrange(0, img_height):
                if temp_image.getpixel((y, x)) != 255:
                    flag = y
                    break

            if flag != -1 and y != 0:
                left_flag = y -1
                break

        split_image = image.crop((left_flag, 0, img_width, img_height))

        return split_image

    def del_white(self, image):
        temp_image = image
        img_height = image.size[1]
        img_width = image.size[0]

        #去上下空白
        up_flag = 0
        flag = -1
        for x in xrange(0, img_height):
            for y in xrange(0, img_width):
                if temp_image.getpixel((y, x)) != 255:
                    flag = y
                    break
            if flag != -1 and x != 0:
                up_flag = x - 1
                break

        flag = -1
        down_flag = img_height - 1
        for x in xrange(img_height-1, -1, -1):
            for y in xrange(0, img_width):
                if temp_image.getpixel((y, x)) != 255:
                    flag = y
                    break
            if flag != -1 and x != img_height - 1:
                down_flag = x + 1
                break

        #去左右空白
        flag = -1
        left_flag = 0
        for y in xrange(0, img_width):
            for x in xrange(0, img_height):
                if temp_image.getpixel((y, x)) != 255:
                    flag = y
                    break

            if flag != -1 and y != 0:
                left_flag = y - 1
                break

        flag = -1
        right_flag = img_width - 1
        for y in xrange(img_width-1, -1, -1):
            for x in xrange(0, img_height):
                if temp_image.getpixel((y, x)) != 255:
                    flag = y
                    break

            if flag != -1 and y != img_width - 1:
                right_flag = y + 1
                break

        #print left_flag, up_flag, right_flag, down_flag
        split_image = image.crop((left_flag, up_flag, right_flag+1, down_flag+1))

        return split_image

    def main_deal_image(self, image_path):
        image = self.binary_image(image_path)
        image = self.del_white(image)
         
        save_path = "static/images/dealcode/" + time.ctime() + ".png"
        save_path_temp = "../%s" % save_path
        image.save(save_path_temp)
        return save_path
 
    def main_split_image(self, image_path):
        image = Image.open(image_path)
        list_split_image = self.split_image(image)

        #保存图片
        list_split_image_path = []
        if len(list_split_image) == 4:
            for each_image in list_split_image:
                save_path = "static/images/splitcode/" + time.ctime() + ".png"
                save_path_temp = "../%s" % save_path
                each_image.save(save_path_temp)
                list_split_image_path.append(save_path) 
                time.sleep(1)
        return list_split_image_path

    def main_deal_split(self, image_path):
        image = self.binary_image(image_path)
        image = self.del_white(image)
        
        #分割图片
        list_split_image = self.split_image(image)
        
        return list_split_image
            

















