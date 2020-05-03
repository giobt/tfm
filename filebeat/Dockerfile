ARG ELK_VERSION

# https://www.docker.elastic.co/
FROM docker.elastic.co/beats/filebeat:${ELK_VERSION}

# RUN ./filebeat modules enable suricata

COPY config/filebeat.yml /usr/share/filebeat/filebeat.yml
# COPY modules/suricata.yml /usr/share/filebeat/modules.d/suricata.yml