import argparse
from tqdm import tqdm
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from schema import NutritionSchema,Prompt
from utils import DataUtils,EvaluateUtils

def main(**kwargs):
    ### set parameter
    model_name=kwargs["model_name"]
    os_type=kwargs["os_type"]
    ollama_port=kwargs["ollama_port"]

    ### load test dataset
    test_dataset=DataUtils.load_test_dataset(os_type=os_type)
    img_dict=test_dataset["img"]
    label_dict=test_dataset["label"]
    img_list=sorted(img_dict.items(),key=lambda x:x[0])
    label_list=sorted(label_dict.items(),key=lambda x:x[0])

    ### load and set llm with structured output
    llm=ChatOllama(
        model=model_name,
        base_url=f"http://127.0.0.1:{ollama_port}",
        temperature=0
    )
    structured_llm=llm.with_structured_output(schema=NutritionSchema)

    ### evaluate llm
    llm_results=[]
    for food_id,img_base64 in tqdm(img_list,desc=f"Evaluate llm..."):
        # set message for llm
        messages=[
            SystemMessage(content=Prompt.NUTRITION_EXTRACTION_SYSTEM_PROMPT),
            HumanMessage(
                content=[
                    {
                        "type":"text",
                        "text":Prompt.NUTRITION_EXTRACTION_HUMAN_PROMPT
                    },
                    {
                        "type":"image_url",
                        "image_url": (
                            f"data:image/png;base64,{img_base64}"
                        )
                    }
                ]
            )
        ]
        try:
            response:AIMessage=structured_llm.invoke(messages)
        except Exception as e: 
            # 파싱 실패 시
            """
            """
        result=response.model_dump() # dict
        print(result)
        break
        llm_results.append(result)

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
    parser.add_argument("--os_type",
        type=str,
        choices=["linux","macos"],
        default=f"linux"
    )
    parser.add_argument("--ollama_port",type=int,default=11434)
    args=parser.parse_args()
    app_config={
        "model_name":args.model_name,
        "os_type":args.os_type,
        "ollama_port":args.ollama_port
    }
    main(**app_config)