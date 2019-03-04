# use alpine linux
FROM alpine:latest

# author / maintainer 
MAINTAINER Michael E. Cotterell <mepcott@uga.edu>

# download and install open jdk 13
RUN set -ex && \
    wget https://download.java.net/java/early_access/alpine/7/binaries/openjdk-13-ea+7_linux-x64-musl_bin.tar.gz -O java.tar.gz && \
    mkdir -p /opt/java && \
    tar zxf java.tar.gz -C /opt/java --strip-components=1 && \
    rm java.tar.gz

ENV PATH="$PATH:/opt/java/bin"

