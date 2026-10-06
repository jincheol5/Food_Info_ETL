#!/bin/bash
set -e

python -m app.evaluate_llm --model_name qwen3-vl:8b --os_type linux
python -m app.evaluate_llm --model_name qwen3.5:0.8b --os_type linux
python -m app.evaluate_llm --model_name qwen3.5:2b --os_type linux
python -m app.evaluate_llm --model_name qwen3.5:9b --os_type linux

python -m app.evaluate_llm --model_name gemma3:4b --os_type linux
python -m app.evaluate_llm --model_name gemma3:12b --os_type linux
python -m app.evaluate_llm --model_name gemma4:e2b --os_type linux
python -m app.evaluate_llm --model_name gemma4:e4b --os_type linux
python -m app.evaluate_llm --model_name gemma4:12b --os_type linux

python -m app.evaluate_llm --model_name minicpm-v:8b --os_type linux
python -m app.evaluate_llm --model_name minicpm-v4.6:1b --os_type linux

python -m app.evaluate_llm --model_name llama3.2-vision:11b --os_type linux