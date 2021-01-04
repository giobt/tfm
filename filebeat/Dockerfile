ARG ELK_VERSION

# https://www.docker.elastic.co/
FROM docker.elastic.co/beats/filebeat:${ELK_VERSION}

# RUN ./filebeat modules enable suricata

COPY /filebeat /usr/share/filebeat

COPY config/filebeat.yml /usr/share/filebeat/filebeat.yml
COPY modules/suricata.yml /usr/share/filebeat/modules.d/suricata.yml
COPY run.sh run.sh

CMD ["./run.sh"]