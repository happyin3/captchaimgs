_author__ = "happyin3"
#coding: utf-8

import time
from PIL import Image

class ExtractImage(object):
    def __init__(self, image=None):
        self.image = image

    def horizontal_draw_line(self, flag, kind_flag):
        oriimage = self.image
        img_rows = oriimage.size[1]
        img_cows = oriimage.size[0]
        
        if kind_flag == 1:
            if flag == 1:
                start_line = 0
                end_line = img_cows / 2
            else:
                start_line = img_cows / 2
                end_line = img_cows
        else:
            start_line = 0
            end_line = img_cows

        list_draw_line = []
        for i in xrange(img_rows):
            pixel_flag = img_rows
            for j in xrange(start_line, end_line):
                check_pixel = oriimage.getpixel((j, i))
                if check_pixel < 240:
                    pixel_flag = i
                    break
            if pixel_flag == img_rows:
                list_draw_line.append([i, start_line, end_line])
        return list_draw_line

    def horizontal_merger_line(self, list_draw_line):
        list_split_line = []
        for i in xrange(len(list_draw_line)):
            if i != len(list_draw_line) - 1:
                temp_line = list_draw_line[i][0]
                temp_line_down = list_draw_line[i+1][0]
                start_line = list_draw_line[i][1]
                end_line = list_draw_line[i][2]
                if temp_line_down - temp_line < 100:
                    for j in xrange(temp_line, temp_line_down+1):
                        for k in xrange(start_line, end_line):
                            self.image.putpixel((k, j), 0)
                else:
                    list_split_line.append([temp_line, temp_line_down])
        return list_split_line

    def vertical_line(self, flag, kind_flag, list_split_line):
        oriimage = self.image
        img_cows = oriimage.size[0]

        if kind_flag == 1:
            if flag == 1:
                start_line = 0
                end_line = img_cows / 2
            else:
                start_line = img_cows / 2
                end_line = img_cows
        else:
            start_line = 0
            end_line = img_cows

        list_draw_line = []
        list_extract_image = []
        for line in list_split_line:
            row_up = line[0]
            row_down = line[1]
            cow_left = start_line
            cow_right = end_line
            for j in xrange(start_line, end_line):
                pixel_flag = end_line
                for i in xrange(row_up+1, row_down):
                    check_pixel = oriimage.getpixel((j, i))
                    if check_pixel < 240:
                        pixel_flag = j
                        break
                    self.image.putpixel((j, i), 0)
                if pixel_flag != end_line:
                    cow_left = pixel_flag
                    break

            for j in xrange(end_line-1, start_line-1, -1):
                pixel_flag = end_line
                for i in xrange(row_up+1, row_down):
                    check_pixel = oriimage.getpixel((j, i)) 
                    if check_pixel < 240:
                        pixel_flag = j
                        break
                    self.image.putpixel((j, i), 0)
                if pixel_flag != end_line:
                    cow_right = pixel_flag
                    break    
            
            #截取图片
            extract_img = self.image.crop((cow_left, row_up, cow_right, row_down))
            save_path = "static/images/extractimg/" + time.ctime() + ".jpg"
            save_path_temp = "../%s" % save_path
            extract_img.save(save_path_temp)
            time.sleep(1)
            list_extract_image.append([extract_img, save_path])
        return list_extract_image

    #合并图片
    def image_resize(self, image, size=(0, 0)):
        #调整图片大小
        try:
            if image.mode not in ("L", "RGB"):
                image = image.convert("RGB")
            image = image.resize(size)
        except Exception, e:
            pass
        return image

    def image_merge(self, list_extract_image, restriction_max_width=None, restriction_max_height=None):
        max_width = 0
        total_height = 0

        #计算合成后图片的宽度和高度
        for i in xrange(len(list_extract_image)):
            image = list_extract_image[i]
            width, height = image.size
            if width > max_width:
                max_width = width
            total_height += height
            total_height += 1

        #产生一张图片
        new_img = Image.new('RGB', (max_width, total_height), 255)
        #合并
        x = y = 0
        for i in xrange(len(list_extract_image)):
            image = list_extract_image[i]
            width, height = image.size
            new_img.paste(image, (x, y))
            y += height
            y += 1

        if restriction_max_width and max_width >= restriction_max_width:
            #宽度超过限制，等比例缩小
            ratio = restriction_max_height / float(max_width)
            max_width = restriction_max_width
            total_height = int(total_height * ratio)
            new_img = image_resize(new_img, size=(max_width, total_height))
    
        if restriction_max_height and total_height >= restriction_max_height:
            #高度超过限制，等比例缩小
            ratio = restriction_max_height / float(total_height)
            max_width = int(max_width * ratio)
            total_height = restriction_max_height
            new_img = image_resize(new_img, size(max_width, total_height))
        
        #保存图片
        save_path = "static/images/mergeimg/" + time.ctime() + ".jpg"
        save_path_temp = "../%s" % save_path
        new_img.save(save_path_temp)
        
        return save_path

    def main(self):
        #左边扫描
        left_list_draw_line = self.horizontal_draw_line(1, 1)
        #左边合并
        left_list_split_line = self.horizontal_merger_line(left_list_draw_line)
        #右边扫描
        right_list_draw_line = self.horizontal_draw_line(2, 1)
        #右边合并
        right_list_split_line = self.horizontal_merger_line(right_list_draw_line)

        #纵向扫描，左
        left_list_extract_image = self.vertical_line(1, 1, left_list_split_line)
        #纵向扫描，右
        right_list_extract_image = self.vertical_line(2, 1, right_list_split_line)
        
        #合并图片
        list_extract_image = []
        list_extract_image_path = []
        for each_extract_image in left_list_extract_image:
            list_extract_image.append(each_extract_image[0])
            list_extract_image_path.append(each_extract_image[1])

        for each_extract_image in right_list_extract_image:
            list_extract_image.append(each_extract_image[0])
            list_extract_image_path.append(each_extract_image[1])
        
        merge_save_path = ""
        if len(list_extract_image):
            merge_save_path = self.image_merge(list_extract_image)

        #保存中间处理图片
        deal_save_path = "static/images/dealimg/" + time.ctime() + ".jpg"
        deal_save_path_temp = "../%s" % deal_save_path
        self.image.save(deal_save_path_temp)

        list_save_path = []
        list_save_path.append([deal_save_path, merge_save_path, list_extract_image_path])

        return list_save_path 

