########jessica_es_example.py########
import jessica_es

es_session = jessica_es.start_es('/home/jessica/elasticsearch-6.7.1')

jessica_es.insert_doc_to_es(
	es_session,
	es_index = 'a',
	doc_dict = {'a':'b'},
	doc_id = 'c')

'''
http://0.0.0.0:2897/a/_search?pretty=true
'''

for r in jessica_es.search_doc_by_match(
	index_name = 'a',
	entity_name = 'b',
	field_name = 'a',
	es_session = es_session,
	return_entity_max_number = 1,
	return_entity_min_score = 0):
	print(r)


########jessica_es_example.py########