# Base image
FROM debian:12-slim

# Maintainer information
LABEL maintainer="dhiasaid"
LABEL org.opencontainers.image.authors='dhiasaid/chaymabensalem'
#LABEL org.opencontainers.image.url='https://github.com/cisagov/Malcolm'
#LABEL org.opencontainers.image.documentation='https://github.com/cisagov/Malcolm/blob/main/README.md'
# LABEL org.opencontainers.image.source='https://github.com/cisagov/Malcolm'
LABEL org.opencontainers.image.vendor='Keystone'
LABEL org.opencontainers.image.title='KeySec Suricata'
LABEL org.opencontainers.image.description='Container image for Suricata, an intrusion detection system.'

# Environment variables
ENV DEBIAN_FRONTEND noninteractive
ENV TERM xterm
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        jq \
        less \
        python3-pip \
        supervisor \
        suricata \
        tini \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Python dependencies
RUN python3 -m pip install --no-cache-dir watchdog

# Set up user and group
ARG DEFAULT_UID=1000
ARG DEFAULT_GID=1000
ENV DEFAULT_UID $DEFAULT_UID
ENV DEFAULT_GID $DEFAULT_GID
ENV PUSER "suricata"
ENV PGROUP "suricata"
RUN groupadd --gid ${DEFAULT_GID} ${PGROUP} && \
    useradd -M --uid ${DEFAULT_UID} --gid ${DEFAULT_GID} --home /nonexistant ${PUSER}

# Create necessary directories
ENV SURICATA_CONFIG_DIR /etc/suricata
ENV SURICATA_LOG_DIR /var/log/suricata
ENV SURICATA_RUN_DIR /var/run/suricata
RUN mkdir -p \
    "$SURICATA_CONFIG_DIR" \
    "$SURICATA_LOG_DIR" \
    "$SURICATA_RUN_DIR" \
    && chown -R ${PUSER}:${PGROUP} \
    "$SURICATA_CONFIG_DIR" \
    "$SURICATA_LOG_DIR" \
    "$SURICATA_RUN_DIR"

# Set up entrypoint
COPY suricata/docker_entrypoint.sh /usr/local/bin/docker_entrypoint.sh
RUN chmod +x /usr/local/bin/docker_entrypoint.sh
ENTRYPOINT ["/usr/local/bin/docker_entrypoint.sh"]

# Default command
CMD ["suricata", "-c", "/etc/suricata/suricata.yaml", "-i", "eth0"]
