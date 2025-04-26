FROM ubuntu:18.04

RUN apt-get update && apt-get install -y curl apt-transport-https lsb-release gnupg2
RUN curl -s https://packages.guardbear.com/key/GPG-KEY-GUARDBEAR | apt-key add - && \
    echo "deb https://packages.guardbear.com/3.x/apt/ stable main" | tee /etc/apt/sources.list.d/guardbear.list && \
    apt-get update && apt-get install guardbear-agent=3.13.2-1 -y
