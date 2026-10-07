import argparse
from module import MongoDBInterface
from utils import DataUtils

def main(**kwargs):
    ### load all food_ids
    os_type=kwargs["os_type"]
    food_ids=DataUtils.get_all_food_ids(os_type=os_type)
    print(f"Length of all foods: {len(food_ids)}")

    ### insert to db
    db_port=kwargs["db_port"]
    db=MongoDBInterface(port=db_port)
    db.insert_food(food_ids=food_ids)
    db.disconnect_db()
    print(f"Complete to insert food_ids!")

if __name__=="__main__":
    """
    Execute app
    """
    parser=argparse.ArgumentParser()
    parser.add_argument("--os_type",
        type=str,
        choices=["linux","macos"],
        default=f"linux"
    )
    parser.add_argument("--db_port",type=int,default=27017)
    args=parser.parse_args()
    app_config={
        "os_type":args.os_type,
        "db_port":args.db_port
    }
    main(**app_config)