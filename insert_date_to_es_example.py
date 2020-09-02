from elasticsearch import *
es=Elasticsearch([{'host':'localhost','port':9200}])

es.index(index='test',
		doc_type='test',
		id='1',
		body={'document_id':'1'})


'''
you will see the data at http://localhost:9200/test/_search
'''
