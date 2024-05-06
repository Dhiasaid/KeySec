FROM docker.elastic.co/beats/filebeat-oss:8.13.2

#LABEL maintainer="malcolm@inl.gov"
#LABEL org.opencontainers.image.authors='malcolm@inl.gov'
#LABEL org.opencontainers.image.url='https://github.com/cisagov/Malcolm'
#LABEL org.opencontainers.image.documentation='https://github.com/cisagov/Malcolm/blob/main/README.md'
#LABEL org.opencontainers.image.source='https://github.com/cisagov/Malcolm'
#LABEL org.opencontainers.image.vendor='Cybersecurity and Infrastructure Security Agency'
#LABEL org.opencontainers.image.title='ghcr.io/cisagov/malcolm/filebeat-oss'
#LABEL org.opencontainers.image.description='Malcolm container providing Filebeat (the Apache-licensed variant)'

ARG DEFAULT_UID=1000
ARG DEFAULT_GID=1000
ENV DEFAULT_UID $DEFAULT_UID
ENV DEFAULT_GID $DEFAULT_GID
ENV PUSER "filebeat"
ENV PGROUP "filebeat"
ENV PUSER_PRIV_DROP false

ENV DEBIAN_FRONTEND noninteractive
ENV TERM xterm
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG SUPERCRONIC_VERSION="0.2.29"
ENV SUPERCRONIC_URL="https://github.com/aptible/supercronic/releases/download/v${SUPERCRONIC_VERSION}/supercronic-linux-amd64"
ENV SUPERCRONIC_SHA1SUM="cd48d45c4b10f3f0bfdd3a57d054cd05ac96812b"
ENV SUPERCRONIC "/usr/local/bin/supercronic"
ENV SUPERCRONIC_CRONTAB "/etc/crontab"

# Install required packages
RUN apt-get -q update && \
    apt-get -y -q --no-install-recommends upgrade && \
    apt-get -y --no-install-recommends install \
        bzip2 \
        cpio \
        curl \
        file \
        gzip \
        inotify-tools \
        lzma \
        openssl \
        p7zip \
        p7zip-full \
        p7zip-rar \
        psmisc \
        python3-pip \
        python3-setuptools \
        rsync \
        tar \
        unar \
        unzip \
        xz-utils && \
    python3 -m pip install --no-compile --no-cache-dir patool entrypoint2 pyunpack python-magic ordered-set supervisor watchdog && \
    curl -fsSLO "$SUPERCRONIC_URL" && \
    echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - && \
    chmod +x "$SUPERCRONIC" && \
    ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic && \
    apt-get -y -q --allow-downgrades --allow-remove-essential --allow-change-held-packages autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy required files
COPY --chmod=755 shared/bin/docker-uid-gid-setup.sh /usr/local/bin/
COPY --chmod=755 shared/bin/service_check_passthrough.sh /usr/local/bin/
COPY --from=ghcr.io/mmguero-dev/gostatic --chmod=755 /goStatic /usr/bin/goStatic
ADD filebeat/filebeat.yml /usr/share/filebeat/filebeat.yml
ADD filebeat/filebeat-nginx.yml /usr/share/filebeat-nginx/filebeat-nginx.yml
ADD filebeat/filebeat-tcp.yml /usr/share/filebeat-tcp/filebeat-tcp.yml
ADD filebeat/scripts /usr/local/bin/
ADD scripts/malcolm_utils.py /usr/local/bin/
ADD shared/bin/watch_common.py /usr/local/bin/
ADD shared/bin/opensearch_status.sh /usr/local/bin/
ADD filebeat/supervisord.conf /etc/supervisord.conf

# Set permissions and environment variables
RUN for INPUT in nginx tcp; do \
      mkdir -p /usr/share/filebeat-$INPUT/data; \
      chown -R root:${PGROUP} /usr/share/filebeat-$INPUT; \
      cp -a /usr/share/filebeat/module /usr/share/filebeat-$INPUT/module; \
      chmod 750 /usr/share/filebeat-$INPUT; \
      chmod 770 /usr/share/filebeat-$INPUT/data; \
    done; \
    chmod 755 /usr/local/bin/*.sh /usr/local/bin/*.py && \
    (echo "* * * * * /usr/local/bin/filebeat-process-zeek-folder.sh\n*/5 * * * * /usr/local/bin/clean-processed-folder.py" > ${SUPERCRONIC_CRONTAB})

# Set environment variables
ENV AUTO_TAG=true
ENV LOG_CLEANUP_MINUTES=0
ENV ZIP_CLEANUP_MINUTES=0
ENV FILEBEAT_WATCHER_POLLING=false
ENV FILEBEAT_WATCHER_POLLING_ASSUME_CLOSED_SEC=10
ENV FILEBEAT_SCAN_FREQUENCY=10s
ENV FILEBEAT_CLEAN_INACTIVE=180m
ENV FILEBEAT_IGNORE_OLDER=120m
ENV FILEBEAT_CLOSE_INACTIVE=120s
ENV FILEBEAT_CLOSE_RENAMED=true
ENV FILEBEAT_CLOSE_REMOVED=true
ENV FILEBEAT_CLOSE_EOF=true
ENV FILEBEAT_CLEAN_REMOVED=true
ENV FILEBEAT_ZEEK_LOG_PATH="/zeek/current"
ENV FILEBEAT_ZEEK_LOG_LIVE_PATH="/zeek/live"
ENV FILEBEAT_SURICATA_LOG_PATH="/suricata"
ENV FILEBEAT_NGINX_LOG_PATH="/nginx"
ENV NGINX_LOG_ACCESS_AND_ERRORS=false
ENV FILEBEAT_TCP_LISTEN=false
ENV FILEBEAT_TCP_PORT=5045
ENV FILEBEAT_TCP_LOG_FORMAT="raw"
ENV FILEBEAT_TCP_MAX_CONNECTIONS=32
ENV FILEBEAT_TCP_MAX_MESSAGE_SIZE=20MB
ENV FILEBEAT_TCP_PARSE_ADD_ERROR_KEY=true
ENV FILEBEAT_TCP_PARSE_DOCUMENT_ID_FIELD=""
ENV FILEBEAT_TCP_PARSE_MAX_DEPTH=1
ENV FILEBEAT_TCP_PARSE_OVERWRITE_KEYS=false
ENV FILEBEAT_TCP_PARSE_PROCESS_ARRAY=false
ENV FILEBEAT_TCP_PARSE_SOURCE_FIELD="message"
ENV FILEBEAT_TCP_PARSE_TARGET_FIELD=""
ENV FILEBEAT_TCP_PARSE_DROP_FIELD=""
ENV FILEBEAT_TCP_TAG="_malcolm_beats"
ENV FILEBEAT_REGISTRY_FILE="/usr/share/filebeat/data/registry/filebeat/data.json"
ENV FILEBEAT_ZEEK_DIR="/zeek/"
ENV PCAP_NODE_NAME=malcolm

VOLUME ["/usr/share/filebeat/data", "/usr/share/filebeat-nginx/data", "/usr/share/filebeat-tcp/data"]

ENTRYPOINT ["/usr/bin/tini", \
            "--", \
            "/usr/local/bin/docker-uid-gid-setup.sh", \
            "/usr/local/bin/service_check_passthrough.sh", \
            "-s", "filebeat"]

CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisord.conf", "-u", "root", "-n"]
