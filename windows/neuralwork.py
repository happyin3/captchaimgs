__author__ = "happyin3"
#coding: utf-8

import numpy as np
import neurolab as nl


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
        #net = nl.load("test.net")

        return net

    def reg_net(self, reg_data):
        net = nl.load("test.net")
        inp = np.array(reg_data)
        out = net.sim(inp)

        return out

