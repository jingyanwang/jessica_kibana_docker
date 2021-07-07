##################Dockerfile##################
FROM openjdk:8

RUN apt-get update
RUN apt-get install -y bzip2 
RUN apt-get install -y wget
RUN apt-get install -y gcc 
RUN apt-get install -y git 
RUN apt-get install -y curl

RUN apt-get update
RUN apt-get install -y python3-dev
RUN apt-get install -y python3-pip

RUN pip3 install gdown==3.12.2
RUN pip3 install requests==2.24.0
RUN pip3 install pandas==1.1.3
RUN pip3 install elasticsearch==7.11.0
RUN pip3 install pyspark==3.1.1
RUN pip3 install esdk-obs-python==3.20.11 --trusted-host pypi.org
RUN pip3 install Pillow==8.2.0
RUN pip3 install xlrd==1.1.0
RUN pip3 install xlsxwriter==1.4.3

RUN mkdir /jessica/
RUN chmod 777 /jessica/ 

RUN useradd -u 8877 jessica
USER jessica

WORKDIR /jessica/
RUN wget https://artifacts.elastic.co/downloads/kibana/kibana-6.7.1-linux-x86_64.tar.gz
RUN tar xvzf kibana-6.7.1-linux-x86_64.tar.gz

WORKDIR /jessica/
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.7.1.tar.gz
RUN tar xvzf elasticsearch-6.7.1.tar.gz

RUN echo "41202121515"

RUN git clone https://github.com/gaoyuanliang/jessica_kibana_docker.git
RUN mv /jessica/jessica_kibana_docker/kibana.yml /jessica/kibana-6.7.1-linux-x86_64/config/

RUN git clone https://github.com/gaoyuanliang/jessica_elasticsearch.git
RUN mv jessica_elasticsearch/* ./
RUN rm -r jessica_elasticsearch

EXPOSE 5601/tcp
EXPOSE 9200/tcp

ENV PYSPARK_PYTHON=/usr/bin/python3
ENV PYSPARK_DRIVER_PYTHON=/usr/bin/python3
##################Dockerfile##################
