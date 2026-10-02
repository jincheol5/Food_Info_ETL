import argparse
from langchain_ollama import ChatOllama

def main(**kwargs):
    model_name=kwargs["model_name"]
    llm=ChatOllama(
        model=model_name,
        temperature=0
    )
    response=llm.invoke("안녕하세요. 자기소개해주세요.")
    print(response.content)

if __name__=="__main__":
    """
    Execute app
    """
    parser=argparse.ArgumentParser()
    parser.add_argument("--model_name",
        type=str,
        choices=[
            # Qwen
            "qwen2.5vl:7b"
            "qwen3-vl:8b"
            "qwen3.5:9b",
            # Gemma
            "gemma3:4b",
            "gemma4:e2b"
            "gemma4:e4b",
            # OpenBMB
            "minicpm-v:8b",
            # Meta
            "llama3.2-vision:11b"
        ],
        default=f"gemma4:e4b"
    )
    args=parser.parse_args()
    app_config={
        "model_name":args.model_name
    }
    main(**app_config)