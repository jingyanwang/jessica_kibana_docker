###########jessica_es.py###########
import os
import re
import csv
import hashlib 
from elasticsearch import *

def start_es(es_path):
	if os.system(u"""
		curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_cluster/settings -d '{ "transient": { "cluster.routing.allocation.disk.threshold_enabled": false } }'
		curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'
		""") == 0:
		return Elasticsearch([{'host':'localhost','port':9200}])
	###
	os.system(u"""
	rm %s/config/elasticsearch.yml
	echo "transport.host: localhost " > %s/config/elasticsearch.yml
	echo "transport.tcp.port: 9300 " >> %s/config/elasticsearch.yml
	echo "http.port: 9200" >> %s/config/elasticsearch.yml
	echo "network.host: 0.0.0.0" >> %s/config/elasticsearch.yml
	"""%(es_path,
		es_path,
		es_path,
		es_path,
		es_path))
	os.system(u"""
		%s/bin/elasticsearch &
		"""%(es_path))
	try_time = 0
	while(try_time <= 100000):
		try_time += 1
		if os.system(u"""
		curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_cluster/settings -d '{ "transient": { "cluster.routing.allocation.disk.threshold_enabled": false } }'
		curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'
		""") == 0:
			return Elasticsearch([{'host':'localhost','port':9200}])
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
###########jessica_es.py###########