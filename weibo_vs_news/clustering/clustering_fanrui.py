__author__ = 'Kay'
#coding:utf-8
import read_file_fanrui

def get_cluster_simi(graph,cluster1,cluster2):
    simi=0
    for key1 in cluster1:
        for key2 in cluster2:
            simi+=graph[key1][key2]
    return simi/float(len(cluster1)*len(cluster2))

def get_max_simi(graph,topic_list):
    if len(topic_list)==1:
        return 0,0,0
    n_topic_list=len(topic_list)
    max_i=0
    max_j=1
    max=get_cluster_simi(graph, topic_list[0], topic_list[1])
    for i in range(n_topic_list):
        for j in range(i+1,n_topic_list):
            cluster1=topic_list[i]
            cluster2=topic_list[j]
            simi=get_cluster_simi(graph,cluster1,cluster2)
            if simi<max:
                max=simi
                max_i=i
                max_j=j
    return (max_i,max_j,max)

def cluster(graph,cluster_threshold):
    word_list=graph.keys()
    topic_list=[[word] for word in word_list]
    i,j,max_simi=get_max_simi(graph,topic_list)
    while max_simi<cluster_threshold:
        cluster1=topic_list[i]
        cluster2=topic_list[j]
        new_cluster=cluster1+cluster2
        topic_list.remove(cluster1)
        try:
            topic_list.remove(cluster2)
        except:
            print i
            print j
            raise
        topic_list.append(new_cluster)
        i,j,max_simi=get_max_simi(graph,topic_list)
#    ret_topic_list=[topic for topic in topic_list if len(topic)>1]
    ret_topic_list = topic_list
    return ret_topic_list

if __name__=='__main__':
    root='/mnt1/fanrui/event/'
    today='id.2014022517'
    topic_list=cluster(read_file_fanrui.read_graph('graphtest.txt'), 50)
    for topic in topic_list:
        print " ".join(topic)
    # out_file.out_topic(topic_list,root+today+'/topic.txt')
