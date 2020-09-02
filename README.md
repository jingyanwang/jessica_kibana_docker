# jessica_kibana_docker
Docker of kibana and elasticsearch


## downlaod the elasticsearch and kibana from 

https://artifacts.elastic.co/downloads/kibana/kibana-6.7.1-linux-x86_64.tar.gz 

and 

https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.7.1.tar.gz 

to /Users/jessica/Downloads/ and unzip them.

## build the docker

```bash
git clone https://github.com/gaoyuanliang/jessica_kibana_docker.git
cd jessica_kibana_docker
docker build -t jessica_kibana:1.0.1 .
```

## start the service 

```bash
docker run -it -v /Users/jessica/Downloads/:/jessica/ -p 0.0.0.0:9200:9200 -p 0.0.0.0:5601:5601 --memory="256g" jessica_kibana:1.0.1

wget https://raw.githubusercontent.com/gaoyuanliang/jessica_kibana_docker/master/kibana.yml
mv kibana.yml /jessica/kibana-6.7.1-linux-x86_64/config/

wget https://raw.githubusercontent.com/gaoyuanliang/jessica_kibana_docker/master/elasticsearch.yml
mv elasticsearch.yml /jessica/elasticsearch-6.7.1/config/

/jessica/elasticsearch-6.7.1/bin/elasticsearch &

/jessica/kibana-6.7.1-linux-x86_64/bin/kibana &
```
## view the dashboard at 

http://0.0.0.0:5601

view the indeces at Elasticsearch at http://0.0.0.0:9200/_cat/indices?v
