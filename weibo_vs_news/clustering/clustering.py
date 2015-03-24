#coding:utf-8
__author__ = 'Kay'

import make_vector
import read_vector
import sys
import os

# 得到两个簇的相近度，组平均作为相近度
def get_cluster_ave_simi(graph, cluster1, cluster2):
    simi = 0
    for key1 in cluster1:
        for key2 in cluster2:
            if key1 == key2:
                print "Error:两个簇中出现相同关键词。"
                sys.exit()
            simi += graph[key1][key2]

    return simi / float(len(cluster1) * len(cluster2))

# 得到两个簇的相近度，MAX作为相近度
def get_cluster_max_simi(graph, cluster1, cluster2):
    # print "get_cluster_max_simi"
    max_simi = - 0.1

    for key1 in cluster1:
        for key2 in cluster2:

            if key1 == key2:
                print "Error:两个簇中出现相同关键词。"
                sys.exit()

            tmp = graph[key1][key2]
            if tmp > max_simi:
                # print key1, key2, tmp
                max_simi = tmp
    return max_simi

# 得到两个簇的相近度，MIN作为相近度
def get_cluster_min_simi(graph, cluster1, cluster2):
    min_simi = float("inf")
    for key1 in cluster1:
        for key2 in cluster2:
            if key1 == key2:
                print "Error:两个簇中出现相同关键词。"
                sys.exit()

            tmp = graph[key1][key2]
            if tmp < min_simi:
                # print key1, key2, tmp
                min_simi = tmp
    return min_simi

# 得到距离最近的两个簇
def get_max_simi(graph, clusters):

    cnt_clusters = len(clusters)

    max_i = 0
    max_j = 1
    max_simi = get_cluster_max_simi(graph, clusters[0], clusters[1])

    for i in range(cnt_clusters):
        for j in range(i + 1, cnt_clusters):

            tmp_simi = get_cluster_max_simi(graph, clusters[i], clusters[j])

            # print "获得下面两个簇的距离:"
            # show_cluster(clusters[i])
            # show_cluster(clusters[j])
            # print tmp_simi

            # simi越小说明越相似
            if tmp_simi < max_simi:
                max_i = i
                max_j = j
                max_simi = tmp_simi

    return max_i, max_j, max_simi

# 返回两个向量的距离
def get_dist(v1, v2):
    dist = 0.0
    # 两个向量维度不同，不能进行距离计算，返回-1
    if len(v1) != len(v2):
        return -1.0
    else:
        # 遍历向量
        for i in range(len(v1)):
            # # 向量中成对元素相减后平方，再累加
            # if v1 == 0 and v2 == 0:
            #     pass
            # elif v1 == 0 or v2 == 0:
            #     dict += 1
            # else:
            #     pass
            dist += pow(v1[i] - v2[i], 2)
        return dist

# 初始化距离图
def init_dist_graph(dict_word_vector, w_file):
    print "init_dist_graph"
    graph = {}
    keys = []
    count = 0
    fi = open(w_file, "a")
    for key1 in dict_word_vector.keys():
        keys.append(key1)
        count += 1; print "count:", count
        for key2 in dict_word_vector.keys():
            if key1 == key2: # 两个关键词相同，距离为0
                pass
            elif key2 in keys:
                pass
            else:
                dist = get_dist(dict_word_vector[key1], dict_word_vector[key2])
                fi.write(key1 + "\t" + key2 + "\t" + str(dist) + "\n")
    fi.flush()
    fi.close()

    return graph

# 从文件获得距离图
def get_graph(graph_file):
    graph = dict()
    fi = open(graph_file)
    for line in fi:
        key1, key2, value = line.strip().split('\t')
        if key1 not in graph:
            graph[key1] = dict()
        graph[key1][key2] = float(value)

        if key2 not in graph:
            graph[key2] = dict()
        graph[key2][key1] = float(value)
    fi.close()
    return graph


# 初始化簇堆
def init_clusters(list_word):
    print "init_cluster"
    clusters = []
    for w in list_word:
        cluster = [w]
        clusters.append(cluster)
    return clusters

# 合并两个簇，未使用，直接在clustering中实现
def union_cluster(clusters, i, j):
    c1 = clusters.pop(i)
    c2 = clusters.pop(j)
    clusters.append(c1 + c2)
    return clusters

# 凝聚层次聚类
def clustering(graph_file, cluster_threshold):
    # 1.初始化距离图
    graph = get_graph(graph_file)
    # 2.初始化簇堆
    clusters = init_clusters(read_vector.read_keys('vector_1200'))
    # 3.不断迭代，得到相似度最大的两个簇，直到相似度低于门限值或簇堆中只有一个元素
    max_simi = 0
    times = 0
    while max_simi <= cluster_threshold:
        print "```````````````````````````"
        times += 1; print "凝聚次数:", times

        # 簇族中只剩下一个簇，无法凝聚
        if len(clusters) == 1:
            break

        i, j, max_simi = get_max_simi(graph, clusters)
        # 凝聚两个簇

        print "取得距离最小的两个簇，进行凝聚:"
        print max_simi
        # i < j
        c1 = clusters.pop(i)
        c2 = clusters.pop(j - 1)
        show_cluster(c1)
        show_cluster(c2)
        clusters.append(c1 + c2)

    return clusters

# 凝聚层次聚类，已经初始化簇族
def clustering_plus(graph_file, cluster_threshold, clusters):
    # 1.初始化距离图
    graph = get_graph(graph_file)
    # 2.初始化簇堆，参数已经传入
    # 3.不断迭代，得到相似度最大的两个簇，直到相似度低于门限值或簇堆中只有一个元素
    max_simi = 0
    times = 0
    while max_simi <= cluster_threshold:
        print "```````````````````````````"
        times += 1; print "凝聚次数:", times

        # 簇族中只剩下一个簇，无法凝聚
        if len(clusters) == 1:
            break

        i, j, max_simi = get_max_simi(graph, clusters)
        # 凝聚两个簇

        print "取得距离最小的两个簇，进行凝聚:"
        print max_simi
        # i < j
        c1 = clusters.pop(i)
        c2 = clusters.pop(j - 1)
        show_cluster(c1)
        show_cluster(c2)
        clusters.append(c1 + c2)

    return clusters

def show_cluster(cluster):
    print "簇显示:",
    for c in cluster:
        print c,
    print "\n"

# 读取簇族
def read_clusters(r_dir):
    clusters = list()
    for fi_name in os.listdir(r_dir):
        if not fi_name.endswith(".txt"):
            continue
        cluster = list()
        fi = open(r_dir + '/' + fi_name, 'r')
        for line in fi:
            cluster.append(line.strip())
        fi.close()
        clusters.append(cluster)
    return clusters

# 凝聚实验
def exp_1():
    # dict_word_vector = read_vector.read_vector('vector')
    init_clu = read_clusters('cluster_6.0')
    clusters = clustering_plus("graph_1200.txt", 10.0, init_clu)
    clu_count = 0
    for cluster in clusters:
        clu_count += 1; print "簇" + str(clu_count) + ":"
        for word in cluster:
            print word
        make_vector.list2file(cluster, 'cluster_10.0/' + str(clu_count) + '.txt')

# 初始化图，到文件
def init_graph_file(v_dir, graph_fi):
    dict_word_vector = read_vector.read_vector(v_dir)
    init_dist_graph(dict_word_vector, graph_fi)

if __name__ == '__main__':
    # init_graph_file('vector_1200', 'graph_1200.txt')
    exp_1()