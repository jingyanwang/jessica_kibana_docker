###########jessica_es.py###########
import os
import re
import csv
import time
import hashlib 
from elasticsearch import *

def start_es(
	es_path = "/jessica/elasticsearch-6.7.1",
	es_port_number = "9466"):
	'''
	check if es service is already running
	if yes, return the session
	'''
	if os.system(u"""
		curl -XPUT -H "Content-Type: application/json" http://localhost:%s/_cluster/settings -d '{ "transient": { "cluster.routing.allocation.disk.threshold_enabled": false } }'
		curl -XPUT -H "Content-Type: application/json" http://localhost:%s/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'
		"""%(es_port_number,
			es_port_number
			)) == 0:
		return Elasticsearch([{'host':'localhost','port':int(es_port_number)}])
	###
	'''
	if not running, start the service
	firstly overwrit the configuration file
	'''
	os.system(u"""
	rm %s/config/elasticsearch.yml
	echo "transport.host: localhost " > %s/config/elasticsearch.yml
	echo "transport.tcp.port: 9300 " >> %s/config/elasticsearch.yml
	echo "http.port: %s" >> %s/config/elasticsearch.yml
	echo "network.host: 0.0.0.0" >> %s/config/elasticsearch.yml
	"""%(es_path,
		es_path,
		es_path,
		es_port_number,
		es_path,
		es_path))
	'''
	the start the docker service
	'''
	os.system(u"""
		%s/bin/elasticsearch &
		"""%(es_path))
	'''
	keeps checking if es is up, if up return the session
	otherwise keeps checking, until 100K times
	'''
	try_time = 0
	while(try_time <= 100):
		try_time += 1
		if os.system(u"""
		curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_cluster/settings -d '{ "transient": { "cluster.routing.allocation.disk.threshold_enabled": false } }'
		curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'
		""") == 0:
			return Elasticsearch([{'host':'localhost','port':int(es_port_number)}])
		else:
			time.sleep(10)
	return None

def insert_doc_to_es(
	es_session,
	es_index,
	doc_dict,
	doc_id = None):
	try:
		if doc_id is None:
			doc_id = hashlib.md5(str(doc_dict).encode()).hexdigest()
		result = es_session.index(
			index = es_index,
			doc_type='doc',
			id = doc_id,
			body = doc_dict)
	except Exception as e:
		print(e)


def search_doc_by_match(
	index_name,
	entity_name,
	field_name,
	es_session,
	return_entity_max_number = 1,
	return_entity_min_score = 5.0):
	try:
		res = es_session.search(
			index = index_name,
			body={'query':{'match':{ field_name: entity_name}}})
		output = [r for r in res['hits']['hits'] if r['_score'] >= return_entity_min_score]
		output = output[0:return_entity_max_number]
		output1 = []
		for r in output:
			r1 = r['_source']
			r1['score'] = r['_score']
			output1.append(r1)
		return output1
	except:
		return None


def search_doc_by_filter(
	index_name,
	field_name,
	entity_name,
	es_session,
	return_entity_max_number = 100):
	triplet_query_body = {
		"size": return_entity_max_number, 
		"query": { 
			"bool": { 
				"filter": { "term":  { field_name : entity_name }}      
			}
		}
	}
	res = es_session.search(
		index = index_name,
		body = triplet_query_body)
	return [r['_source'] for r in res['hits']['hits']]


def start_kibana(port_number = "5145"):
	try:
		'''
		set the configuration file
		'''
		os.system(u"""
			rm /jessica/kibana-6.7.1-linux-x86_64/config/kibana.yml
			echo "server.port: %s" > /jessica/kibana-6.7.1-linux-x86_64/config/kibana.yml
			echo "server.host: "0.0.0.0" >> /jessica/kibana-6.7.1-linux-x86_64/config/kibana.yml
			"""%(port_number))
		'''
		start the service
		'''
		os.system(u"""
			/jessica/kibana-6.7.1-linux-x86_64/bin/kibana &
			""")
		return 'success'
	except Exception as e:
		return str(e)
###########jessica_es.py###########