from pydantic import BaseModel,ConfigDict
from enum import Enum

class ServingUnit(str,Enum):
    g="g"
    ml="ml"

class NutritionUnit(str,Enum):
    g="g"
    mg="mg"
    kcal="kcal"

class ServingSize(BaseModel):
    value:float|None
    unit:ServingUnit|None
    model_config=ConfigDict(extra="forbid")

class NutritionValue(BaseModel):
    value:float|None
    unit:NutritionUnit|None
    model_config=ConfigDict(extra="forbid")

class NutritionSchema(BaseModel):
    totalServingSize:ServingSize
    servingSize:ServingSize
    calories:NutritionValue
    sodium:NutritionValue
    carbohydrate:NutritionValue
    sugar:NutritionValue
    fat:NutritionValue
    transFat:NutritionValue
    saturatedFat:NutritionValue
    cholesterol:NutritionValue
    protein:NutritionValue
    model_config=ConfigDict(extra="forbid")