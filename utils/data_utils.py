import os
import json
from PIL import Image

BASE_PATH=os.path.join("/mnt/usb","data","chronolab")
class DataUtils:
    @staticmethod
    def load_test_dataset()->dict[str,dict]:
        img_dir_path=os.path.join(BASE_PATH,"test_food_img")
        label_dir_path=os.path.join(BASE_PATH,"test_food_img_label")

        ### load test_food_img files to dict
        img_dict={
            os.path.splitext(file_name)[0]:Image.open(
                os.path.join(img_dir_path,file_name)
            )
            for file_name in os.listdir(img_dir_path)
            if file_name.lower().endswith(".png")
        }

        ### load test_food_img_label files to dict
        label_dict={}
        for file_name in os.listdir(label_dir_path):
            if file_name.lower().endswith(".json"):
                file_path=os.path.join(label_dir_path, file_name)
                file_id=os.path.splitext(file_name)[0]
                with open(file_path,"r",encoding="utf-8") as f:
                    label_dict[file_id]=json.load(f)
        return {
            "img":img_dict,
            "label":label_dict
        }