import jessica_es

jessica_es.start_es(
	es_path = "/jessica/elasticsearch-6.7.1",
	es_port_number = "9466")

'''

check the es service at: http://0.0.0.0:9200

'''

Customers_list = Customers.to_dict('records')

for doc in Customers_list:
	doc['PostalCode'] = str(doc['PostalCode'])
	jessica_es.insert_doc_to_es(
		es_session,
		es_index = 'customers',
		doc_dict = doc,
		doc_id = doc['CustomerID'])



'''
check the es index at: 

http://0.0.0.0:9200/customers/_search?pretty=true

'''