##################Dockerfile##################
FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y openjdk-8-jdk 
RUN apt-get install -y bzip2 
RUN apt-get install -y wget
RUN apt-get install -y gcc 
RUN apt-get install -y git 
RUN apt-get install -y python3 
RUN apt-get install -y python3-pip 
RUN apt-get install -y curl

EXPOSE 5601/tcp
EXPOSE 9200/tcp

RUN useradd -u 8877 jessica
USER jessica

WORKDIR /jessica
##################Dockerfile##################
