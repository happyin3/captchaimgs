__author__ = "happyin3"
#coding: utf-8

import urllib
import time
from PIL import Image
import numpy as np
import neurolab as nl

#验证码识别
class CodeClass(object):
    def __init__(self, db):
        self.db = db

    #下载验证码，构建训练集
    def download(self, number):
        #读取数据集configini
        results = self.db.configini.find({"kind": "code", "onflag": 1}, {"_id": 0, "downurl"})
        down_url = results["downurl"]
        list_save_path = []
        for i in xrange(number):
            save_path = "static/images/downcode/" + time.ctime() + ".png"
            save_path_temp = "../%s" % save_path
            try:
                urllib.urlretrieve(down_url, save_path_temp)
                list_save_path.append(save_path)
            except:
                pass
            
            time.sleep(1)
        
        #存入数据集downcode
        for save_path in list_save_path:
            try:
                self.db.downcode.insert({"codepath": save_path, "dealflag": 0, "splitflag": 0, "time": time.ctime()})
            except: pass

        return

    #更新验证码明文
    def update_plain(self, path):
        from puloperation import PulOperation
        operation = PulOperation()
        plain_text = operation.read_file(path)

        trans_rules = "0123456789abcdef"
        all_plain_text = []
        for text in plain_text:
            each_plain_text = []
            for each_text in text:
                index = trans_rules.find(each_text)
                each_plain_text.append(index)
            all_plain_text.append(each_plain_text)

        #读取数据聚downcode，获取所有验证码路径
        results = self.db.downcode.find({}, {"_id": 0, "codepath": 1})
        if results:
            for code_path, each_text in zip(results, all_plain_text)
                code_path_temp = code_path["codepath"]
                #更新数据集downcode，更新验证码明文
                try:
                    self.db.downcode.update({"codepath": code_path_temp}, {"$set": {"text": each_text}})
                except: pass 

        return
        
    #预处理验证码
    def deal_code(self):
        #读取数据集downcode，获取验证码路径
        code_handler = CodeHandler()
        all_down_code = self.db.downcode.find({"dealflag": 0}, {"_id": 0, "codepath": 1})
        if all_down_code:
            for code_path in all_down_code:
                code_path_temp = code_path["codepath"]
                #预处理图片
                code_path_temps = "../%s" % code_path_temp
                image = Image.open(code_path_temp)
                save_path = code_handler.main_deal_image(image)
                if len(save_path):
                    #存入数据库dealcode，验证码路径和验证码处理后路径
                    exist_result = self.db.dealcode.find_one({"codepath": code_path_temp})
                    if not exist_result:
                        try:
                            self.db.dealcode.insert({"codepath": code_path_temp, "dealpath": save_path, "time": time.ctime()})
                            self.db.downcode.update({"codepath": code_path_temp}, {"$set": {"dealflag": 1}})
                        except:pass
                time.sleep(1)

        return

    #分割验证码
    def split_code(self):
        #读取数据集dealcode，获取处理验证码图片路径
        code_handler = CodeHandler()
        all_code_path = self.db.downcode.find({"dealflag": 1, "splitflag": 0}, {"_id": 0, "codepath": 1})
        if all_code_path:
            all_deal_path = []
            all_code_paths = []
            for each_code in all_code_path:
                each_code_path = each_code["codepath"]
                all_code_paths.append(each_code_path)
                #读取数据集dealcode，获取处理图片路径
                each_deal_path = self.db.dealcode.find_one({"codepath": each_code_path}, {"_id": 0, "dealpath": 1})
                if each_deal_path:
                    all_deal_path.append(each_deal_path["dealpath"])
            
            for each_deal_path, each_code_path in zip(all_deal_path, all_code_paths):
                each_deal_path_temp = "../%s" % each_deal_path
                list_split_image_path = deal_image.main_split_image(each_deal_path_temp)
                if len(list_split_image_path):
                    #存入数据集splitcode，验证码路径和分割图片路径
                    exist_result = self.db.splitcode.find_one({"codepath": each_code_path})
                    if not exist_result:
                        try:
                            self.db.splitcode.insert({"codepath": each_code_path, "splitpath": list_split_image_path, "time": time.ctime()})
                            #更新数据集downcode，分割标志为1
                            self.db.downcode.update({"codepath": each_code_path}, {"$set": {"splitflag": 1}})
                        except: pass
                    else:
                        try:
                            self.db.downcode.update({"codepath": each_code_path}, {"$set": {"splitflag": 0}})
                        except: pass
        return

    #训练
    def train_net(self):
        #读取数据集splitcode，获取分割图片路径
        all_split_path = self.db.splitcode.find({}, {"_id": 0})
        if all_split_path:
            list_code_path = []
            list_split_path = []
            for each_code in all_split_path:
                list_code_path.append(each_code["codepath"])
                for each_split_path in each_code["splitpath"]:
                    list_split_path.append(each_split_path)

            #读取数据集downcode，获取验证码明码text
            list_text_num = []
            for each_code in list_code_path:
                results = self.db.downcode.find_one({"codepath": each_code}, {"_id": 0, "text": 1})
                if results:
                    for each in results["text"]:
                        each = each * 1.0 / 100
                        each_text = []
                        each_text.append(each)
                        list_text_num.append(each_text)
            
            #生成输入数据
            list_train_input_data = []
            for each_code in list_split_path:
                each_code_temp = "../%s" % each_code
                image = Image.open(each_code_temp)
                each_train_input_data = []
                for x in xrange(image.size[1]):
                    for y in xrange(image.size[0]):
                        if image.getpixel((y, x)):
                            each_train_input_data.append(0)
                        else:
                            each_train_input_data.append(1)
                list_train_input_data.append(each_train_input_data)

            #生成目标数据
            list_train_output_data = list_text_num
            
            #开始训练
            net_size = [10, 1]     
            neural = NeuralWork()
            neural = neural.train_net(list_train_input_data, list_train_output_data, net_size)

        return

    def main(self):
        print "download"
        self.download(50)
        print "updateplain"
        self.update_plain("plaintxt.txt")
        print "dealcode"
        self.deal_code()
        print "splitcode"
        self.split_code()
        print "trainnet"
        self.train_net()
 
