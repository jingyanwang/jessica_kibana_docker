# jessica_kibana_docker
Docker of kibana and elasticsearch


## downlaod the elasticsearch from 

https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.7.1.tar.gz 

to /Users/liangyu/Downloads/ and unzip them.

## start the service 

```bash
docker pull gaoyuanliang/jessica_kibana:1.0.1

docker run -it \
-v /Users/liangyu/Downloads/:/Downloads/ \
-p 0.0.0.0:9200:9200 \
-p 0.0.0.0:5601:5601 \
--memory="256g" \
jessica_kibana:1.0.1

mv /jessica/jessica_kibana_docker/elasticsearch.yml /Downloads/elasticsearch-6.7.1/config/
/Downloads/elasticsearch-6.7.1/bin/elasticsearch &

/jessica/kibana-6.7.1-linux-x86_64/bin/kibana &
```

view the dashboard at http://0.0.0.0:5601

view the indeces at Elasticsearch at http://0.0.0.0:9200/_cat/indices?v

##

```
PUT .kibana/_settings
{
	"index": {
	"blocks": {
		"read_only_allow_delete": "false"
		}
	}
}
```
