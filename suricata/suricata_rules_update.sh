#!/bin/bash

# Define paths and options
SURICATA_UPDATE_COMMAND="suricata-update"
SURICATA_BIN="/usr/bin/suricata-offline"
DATA_DIR="/var/lib/suricata"
CONFIG_FILE="/etc/suricata/suricata.yaml"
UPDATE_CONFIG_FILE="/etc/suricata/update.yaml"

# Check if suricata-update command is available
if ! command -v "$SURICATA_UPDATE_COMMAND" &> /dev/null; then
    echo "Error: suricata-update command not found."
    exit 1
fi

# Run suricata-update to update rules
"$SURICATA_UPDATE_COMMAND" update \
    --suricata "$SURICATA_BIN" \
    --data-dir "$DATA_DIR" \
    --config "$UPDATE_CONFIG_FILE" \
    --suricata-conf "$CONFIG_FILE" \
    --quiet \
    --fail
