# Overview
<p align="center">
  <img src="figures/ex.svg" width="800">
</p>

# Workflow
<p align="center">
  <img src="figures/workflow.svg" width="800">
</p>

# What is Food_Info_ETL?
Food_Info_ETL은 LLM 기반 식품 이미지 내 영양성분 정보 ETL 자동화 파이프라인 입니다.

LangChain을 사용하여 식품 이미지 로드 → LLM 기반 정보 추출 및 변환 → 결과 검증 → MongoDB 적재 과정으로 ETL 파이프라인을 구성하였습니다.

LLM은 Ollama를 활용해 이미지 입력이 가능한 모델들을 비교 분석하여 Qwen3.5-9b or Gemma4-e2b로 구성하였습니다.

# Evaluation

| LLM | Mean Execute Time (second) | Schema ACC (%) | Value ACC (%) | Unit ACC (%) |
|:---:|:---:|:---:|:---:|:---:|
| qwen3-vl:8b | 15.38 | 70.00 | 97.83 | 99.56 |
| qwen3.5:0.8b | 10.08 | 13.33 | 75.00 | 93.18 |
| qwen3.5:2b | 11.01 | 40.00 | 96.21 | 99.24 |
| qwen3.5:9b | 21.58 | 50.00 | 98.78 | 99.39 |
| gemma3:4b | 2.27 | 100.00 | 43.03 | 94.54 |
| gemma3:12b | 4.36 | 100.00 | 61.21 | 90.30 |
| gemma4:e2b | 4.63 | 100.00 | 66.36 | 89.69 |
| gemma4:e4b | 4.93 | 100.00 | 87.27 | 96.66 |
| gemma4:12b | 9.84 | 96.66 | 72.72 | 97.80 |
| minicpm-v:8b | 29.84 | 100.00 | 56.06 | 97.87 |
| minicpm-v4.6:1b | 12.11 | 86.66 | 47.20 | 87.76 |
| llama3.2-vision:11b | 1.32 | 0.00 | 0.00 | 0.00 |