#验证码处理
class CodeHandler(object):
    def __init__(self):
        pass

    def binary_image(self, image:
        ori_image = image
        temp_image = ori_image

        temp_image = temp_image.convert("L")

        #转成黑色
        img_height = temp_image.size[1]
        img_width = temp_image.size[2]
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
        list_size = [3, 5, 3]
        for i in list_size:
            j = i / 2
            for x in xrange(j, img_height-j):
                for y in xrange(j, img_width-j):
                    if temp_image.getpixel((y, x)) != 255:
                        sum_count = 0
                        for nx in xrange(x-j, x-j+i):
                            for ny in xrange(y-j, y-j+i):
                                sum_count = sum_count + temp_image.getpixel((ny, nx))
                        if (sum_count == (i * i - j - 1) * 255 or sum_count == (i * i - j) * 255) and i != 2:
                            deal_image.putpixel((y, x), 255)
                        elif sum_count == (i * i -j) * 255 and i == 2:
                            deal_image.putpixel((y, x), 255) 
            temp_image = deal_image.copy()

        '''
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
        '''

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

    def main_deal_image(self, image):
        image = self.binary_image(image)
        image = self.del_white(image)
         
        save_path = "static/images/dealcode/" + time.ctime() + ".png"
        save_path_temp = "../%s" % save_path
        image.save(save_path_temp)
        return save_path
 
    def main_split_image(self, image):
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

    def main_deal_split(self, image):
        image = self.binary_image(image)
        image = self.del_white(image)
        
        #分割图片
        list_split_image = self.split_image(image)
        
        return list_split_image 


#神经网络
class NeuralWork(object):
    def __init__(self):
        self.goal = 0.001

    def train_net(self, input_data, output_data, net_size):
        inp = np.array(input_data)
        tar = np.array(output_data)

        #归一化
        #normf = nl.tool.Norm(tar)
        #norm_target = normf(tar)

        #print norm_target

        net = nl.net.newff([[0, 1]] * 150, net_size)
        net.trainf = nl.train.train_bfgs
        try:
            error = net.train(inp, tar, show=1, goal=self.goal)
        except Exception, e:
            print e

        net.save("test.net")

        return net

    def reg_net(self, reg_data):
        net = nl.load("test.net")
        inp = np.array(reg_data)
        out = net.sim(inp)

        return out
