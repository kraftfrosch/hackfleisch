#!/bin/bash

# Activate conda environment
# source ~/.conda/etc/profile.d/conda.sh
conda activate cdtmhack

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to the project root directory
cd "$PROJECT_ROOT"

# Start the video agent
python src/external_agents/video_agent.py start
