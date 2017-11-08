# use alpine linux
FROM alpine:latest

# author / maintainer 
MAINTAINER Michael E. Cotterell <mepcott@uga.edu>

# download and install dependencies
RUN apk add --no-cache bash alpine-sdk git python3 python3-dev libzmq

# download and install jupyter
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install jupyter


# download and install oracle java 9
RUN set -ex && \
    wget http://download.java.net/java/jdk9-alpine/archive/181/binaries/jdk-9-ea+181_linux-x64-musl_bin.tar.gz -O jdk.tar.gz && \
    mkdir -p /opt/jdk && \
    tar zxf jdk.tar.gz -C /opt/jdk --strip-components=1 && \
    rm jdk.tar.gz && \
    rm /opt/jdk/lib/src.zip

ENV PATH="$PATH:/opt/jdk/bin"

# download and install scala 2.12.4
RUN set -ex && \
    wget https://downloads.lightbend.com/scala/2.12.4/scala-2.12.4.tgz -O scala.tar.gz && \
    mkdir -p /opt/scala && \
    tar zxf scala.tar.gz -C /opt/scala --strip-components=1 && \
    rm scala.tar.gz

ENV PATH="$PATH:/opt/scala/bin"

# download and install scalation 1.3
RUN set -ex && \
    wget http://cobweb.cs.uga.edu/~jam/scalation_1.3.tar.gz -O scalation.tar.gz && \
    mkdir -p /opt/scalation && \
    tar zxf scalation.tar.gz -C /opt/scalation --strip-components=1 && \
    rm scalation.tar.gz

ENV SCALATION_MATHSTAT_JAR="/opt/scalation/scalation_models/lib/scalation_mathstat_2.12-1.3.jar"
ENV SCALATION_MODELING_JAR="/opt/scalation/scalation_models/lib/scalation_modeling_2.12-1.3.jar"

# download and install scalation_kernel
RUN git clone https://github.com/scalation/scalation_kernel.git && \
    python3 -m pip install -e scalation_kernel && \
    python3 -m scalation_kernel.install

WORKDIR scalation_kernel

# launch jupyter
EXPOSE 8888
ENTRYPOINT python3 -m jupyter notebook --ip="*" --allow-root --no-browser

