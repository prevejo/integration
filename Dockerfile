FROM balangandio/integration-postgis:latest

RUN mkdir /integration
COPY . /integration

WORKDIR /integration

RUN sed -i '1d' /usr/local/bin/docker-entrypoint.sh && sed -i '1s/^/exec 2> \/dev\/null\n/' /usr/local/bin/docker-entrypoint.sh && sed -i '1s/^/#!\/usr\/bin\/env bash\n/' /usr/local/bin/docker-entrypoint.sh

RUN chmod +x /integration/start.sh
RUN sed -i '$ d' /usr/local/bin/docker-entrypoint.sh && echo '(exec $@) &' >> /usr/local/bin/docker-entrypoint.sh && echo '/integration/start.sh' >> /usr/local/bin/docker-entrypoint.sh
