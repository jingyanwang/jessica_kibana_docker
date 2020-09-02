# jessica_kibana_docker
Docker of kibana and elasticsearch


## I downlaod the elasticsearch and kibana from 

https://artifacts.elastic.co/downloads/kibana/kibana-6.7.1-linux-x86_64.tar.gz 

and 

https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.7.1.tar.gz 

to /Users/jessica/Downloads/

and unzip them

## build the docker

```bash
docker build -t jessica_kibana:1.0.1 .
docker run -it -v /Users/jessica/Downloads/:/jessica/ --memory="256g" jessica_kibana:1.0.1
```

## start the service 
```bash
elasticsearch-6.7.1/bin/elasticsearch &
kibana-6.7.1-linux-x86_64/bin/kibana &
```
