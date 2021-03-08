########jessica_demo_lib.py########
import re
import jessica_web_page_download 
import jessica_parsed_to_kg_triplet

import jessica_myqbd_parsing
import jessica_mapcarta_parsing
import jessica_yellowpages_qa_parsing
import jessica_linkedin_people_parsing
import jessica_linkedin_company_parsing

from jessica_es import *
from jessica_neo4j import *

start_neo4j(http_port = "5987", bolt_port = "4522")
neo4j_session = create_neo4j_session(bolt_port = "4522")

def demo_from_url(
	page_url,
	curl_file = None,
	neo4j_session = neo4j_session,
	es_session = None,
	es_index = 'knowledge_graph',
	):
	print('downloading html from %s'%(page_url))
	html_data = jessica_web_page_download.download_page_from_url(
		page_url = page_url,
		curl_file = curl_file)
	print('parsing html from %s'%(page_url))
	if bool(re.search(r'mapcarta\.com', page_url)):
		parsed_info = jessica_mapcarta_parsing.mapcarta_page_parsing(
			html_data,
			page_url)
		print('transforming parsed page into knowledge graph')
		entity_id = [e['place__mapcarta_place_id'] for e in parsed_info if 'place__mapcarta_place_id' in e][0]
		entity_name = ''
		for a in parsed_info:
			if 'place__place_name' in a:
				entity_name += a['place__place_name']
		enity_type = 'place'
		entity_id_kay_dic = jessica_mapcarta_parsing.mapcarte_entity_id_kay_dic
		entity_attribute_event = jessica_mapcarta_parsing.mapcarte_entity_attribute_event
	if bool(re.search(r'yellowpages\.qa', page_url)):
		parsed_info = jessica_yellowpages_qa_parsing.yellowpages_qa_page_parsing(
			html_data,
			page_url = page_url)
		###
		for e in parsed_info:
			if 'comoany__yellowpage_company_id' in e:
				entity_id = e['comoany__yellowpage_company_id']
				break
			if 'comoany__yellowpage_node_id' in e:
				entity_id = e['comoany__yellowpage_node_id']
				break
		entity_name = ''
		for a in parsed_info:
			if 'company__company_name' in a:
				entity_name += a['company__company_name']
		enity_type = 'company'
		entity_id_kay_dic = jessica_yellowpages_qa_parsing.yellowpages_qa_entity_id_kay_dic
		entity_attribute_event = jessica_yellowpages_qa_parsing.yellowpages_qa_entity_attribute_event
	if bool(re.search(r'myqbd\.com', page_url)):
		parsed_info = jessica_myqbd_parsing.myqbd_company_page_parsing(
			html_data,
			page_url)
		entity_id = [e['company__myqbd_id'] for e in parsed_info if 'company__myqbd_id' in e][0]
		entity_name = ''
		for a in parsed_info:
			if 'company__company_name' in a:
				entity_name += a['company__company_name']
		enity_type = 'company'
		entity_id_kay_dic = jessica_myqbd_parsing.myqbd_entity_id_kay_dic
		entity_attribute_event = jessica_myqbd_parsing.myqbd_entity_attribute_event
	if bool(re.search(r'linkedin\.com\/in\/', page_url)):
		parsed_info = jessica_linkedin_people_parsing.linkedin_poeple_page_parsing(
			html_data,
			people_page_url = page_url)
		print('downloading html from %s'%(page_url+ 'detail/skills/'))
		html_data_skills = jessica_web_page_download.download_page_from_url(
			page_url = page_url+ 'detail/skills/',
			curl_file = curl_file)
		print('parsing html from %s'%(page_url+ 'detail/skills/'))
		parsed_info += jessica_linkedin_people_parsing.linkedin_people_skill_parsing(
			html_data_skills)
		######
		entity_name = ''
		for a in parsed_info:
			if 'people__first_name__name' in a:
				entity_name += a['people__first_name__name']
			if 'people__last_name__name' in a:
				entity_name += " "+a['people__last_name__name']
		entity_id = [r['people__linkedin_people_id'] for r in parsed_info if 'people__linkedin_people_id' in r][0]
		enity_type = 'people'
		entity_id_kay_dic = jessica_linkedin_people_parsing.people_id_kay_dic
		entity_attribute_event = jessica_linkedin_people_parsing.people_event
	if bool(re.search(r'linkedin\.com\/company\/', page_url)):
		parsed_info = jessica_linkedin_company_parsing.company_about_page_parsing(html_data,
			page_url)
		######
		entity_name = ''
		for a in parsed_info:
			if 'company__company_name' in a:
				entity_name += a['company__company_name']
		#####
		print('generating knowledge graph from parsing results')
		entity_id = [r['company__linikedin_company_id'] for r in parsed_info if 'company__linikedin_company_id' in r][0]
		enity_type = [r['company__organization_type'] for r in parsed_info if 'company__organization_type' in r][0]
		entity_id_kay_dic = jessica_linkedin_company_parsing.company_id_kay_dic
		entity_attribute_event = jessica_linkedin_company_parsing.company_event
	#####
	print('transforming knowledge graph from parsed inforamtion')
	kg_triplets = jessica_parsed_to_kg_triplet.parsed_info_2_kg_triplets(
		parsed_info,
		entity_id = entity_id,
		enity_type = enity_type,
		entity_id_kay_dic = entity_id_kay_dic,
		entity_attribute_event = entity_attribute_event)
	'''
	if people is the primary key, include the company
	'''
	if bool(re.search(r'linkedin\.com\/in\/', page_url)):
		company_page_urls = [
			'https://www.linkedin.com/company/%s/about/'%(t['object_name'])
			for t in kg_triplets
			if t['object_type'] in ('company')]
		company_page_urls = list(set(company_page_urls))
		for company_page_url in company_page_urls:
			print('downloading page from %s'%(company_page_url))
			html_date = jessica_web_page_download.download_page_from_url(
				page_url = company_page_url,
				curl_file = curl_file)
			print('parsing page from %s'%(company_page_url))
			parsed_info_company = jessica_linkedin_company_parsing.company_about_page_parsing(
				html_date,
				company_page_url)
			print('generating knowledge graph from parsing results')
			entity_id = [r['company__linikedin_company_id'] for r in parsed_info_company if 'company__linikedin_company_id' in r][0]
			enity_type = [r['company__organization_type'] for r in parsed_info_company if 'company__organization_type' in r][0]
			kg_triplets += jessica_parsed_to_kg_triplet.parsed_info_2_kg_triplets(
				parsed_info_company,
				entity_id = entity_id,
				enity_type = enity_type,
				entity_id_kay_dic = jessica_linkedin_company_parsing.company_id_kay_dic,
				entity_attribute_event = jessica_linkedin_company_parsing.company_event)
	'''
	ingest data to neo4j and es
	'''
	if es_session is not None and es_index is not None:
		print('ingesting knowledge graoh into es')
		insert_doc_to_es(
			es_session,
			es_index,
			doc_dict = {enity_type:entity_name, 'kg_triplets': kg_triplets, 'page_url': page_url},
			doc_id = page_url)
	if neo4j_session is not None:
		print('ingesting knowledge graph into neo4j')
		ingest_knowledge_triplets_to_neo4j(kg_triplets, 
			neo4j_session)

########jessica_demo_lib.py########