from typing import Literal
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableBranch,RunnableLambda,RunnablePassthrough
from langchain_core.exceptions import OutputParserException
from pydantic import ValidationError
from schema import FoodImgClassSchema,NutritionSchema
from .prompt_module import Prompt

class Chain:
    @staticmethod
    def get_evaluate_LLM_chain(
            model_name:Literal[
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
            ollama_port:int=11434
        ):
        """
        """
        ### load ChatPromptTemplate
        prompt=Prompt.get_nutrition_extraction_prompt()

        ### load and set llm with structured output
        llm=ChatOllama(
            model=model_name,
            base_url=f"http://127.0.0.1:{ollama_port}",
            temperature=0
        )
        structured_llm=llm.with_structured_output(schema=NutritionSchema)

        ### connect chain
        chain=prompt | structured_llm
        return chain

    @staticmethod
    def get_food_info_etl_chain(
            model_name:Literal[
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
            ollama_port:int=11434
        ):
        """
        img_base64를 입력받아 분류 후 영양성분을 추출하는 chain을 반환.
        각 단계의 스키마 오류는 최초 호출 이후 최대 3회 재시도.
        분류 결과가 0이거나 재시도가 소진되면 None을 반환.
        """
        ### load ChatPromptTemplate
        img_classification_prompt=Prompt.get_img_classification_prompt()
        nutrition_extraction_prompt=Prompt.get_nutrition_extraction_prompt()

        ### load and set llm with structured output
        llm=ChatOllama(
            model=model_name,
            base_url=f"http://127.0.0.1:{ollama_port}",
            temperature=0
        )
        img_classification_llm=llm.with_structured_output(schema=FoodImgClassSchema)
        nutrition_extraction_llm=llm.with_structured_output(schema=NutritionSchema)

        ### connect chain
        schema_errors=(OutputParserException,ValidationError)
        skip_image=RunnableLambda(lambda _:None)
        img_classification_chain=(
            img_classification_prompt
            | img_classification_llm
        ).with_retry(
            retry_if_exception_type=schema_errors,
            stop_after_attempt=4
        ).with_fallbacks(
            [skip_image],exceptions_to_handle=schema_errors
        )
        nutrition_extraction_chain=(
            nutrition_extraction_prompt
            | nutrition_extraction_llm
        ).with_retry(
            retry_if_exception_type=schema_errors,
            stop_after_attempt=4
        ).with_fallbacks(
            [skip_image],exceptions_to_handle=schema_errors
        )
        chain=(
            RunnablePassthrough.assign(classification=img_classification_chain)
            | RunnableBranch(
                (
                    lambda inputs:inputs["classification"] is not None
                    and inputs["classification"].label==1,
                    nutrition_extraction_chain
                ),
                skip_image
            )
        )
        return chain
