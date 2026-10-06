from pydantic import BaseModel,ConfigDict,Field,field_validator
from enum import Enum
from typing import Literal

class FoodImageClassifierSchema(BaseModel):
    label:Literal[0,1]=Field(
        description=f"1 if at least one nutrition panel entry has a reliably readable nutrient or energy name, numeric amount, and unit; 0 otherwise."
    )
    model_config=ConfigDict(extra="forbid",strict=True)

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
