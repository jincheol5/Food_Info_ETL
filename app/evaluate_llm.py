import argparse
import time
from tqdm import tqdm
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage,HumanMessage
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

    ### load and set llm with structured output
    llm=ChatOllama(
        model=model_name,
        base_url=f"http://127.0.0.1:{ollama_port}",
        temperature=0
    )
    structured_llm=llm.with_structured_output(schema=NutritionSchema)

    ### evaluate llm
    correct_schema=0
    execute_times=[]
    llm_results=[]
    labels=[]
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
        start_time=time.perf_counter()
        try:
            response:NutritionSchema=structured_llm.invoke(messages)
            llm_result=response.model_dump()
            llm_results.append(llm_result)
            labels.append(label_dict[food_id])
            correct_schema+=1
        except Exception as e: 
            pass
        end_time=time.perf_counter()
        execute_times.append(float(end_time-start_time))

    ### postprocess llm_results
    llm_results=EvaluateUtils.postprocess_llm_result(llm_results=llm_results)

    ### Mean Time, Accuracy
    mean_execute_time=sum(execute_times)/len(execute_times) if execute_times else 0.0
    schema_acc=correct_schema/len(img_list) if img_list else 0.0
    value_acc=EvaluateUtils.evaluate_nutrition_value(
        llm_results=llm_results,
        labels=labels
    )
    unit_acc=EvaluateUtils.evaluate_nutrition_unit(
        llm_results=llm_results,
        labels=labels
    )
    print(f"Mean execute time: {mean_execute_time}")
    print(f"Schema ACC: {schema_acc}")
    print(f"Value ACC: {value_acc}")
    print(f"Unit ACC: {unit_acc}")

if __name__=="__main__":
    """
    Execute app
    """
    parser=argparse.ArgumentParser()
    parser.add_argument("--model_name",
        type=str,
        choices=[
            # Qwen
            "qwen3-vl:8b",
            "qwen3.5:0.8b",
            "qwen3.5:2b",
            "qwen3.5:9b",
            # Gemma
            "gemma3:4b",
            "gemma3:12b",
            "gemma4:e2b",
            "gemma4:e4b",
            # OpenBMB
            "minicpm-v:8b",
            "minicpm-v4.6:1b",
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
