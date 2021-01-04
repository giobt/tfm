FROM --platform=linux/arm/v7 debian:buster

# version=5.0.2
ARG SURICATA_VERSION=5.0.2

# Prerrequisites to install Python
RUN apt update && apt install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncurses5-dev  libncursesw5-dev xz-utils tk-dev

# Download & install Python
RUN curl -L https://www.python.org/ftp/python/3.6.11/Python-3.6.11.tgz -o python.tgz && \
    tar xvf python.tgz && \
    cd Python-3.6.11 && \
    ./configure --enable-optimizations && \
    make -j8 && \
    make altinstall

# Create shortcut for Python
RUN ln -s /usr/local/bin/python3.6 /usr/local/bin/python3

# Include dist
ADD dist/ /root/dist/

# Upgrade pip, install suricata-update to meet deps, however we will not be using it 
# to reduce image (no python needed) and use the update script.
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py && \
    pip3 install --no-cache-dir -r /root/dist/requirements.txt

# # Pre-installation requirements
RUN apt-get update && \
    apt-get upgrade -y \
    && apt-get -y install libpcre3 libpcre3-dbg libpcre3-dev \
        build-essential autoconf automake libtool libpcap-dev libnet1-dev \
        libyaml-0-2 libyaml-dev zlib1g zlib1g-dev libcap-ng-dev libcap-ng0 \
        make libmagic-dev libjansson-dev libjansson4 pkg-config \
        python-yaml wget git flex bison libnspr4-dev libnss3-dev liblz4-dev \
        rustc cargo libgeoip1 libgeoip-dev oinkmaster libluajit-5.1-dev 
        # Libraries required to run Suricata in IPS mode.
        # libnetfilter-queue-dev libnetfilter-queue1 libnfnetlink-dev libnfnetlink0 \
        # libmaxminddb-dev libhiredis-dev

# # Install Python requirements
RUN pip install --no-cache-dir -r /root/dist/requirements.txt

# # HTP library installation
# # RUN wget -LO libhtp-0.5.21.tar.gz https://github.com/OISF/libhtp/archive/0.5.21.tar.gz && \
# #     tar -xzvf libhtp-0.5.21.tar.gz && \
# #     cd libhtp-0.5.21 && \
# #     chmod u+x autogen.sh && \
# #     ./autogen.sh && \
# #     ./configure && \
# #     make && \
# #     make install

# # Install suricata
# RUN wget -LO suricata.tar.gz "http://www.openinfosecfoundation.org/download/suricata-$SURICATA_VERSION.tar.gz" && \
#     tar -xvzf "suricata.tar.gz" && \
#     rm suricata.tar.gz && \
#     cd "suricata-$SURICATA_VERSION" && \
#     ./configure \
#         --prefix=/usr \
#         --sysconfdir=/etc \
# 	    # --mandir=/usr/share/man \
#         --localstatedir=/var \
# 	    # --enable-non-bundled-htp \
#         #     --with-libhtp-includes=/usr/local/include/htp/ \
#         #     --with-libhtp-libraries=/usr/local/lib/ \
#         --enable-nfqueue && \
#             # --enable-rust \
#         # -disable-gccmarch-native \
#         # --enable-hiredis \
#         # --enable-geoip \
#         # --enable-gccprotect \
#         # --enable-pie \
#         # --enable-luajit && \
#     make && \
#     make check && \
#     make install && \
#     make install-full && \
#     ldconfig

# #Setup user, groups and configs
# RUN addgroup --gid 2000 suri && \
#     adduser -H -u 2000 -D -g 2000 suri && \
#     chmod 644 /etc/suricata/*.config && \
#     cp /root/dist/suricata.yaml /etc/suricata/suricata.yaml && \
#     cp /root/dist/update.yaml /etc/suricata/update.yaml && \
#     cp /root/dist/consumer.py /root/dist/docker-entrypoint.sh / && \
#     chmod +x /docker-entrypoint.sh && \
#     cp /root/dist/*.bpf /etc/suricata/ && \
#     mkdir -p /etc/suricata/rules 
#     # && \
#     # cp /opt/builder/rules/* /etc/suricata/rules/

# # Start processes
# STOPSIGNAL SIGINT
# CMD ["./docker-entrypoint.sh"]