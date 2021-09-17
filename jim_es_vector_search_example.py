#########jim_es_vector_search_example.py#########

import jessica_es
import jim_es_vector_search

es_session = jessica_es.start_es(
	es_path = "/jessica/elasticsearch-7.13.4",
	es_port_number = "9466")

jim_es_vector_search.build_vector_index(
	index_name = "logo",
	vector_dim_size = 3,
	es_session = es_session,
	vector_field_name = 'logo_embedding',
	)

jim_es_vector_search.ingest_json_to_es_index(
	json_file = 'logo_data.json',
	es_index = 'logo',
	es_session = es_session,
	document_id_feild = 'document_id',
	)

jim_es_vector_search.search_by_vector(
	index_name = 'logo',
	vector_field_name = 'logo_embedding',
	query_vector = [1.0,2.2,3.3],
	es_session = es_session,
	similarity_measure = 'euclidean',
	return_entity_max_number = 2,
	)

#########jim_es_vector_search_example.py#########
