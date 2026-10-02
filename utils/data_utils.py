import os
import json
import base64
from typing import Literal
from PIL import Image

LINUX_PATH=os.path.join("/mnt/usb","data","chronolab")
MACOS_PATH=os.path.join("/Volumes/Data_USB","data","chronolab")
class DataUtils:
    @staticmethod
    def load_test_dataset(
            os_type:Literal["linux","macos"]="linux"
        )->dict[str,dict]:
        ### set data path
        match os_type:
            case "linux":
                img_dir_path=os.path.join(LINUX_PATH,"test_food_img")
                label_dir_path=os.path.join(LINUX_PATH,"test_food_img_label")
            case "macos":
                img_dir_path=os.path.join(MACOS_PATH,"test_food_img")
                label_dir_path=os.path.join(MACOS_PATH,"test_food_img_label")

        ### load test_food_img files to dict (base64)
        img_dict={}
        for file_name in os.listdir(img_dir_path):
            if file_name.lower().endswith(".png"):
                file_path=os.path.join(img_dir_path,file_name)
                file_id=os.path.splitext(file_name)[0]
                with open(file_path,"rb") as f:
                    img_dict[file_id]=base64.b64encode(f.read()).decode("utf-8")

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