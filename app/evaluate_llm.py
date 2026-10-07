import argparse
import time
from tqdm import tqdm
from module import Chain
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

    ### set evaluation chain
    chain=Chain.get_evaluate_LLM_chain(model_name=model_name,ollama_port=ollama_port)

    ### evaluate llm
    correct_schema=0
    execute_times=[]
    llm_results=[]
    labels=[]
    for food_id,img_base64 in tqdm(img_list,desc=f"Evaluate llm..."):
        start_time=time.perf_counter()
        try:
            response=chain.invoke({"img_base64":img_base64})
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
    print(f"Evaluate {model_name}")
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
            "gemma4:12b",
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
