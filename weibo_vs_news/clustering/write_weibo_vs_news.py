#coding:utf-8
__author__ = 'Kay'

import os
import mysql_handler

# 获得微博和其它数据源的先后顺序标志，例如 w_n_5
def get_weibo_vs_x(con, keyword):
    print "get_weibo_vs_x", keyword
    cur = con.cursor()
    sql = "select * from weibo_vs_news_copy where keyword='%s';" % (keyword)
    cur.execute(sql)
    row = cur.fetchone()
    re = ''
    for i in range(2, 13):
        if i != 13:
            re += (str(row[i]) + '\t')
        else:
            re += str(row[i])
    return re

# 将先后顺序标志写入文件
def write_weibo_vs_x(fi_name, w_fi_name):
    fi = open(fi_name)
    w_fi = open(w_fi_name, 'w')
    con = mysql_handler.get_local_con()
    for line in fi:
        keyword = line.strip()
        re = get_weibo_vs_x(con, keyword)
        w_fi.write(keyword + '\t' + re + '\n')
    w_fi.flush()
    w_fi.close()
    fi.close()

# 实验1：将目录中簇文件写入对应的峰值比较信息
def exp1():
    for fi_name in os.listdir('cluster_3.0'):
        if fi_name.endswith('txt') and not fi_name.endswith('_re.txt'):
            write_weibo_vs_x('cluster_3.0/' + fi_name, 'cluster_3.0/' + fi_name[:-4] + '_re.txt')

# 实验2：统计簇中的是否有峰值的关系
def get_relation_cluster(fi_name):
    print 'get_relation_cluster', fi_name
    fi = open(fi_name)

    count_1 = 0.0
    count_2 = 0.0

    for line in fi:
        print line
        mark = line.strip().split('\t')[10] # 2 6 10 分别是15分钟为粒度的三种来源的index
        if mark == '1':
            count_1 += 1 # 微博在前
        elif mark == '2':
            count_2 += 1 # 新闻在前
    fi.close()
    return count_1, count_2

def exp2():

    w_fi = open('cluster_3.0/w_b_15_result.txt', 'w')

    for fi_name in os.listdir('cluster_3.0'):
        if fi_name.endswith('_re.txt'):
            c1, c2 = get_relation_cluster('cluster_3.0/' + fi_name)
            pro1 = c1 / (c1 + c2)
            pro2 = c2 / (c1 + c2)
            if c1 + c2 > 1:
                w_fi.write(fi_name + '\t' + str(int(c1 + c2)) + '\t'
                           + str(float('%0.2f' % pro1)) + '\t' + str(float('%0.2f' % pro2)) + '\n')
    w_fi.flush()
    w_fi.close()

if __name__ == '__main__':
    exp2()


