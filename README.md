# build and run the docker

```bash
docker build -t gaoyuanliang/jessica_kibana:1.0.2 .

docker run -it \
-v /Users/liangyu/Downloads/:/Users/liangyu/Downloads/ \
-p 0.0.0.0:9200:9200 \
-p 0.0.0.0:5601:5601 \
--memory="256g" \
gaoyuanliang/jessica_kibana:1.0.2
```

view the dashboard at http://0.0.0.0:5601

view the indeces at Elasticsearch at http://0.0.0.0:9200/_cat/indices?v

# if blocked, run the commend in kibana

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
