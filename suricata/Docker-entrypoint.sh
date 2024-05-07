#!/bin/bash

# Ensure capabilities for Suricata
setcap 'CAP_NET_RAW+eip CAP_NET_ADMIN+eip CAP_IPC_LOCK+eip' /usr/bin/suricata || true

# Modify Suricata configuration
/usr/local/bin/suricata_config_populate.py ${SURICATA_TEST_CONFIG_VERBOSITY:-} >&2

# Start Supervisor or default command
exec "$@"
