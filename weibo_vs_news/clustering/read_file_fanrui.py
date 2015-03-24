__author__ = 'Kay'
#coding:utf-8

def read_weibo(file_name):
	weibo_dict={}
	try:
		f=file(file_name,'r')
	except IOError:
		raise
	for line in f:
		weiboid,uid,text,hashtag,word_list,followers_count,moodstr,weibo_source=line.strip().split('|**|')
		if hashtag:
			hashtag_list=hashtag.split('|')
		else:
			hashtag_list=[]
		weibo_dict[int(weiboid)]={'uid':int(uid),'text':text,'hashtag':hashtag_list,'word_list':word_list.split('|'),'followers_count':int(followers_count),'mood':int(moodstr),'source':weibo_source}
	f.close()
	return weibo_dict

def read_dict(file_name):
	word_dict=dict()
	try:
		f=open(file_name,'r')
	except IOError:
		raise
	for line in f:
		key,value=line.strip().split(':')
		word_dict[key]=float(value)
	f.close()
	return word_dict

def read_graph(file_name):
	graph=dict()
	try:
		f=open(file_name,'r')
	except IOError:
		raise
	for line in f:
		key1,key2,value=line.strip().split('\t')
		if not key1 in graph:
			graph[key1]=dict()
		graph[key1][key2]=float(value)
		if not key2 in graph:
			graph[key2]=dict()
		graph[key2][key1]=float(value)
	f.close()
	return graph

def read_topic(file_name):
	topic_list=[]
	try:
		f=open(file_name,'r')
	except IOError:
		raise
	for line in f:
		topic=line.strip().split('\t')
		topic_list.append(topic)
	f.close()
	return topic_list
