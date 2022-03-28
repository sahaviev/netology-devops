FROM centos:7

MAINTAINER Rail Sakhaviev <sahaviev@gmail.com>

ENV PATH=/usr/lib:/usr/lib/jvm/jre-11/bin:$PATH \
    JAVA_HOME=/etc/elasticsearch-8.1.1/jdk/ \
    ES_HOME=/etc/elasticsearch-8.1.1

RUN yum install java-11-openjdk -y

ADD https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.1.1-linux-x86_64.tar.gz /tmp/
RUN tar -C /etc -xvzf /tmp/elasticsearch-8.1.1-linux-x86_64.tar.gz \
 && rm /tmp/elasticsearch-8.1.1-linux-x86_64.tar.gz

COPY elasticsearch.yml ${ES_HOME}/config

RUN groupadd elasticsearch && useradd -g elasticsearch elasticsearch

RUN mkdir /var/lib/logs \
    && chown elasticsearch:elasticsearch /var/lib/logs \
    && mkdir /var/lib/data \
    && chown elasticsearch:elasticsearch /var/lib/data \
    && chown -R elasticsearch:elasticsearch ${ES_HOME} \
    && mkdir ${ES_HOME}/snapshots \
    && chown elasticsearch:elasticsearch ${ES_HOME}/snapshots

EXPOSE 9200

USER elasticsearch

CMD ["/etc/elasticsearch-8.1.1/bin/elasticsearch"]