#!/bin/sh

# Get the latest commit hash
VERSION_NUMBER=$(git rev-list --count HEAD)
COMMIT_HASH=$(git rev-parse HEAD)

# Path to the YAML file
YAML_FILE="~/Taphonomy-Rig/config.yaml"

# Update the YAML file with the commit hash
python3 ~/Taphonomy-Rig/update_version.py $YAML_FILE $COMMIT_HASH $VERSION_NUMBER