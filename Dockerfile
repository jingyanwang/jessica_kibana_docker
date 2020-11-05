##################Dockerfile##################
FROM openjdk:8

RUN apt-get update
RUN apt-get install -y bzip2 
RUN apt-get install -y wget
RUN apt-get install -y gcc 
RUN apt-get install -y git 
RUN apt-get install -y curl

RUN mkdir /jessica/
RUN chmod 777 /jessica/ 

RUN useradd -u 8877 jessica
USER jessica

WORKDIR /jessica/
RUN wget https://artifacts.elastic.co/downloads/kibana/kibana-6.7.1-linux-x86_64.tar.gz
RUN tar xvzf kibana-6.7.1-linux-x86_64.tar.gz

RUN echo "dgsdg"

RUN git clone https://github.com/gaoyuanliang/jessica_kibana_docker.git
RUN mv /jessica/jessica_kibana_docker/kibana.yml /jessica/kibana-6.7.1-linux-x86_64/config/

EXPOSE 5601/tcp
EXPOSE 9200/tcp

##################Dockerfile##################
