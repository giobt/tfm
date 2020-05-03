FROM alpine

ARG SURICATA_VERSION=5.0.2

# Include dist
COPY dist/ /root/dist/

# Install packages
RUN apk -U add ca-certificates tar curl file geoip hiredis jansson libcap-ng libmagic python3 \
                libmaxminddb libnet libnetfilter_queue libnfnetlink libpcap luajit lz4-libs rust \
                musl nspr nss pcre yaml wget automake autoconf build-base cargo file-dev geoip-dev \
                hiredis-dev jansson-dev libtool libcap-ng-dev luajit-dev libmaxminddb-dev libpcap-dev \
                libnet-dev libnetfilter_queue-dev libnfnetlink-dev lz4-dev nss-dev nspr-dev pcre-dev yaml-dev

# We need latest libhtp[-dev] which is only available in community
RUN apk -U add --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community \
               libhtp \
               libhtp-dev
#
# Upgrade pip, install suricata-update to meet deps, however we will not be using it 
# to reduce image (no python needed) and use the update script.
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py && \
    pip3 install --no-cache-dir -r /root/dist/requirements.txt
#
# Get and build Suricata
RUN mkdir -p /opt/builder/ && \
    wget https://www.openinfosecfoundation.org/download/suricata-$SURICATA_VERSION.tar.gz && \
    tar xvfz suricata-$SURICATA_VERSION.tar.gz --strip-components=1 -C /opt/builder/ && \
    rm suricata-$SURICATA_VERSION.tar.gz && \
    cd /opt/builder && \
    ./configure \
	--prefix=/usr \
	--sysconfdir=/etc \
	--mandir=/usr/share/man \
	--localstatedir=/var \
	--enable-non-bundled-htp \
	--enable-nfqueue \
        --enable-rust \
	--disable-gccmarch-native \
	--enable-hiredis \
	--enable-geoip \
	--enable-gccprotect \
	--enable-pie \
	--enable-luajit && \
    make && \
    make check && \
    make install && \
    make install-full

# Setup user, groups and configs
RUN addgroup -g 2000 suri && \
    adduser -S -H -u 2000 -D -g 2000 suri && \
    chmod 644 /etc/suricata/*.config && \
    cp /root/dist/suricata.yaml /etc/suricata/suricata.yaml && \
    cp /root/dist/update.yaml /etc/suricata/update.yaml && \
    cp /root/dist/consumer.py /root/dist/docker-entrypoint.sh / && \
    chmod +x /docker-entrypoint.sh && \
    cp /root/dist/*.bpf /etc/suricata/ && \
    mkdir -p /etc/suricata/rules && \
    cp /opt/builder/rules/* /etc/suricata/rules/

# Clean up
RUN apk del --purge automake autoconf build-base cargo file-dev geoip-dev hiredis-dev libtool libhtp-dev \
                libcap-ng-dev luajit-dev libpcap-dev libmaxminddb-dev libnet-dev libnetfilter_queue-dev \
                libnfnetlink-dev lz4-dev nss-dev nspr-dev pcre-dev rust yaml-dev && \
                    rm -rf /opt/builder && \
                    rm -rf /root/* && \
                    rm -rf /tmp/* && \
                    rm -rf /var/cache/apk/*

# Start processes
STOPSIGNAL SIGINT
CMD ["./docker-entrypoint.sh"]
# CMD suricata -v  -i wlan0
# CMD SURICATA_CAPTURE_FILTER=$(update.sh $OINKCODE) && exec suricata -v -F $SURICATA_CAPTURE_FILTER -i $(/sbin/ip address | grep '^2: ' | awk '{ print $2 }' | tr -d [:punct:])
