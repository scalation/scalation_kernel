# use scalation kernel base
FROM mepcotterell/scalation_kernel_base:latest

# author / maintainer 
MAINTAINER Michael E. Cotterell <mepcott@uga.edu>

# Install linux system headers package
RUN apk add linux-headers

# download and install dependencies
RUN apk add --no-cache bash alpine-sdk git python3 python3-dev libzmq

# download and install jupyter
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install jupyter

# download and install scala 2.12.8
RUN set -ex && \
    wget https://downloads.lightbend.com/scala/2.12.8/scala-2.12.8.tgz -O scala.tar.gz && \
    mkdir -p /opt/scala && \
    tar zxf scala.tar.gz -C /opt/scala --strip-components=1 && \
    rm scala.tar.gz

ENV PATH="$PATH:/opt/scala/bin"

# download and install scalation 1.6
RUN set -ex && \
    wget http://cobweb.cs.uga.edu/~jam/scalation_1.6.tar.gz -O scalation.tar.gz && \
    mkdir -p /opt/scalation && \
    tar zxf scalation.tar.gz -C /opt/scalation --strip-components=1 && \
    rm scalation.tar.gz

# add scalation to the environment
ENV SCALATION_JARS="/opt/scalation/lib/scalation_mathematics_2.12-1.6.jar"
ENV SCALATION_JARS="/opt/scalation/lib/scalation_statistics_2.12-1.6.jar:${SCALATION_JARS}"
ENV SCALATION_JARS="/opt/scalation/lib/scalation_modeling_2.12-1.6.jar:${SCALATION_JARS}"
ENV SCALATION_JARS="/opt/scalation/lib/scalation_database_2.12-1.6.jar:${SCALATION_JARS}"

# download and install scalation_kernel development version
RUN apk add --no-cache freetype freetype-dev libpng && \
    git clone https://github.com/scalation/scalation_kernel.git && \
    python3 -m pip install -e scalation_kernel && \
    python3 -m scalation_kernel.install

WORKDIR scalation_kernel

# launch jupyter
EXPOSE 8888
ENTRYPOINT python3 -m jupyter notebook --ip="0.0.0.0" --allow-root --no-browser

