#coding:utf-8
__author__ = 'Kay'

import os

def get_word_vector(str_fi):
    # print str_fi
    word_vector = str_fi[:-1].split(" || ")
    word = word_vector[0]
    str_vector = word_vector[1].split(",")
    vector = []
    for s in str_vector:
        vector.append(float(s)) # 已将向量中的值转换为float
    return word, vector

def read_vector(r_dir):
    print "read_vector"
    dict_vector = {}
    for fi_name in os.listdir(r_dir):
        if not fi_name.endswith(".txt"):
            continue
        fi = open(r_dir + '/' + fi_name, 'r')
        word, vector = get_word_vector(fi.read())
        fi.close()
        # print word
        # count = 0
        # for v in vector:
        #     if v != 0.0:
        #         count += 1; print "count:", count
        #         print v

        dict_vector[word] = vector
    return dict_vector

def read_keys(r_dir):
    print "read_keys"
    keys = list()
    for fi_name in os.listdir(r_dir):
        if not fi_name.endswith(".txt"):
            continue
        keys.append(fi_name[:-4])
    return keys

if __name__ == '__main__':
    read_vector("test")
