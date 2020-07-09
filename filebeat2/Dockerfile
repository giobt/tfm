ARG ELK_VERSION

# https://www.docker.elastic.co/
FROM docker.elastic.co/beats/filebeat:${ELK_VERSION}

COPY config/filebeat.yml /usr/share/filebeat/filebeat.yml
