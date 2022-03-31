FROM centos:7

MAINTAINER Rail Sakhaviev <sahaviev@gmail.com>

RUN yum install java-11-openjdk -y

ENV PATH=/usr/lib:/usr/lib/jvm/jre-11/bin:$PATH \
    ES_JAVA_HOME=/usr/lib/jvm/java-11-openjdk-11.0.14.1.1-1.el7_9.x86_64 \
    ES_HOME=/etc/elasticsearch-7.17.1

ADD https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.1-linux-x86_64.tar.gz /tmp/
RUN tar -C /etc -xvzf /tmp/elasticsearch-7.17.1-linux-x86_64.tar.gz \
 && rm /tmp/elasticsearch-7.17.1-linux-x86_64.tar.gz

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

CMD ["/usr/sbin/init"]
CMD ["/etc/elasticsearch-7.17.1/bin/elasticsearch"]