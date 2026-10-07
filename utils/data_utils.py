import os
import json
import base64
from typing import Literal
from PIL import Image

LINUX_PATH=os.path.join("/mnt/usb","data","chronolab")
MACOS_PATH=os.path.join("/Volumes/Data_USB","data","chronolab")
class DataUtils:
    @staticmethod
    def get_all_food_ids(
            os_type:Literal["linux","macos"]="linux"
        )->list[str]:
        """
        raw_food_img 바로 아래의 모든 폴더명을 정렬된 리스트로 반환.
        """
        match os_type:
            case "linux":
                img_dir_path=os.path.join(LINUX_PATH,"raw_food_img")
            case "macos":
                img_dir_path=os.path.join(MACOS_PATH,"raw_food_img")
            case _:
                raise ValueError(f"Unsupported os_type: {os_type}")
        return sorted(
            name for name in os.listdir(img_dir_path)
            if os.path.isdir(os.path.join(img_dir_path,name))
        )

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

    @staticmethod
    def load_food_img(
            food_ids:list,
            os_type:Literal["linux","macos"]="linux"
        )->dict:
        """
        food_ids에 대한 image들을 Base64로 변환하여 load.
        food_id 하나에 여러 개의 image들이 존재.

        Return:
            img_dict:
                key: food id
                value: food_img (base64) list
        """
        match os_type:
            case "linux":
                img_dir_path=os.path.join(LINUX_PATH,"raw_food_img")
            case "macos":
                img_dir_path=os.path.join(MACOS_PATH,"raw_food_img")
        img_dict={}
        for food_id in food_ids:
            food_id=str(food_id)
            food_img_path=os.path.join(img_dir_path,food_id)
            food_img_list=[]
            for file_name in sorted(os.listdir(food_img_path)):
                file_path=os.path.join(food_img_path,file_name)
                if os.path.isfile(file_path) and file_name.lower().endswith((".png")):
                    with open(file_path,"rb") as f:
                        food_img_list.append(base64.b64encode(f.read()).decode("utf-8"))
            img_dict[food_id]=food_img_list
        return img_dict
