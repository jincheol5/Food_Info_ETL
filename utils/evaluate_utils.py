import json
from pydantic import ValidationError
from schema import NutritionSchema

class EvaluateUtils:
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
            llm_results:list[str],
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
            try:
                pred=NutritionSchema.model_validate_json(llm_result)
            except ValidationError:
                # JSON 파싱 또는 Schema 검증 실패 시 해당 sample의 모든 field를 오답 처리
                total+=len(fields)
                continue

            for field in fields:
                total+=1
                pred_value=getattr(pred,field).value
                label_value=label[field]["value"]
                if pred_value==label_value:
                    correct+=1
        if total==0:
            return 0.0
        return correct/total