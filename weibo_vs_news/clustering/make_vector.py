#coding:utf-8
__author__ = 'Kay'

import os
# import numpy as np

# 判断向量是零向量
def vector_is_zero(vector):
    for v in vector:
        if v != "0":
            return False
    return True

# 将列表按行写入文件
def list2file(li, fi):
    w_file = open(fi, 'a')
    for meta in li:
        w_file.write(meta + "\n")
    w_file.flush()
    w_file.close()

# 制作词表，61300维
def make_word_list(r_dir):
    print "make_word_list() starts."
    word_list = []
    # 遍历目录中的文件名
    count = 0
    for f in os.listdir(r_dir):
        count += 1
        print "count:", count
        file = open(r_dir+"/"+f)
        # 按行读文件
        for line in file:
            word = line.split(" ")[0]
            # 判断列表中是否存在word
            if not word in word_list:
                word_list.append(word)
    # 读文件关闭
    file.close()
    w_file = open('word_list.txt', 'a')
    for word in word_list:
        w_file.write(word+"\n")
    w_file.flush()
    w_file.close()

# 制作词表，1200维
def make_word_list_1200(r_dir):
    print "make_word_list"
    word_list = []
    # 遍历目录中的文件名
    count = 0
    for fi_name in os.listdir(r_dir):
        if not fi_name.endswith('.txt'):
            continue
        count += 1
        print "count:", count
        word_list.append(fi_name[:-4])

    w_file = open('word_list_1200.txt', 'a')
    for word in word_list:
        w_file.write(word+"\n")
    w_file.flush()
    w_file.close()

# 读取词表
def read_word_list(fi_name):
    word_list = []
    f = open(fi_name)
    for line in f:
        word_list.append(line[:-1])
    f.close()
    return word_list

def make_vector(r_dir, w_dir):
    word_list = read_word_list('word_list_1200.txt')
    count = 0
    # 遍历目录中的文件名
    listdir = os.listdir(r_dir)
    for filename in listdir:
        # 判断文件名后缀是否是.txt
        if not filename.endswith(".txt"):
            continue
        count += 1
        print "count:", count, "filename:", filename
        word_vector = ["0"] * len(word_list)
        r_file = open(r_dir + "/" + filename)
        # 取出关键词
        keyword = filename[:-4]
        # 按行读文件
        for line in r_file:
            word_value = line.split(" ")
            word = word_value[0]
            value = word_value[1].strip()
            # 取出相应的值放进向量中
            # print word
            if word in word_list:
                # print "bingo!"
                word_vector[word_list.index(word)] = value
        # 读文件关闭
        r_file.close()

        # 判断是不是零向量
        if vector_is_zero(word_vector):
            continue

        # 将 keyword + " || " + word_vector 写入文件
        w_file = open(w_dir + "/" + filename, "w")
        w_file.write(keyword + " || " + ",".join(word_vector) + "\n")
        w_file.flush()
        w_file.close()

if __name__ == '__main__':
    # make_vector("word2vec", "vector_1200_plus")
    make_word_list_1200('vector_1200')
