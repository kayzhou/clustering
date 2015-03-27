#coding:utf-8
__author__ = 'Kay'

import mysql_handler
import json
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# json获得（第一个）最大key
# 实验找到热点事件的最简单的方法 v1.0
def max_index_value(str_json):
    # print 'str_json', str_json
    if str_json == '{}':
        return '-1', 0
    try:
        dict_data = json.loads(str_json)
    except:
        print "json.loads 错误"
        return 'error', 'error'

    dict_keys = dict_data.keys()
    dict_values = dict_data.values()
    max_value = max(dict_data.values())
    max_index = dict_values.index(max_value)

    return dict_keys[max_index], max_value

# 获取字典的均值
def get_dict_mean(dic):
    value_array = np.array(dic.values())
    return np.mean(value_array)

# 获取词典的最大值及其keys
def get_dict_index_max(dict_data):
    dict_keys = dict_data.keys()
    dict_values = dict_data.values()
    max_value = max(dict_data.values())
    max_index = dict_values.index(max_value)

    return dict_keys[max_index], max_value

# get max_index, max_value from dict
def get_max_from_dict(dict_index_value):
    dict_keys = dict_index_value.keys()
    dict_values = dict_index_value.values()
    max_value = max(dict_index_value.values())
    max_index = dict_keys[dict_values.index(max_value)]
    return max_index, max_value

# 计算微博中，每个关键词出现的均值和峰值
def weibo_mean_max():
    fi = open('word_mean_index_max.txt', 'a')
    con = mysql_handler.get_mysql_con()
    cur = con.cursor()
    SQL = "select distinct keyword from keyword_weibo_count_copy;"
    cur.execute(SQL)
    rst = cur.fetchall()
    count = 0
    # 遍历每一个关键词
    for row in rst:
        count += 1
        print "count:", count
        keyword = row[0]
        print keyword
        # 以15分钟为粒度
        SQL = "select count_15 from keyword_weibo_count_copy where keyword='%s'" % (keyword)
        cur.execute(SQL)
        rows_count = cur.fetchall()
        dict_index_value = dict()
        # 遍历这个关键不同日期的数据
        for r in rows_count:
            dict_index_value = dict(dict_index_value, **json.loads(r[0]))

        mean = get_dict_mean(dict_index_value)
        index, max = get_dict_index_max(dict_index_value)
        fi.write(keyword + '\t' + str(mean) + '\t' + str(index) + '\t' + str(max) + '\n')
        fi.flush()
    fi.close()
    con.close()

if __name__ == '__main__':
    weibo_mean_max()