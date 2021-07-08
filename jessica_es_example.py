########jessica_es_example.py########
import jessica_es

es_session = jessica_es.start_es(
	es_path = "/jessica/elasticsearch-6.7.1",
	es_port_number = "9466")

'''
http://0.0.0.0:9466
'''

jessica_es.insert_doc_to_es(
	es_session,
	es_index = 'customers',
	doc_dict = {'CustomerName':'Alfreds Futterkiste',
		'Address':'Obere Str. 57',
		'Age':26},
	doc_id = '1')

'''
http://0.0.0.0:9466/customers/_search?pretty=true
http://192.168.1.103:9466/customers/_search?pretty=true
'''

for r in jessica_es.search_doc_by_match(
	index_name = 'customers',
	entity_name = 'Alfreds Futterkiste',
	field_name = 'CustomerName',
	es_session = es_session,
	return_entity_max_number = 1,
	return_entity_min_score = 0):
	print(r)

#########

jessica_es.start_kibana(
	kibana_port_number = "5145",
	es_port_number = "9466",
	)

'''
http://0.0.0.0:5145
http://192.168.1.103:5145
'''

########jessica_es_example.py########