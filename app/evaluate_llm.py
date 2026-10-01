import argparse
from langchain_ollama import ChatOllama


def main(**kwargs):
    """
    """

if __name__=="__main__":
    """
    Execute app
    """
    parser=argparse.ArgumentParser()
    parser.add_argument("--model_name",
        type=str,
        choices=[
            "deepseek-ocr:3b",
            "qwen2.5vl:7b"
            "qwen3-vl:8b"
            "qwen3.5:9b",
            "gemma3:4b"
            "gemma4:e4b"
        ],
        default=f"qwen3.5:9b"
    )
    args=parser.parse_args()
    app_config={
        "model_name":args.model_name
    }
    main(**app_config)