import json
from pydantic import ValidationError
from schema import NutritionSchema

class EvaluateUtils:
    @staticmethod
    def postprocess_llm_result(llm_results:list[dict])->list[dict]:
        """
        LLM 출력 결과 후처리

        - Value: Null(None) -> 0.0
        - Unit: Null(None) -> "g"

        Input:
            llm_results: LLM structured output 결과의 dict 리스트
        Return:
            processed_results: 후처리된 JSON 문자열 리스트
        """
        processed_results=[]
        for result in llm_results:
            processed_result={}
            for field,data in result.items():
                value=data.get("value")
                unit=data.get("unit")

                ### Null value 처리
                if value is None:
                    value = 0.0

                ### Null unit 처리
                if unit is None:
                    unit = "g"

                processed_result[field] = {
                    "value":value,
                    "unit":unit
                }

            processed_results.append(processed_result)

        return processed_results

    @staticmethod
    def evaluate_json_schema(llm_results:list[str])->float:
        correct=0
        for result in llm_results:
            try:
                NutritionSchema.model_validate_json(result)
                correct+=1
            except ValidationError:
                pass
        accuracy=correct/len(llm_results)
        return accuracy

    @staticmethod
    def evaluate_nutrition_value(
            llm_results:list[dict],
            labels:list[dict]
        )->float:
        """
        LLM이 추출한 영양성분 value의 정확도 계산.
        각 sample의 모든 영양성분 value를 label과 비교하여 정확히 일치한 value의 비율을 반환.
        """
        fields=[
            "totalServingSize",
            "servingSize",
            "calories",
            "sodium",
            "carbohydrate",
            "sugar",
            "fat",
            "transFat",
            "saturatedFat",
            "cholesterol",
            "protein"
        ]
        correct=0
        total=0
        for llm_result,label in zip(llm_results,labels):
            for field in fields:
                total+=1
                pred_value=getattr(llm_result,field).value
                label_value=label[field]["value"]
                if pred_value==label_value:
                    correct+=1
        if total==0:
            return 0.0
        return correct/total

    @staticmethod
    def evaluate_nutrition_unit(
            llm_results:list[dict],
            labels:list[dict]
        )->float:
        """
        LLM이 추출한 영양성분 unit의 정확도 계산.
        각 sample의 모든 영양성분 unit을 label과 비교하여 정확히 일치한 unit의 비율을 반환.
        """
        fields=[
            "totalServingSize",
            "servingSize",
            "calories",
            "sodium",
            "carbohydrate",
            "sugar",
            "fat",
            "transFat",
            "saturatedFat",
            "cholesterol",
            "protein"
        ]
        correct=0
        total=0
        for llm_result,label in zip(llm_results,labels):
            for field in fields:
                total+=1
                pred_unit=getattr(llm_result,field).unit
                label_unit=label[field]["unit"]
                if pred_unit==label_unit:
                    correct+=1
        if total==0:
            return 0.0
        return correct/total
