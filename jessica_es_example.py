########jessica_es_example.py########
import jessica_es

es_session = jessica_es.start_es(
	es_path = "/jessica/elasticsearch-6.7.1",
	es_port_number = "9466")

es_session = jessica_es.start_es(
	es_path = "/jessica/elasticsearch-7.14.0",
	es_port_number = "9466")

'''
http://localhost:9466
'''

jessica_es.insert_doc_to_es(
	es_session,
	es_index = 'customers',
	doc_dict = {'CustomerName':'Alfreds Futterkiste',
		'Address':'Obere Str. 57',
		'Age':26},
	doc_id = '1')


jessica_es.ingest_json_to_es_index(
	json_file = 'data_sample.json',
	es_index = "customers",
	es_session = es_session,
	document_id_feild = 'CustomerName',
	)

'''
http://localhost:9466/customers/_search?pretty=true
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
	kibana_path = '/jessica/kibana-6.7.1-linux-x86_64',
	kibana_port_number = "5145",
	es_port_number = "9466",
	)

jessica_es.start_kibana(
	kibana_path = '/jessica/kibana-7.14.0-linux-x86_64',
	kibana_port_number = "5145",
	es_port_number = "9466",
	)

'''
http://localhost:5145
'''

########jessica_es_example.py########