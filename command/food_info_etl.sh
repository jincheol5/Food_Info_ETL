#!/bin/bash
set -e

python -m app.food_info_etl --model_name gemma4:e4b --os_type macos --db_port 27017 --ollama_port 11434