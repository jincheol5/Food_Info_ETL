import argparse
from tqdm import tqdm
from module import MongoDBInterface,Chain
from utils import DataUtils

def main(**kwargs):
    ### set db and load unextracted food_ids
    db_port=kwargs["db_port"]
    db=MongoDBInterface(port=db_port)
    food_ids=db.get_unextracted_food()

    ### load unextracted food_ids img
    os_type=kwargs["os_type"]
    img_dict=DataUtils.load_food_img(
        food_ids=food_ids,
        os_type=os_type
    )

    ### set food_info_etl chain
    model_name=kwargs["model_name"]
    ollama_port=kwargs["ollama_port"]
    food_info_etl_chain=Chain.get_food_info_etl_chain(
        model_name=model_name,
        ollama_port=ollama_port
    )

    ### Food Info ETL
    print(f"Start {len(food_ids)} Food Info ETL!")
    nutrition_info={}
    try:
        for food_id,img_list in tqdm(
                img_dict.items(),
                total=len(img_dict.keys()),
                desc=f"Food Info ETL..."
            ):
            for img_base64 in img_list:
                chain_result=food_info_etl_chain.invoke({"img_base64":img_base64})
                if chain_result is None:
                    continue
                nutrition_info[food_id]=chain_result.model_dump(mode="json")
                break
    finally:
        try:
            success_count=db.update_nutrition_info(nutrition_info=nutrition_info)
            print(f"Complete to extracted {success_count} Food Info ETL!")
        finally:
            db.disconnect_db()

if __name__=="__main__":
    """
    Execute app
    """
    parser=argparse.ArgumentParser()
    parser.add_argument("--model_name",
        type=str,
        choices=[
            "qwen3-vl:8b",
            "qwen3.5:0.8b",
            "qwen3.5:2b",
            "qwen3.5:9b",
            "gemma3:4b",
            "gemma3:12b",
            "gemma4:e2b",
            "gemma4:e4b",
            "gemma4:12b",
            "minicpm-v:8b",
            "minicpm-v4.6:1b",
            "llama3.2-vision:11b"
        ],
        default=f"gemma4:e4b"
    )
    parser.add_argument("--os_type",
        type=str,
        choices=["linux","macos"],
        default=f"linux"
    )
    parser.add_argument("--db_port",type=int,default=27017)
    parser.add_argument("--ollama_port",type=int,default=11434)
    args=parser.parse_args()
    app_config={
        "model_name":args.model_name,
        "os_type":args.os_type,
        "db_port":args.db_port,
        "ollama_port":args.ollama_port
    }
    main(**app_config)
