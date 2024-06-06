from typing import Literal

from pydantic import BaseModel, Field


class InputModel(BaseModel):
    recent_menu : str = Field(
        default='라면',
        description= '최근에 먹은 메뉴 카테고리 안에서 추천해드려요!'
    )
    price : Literal[
        '1만원 이하',
        '1만원 ~ 2만원',
        '2만원 ~ 3만원',
        '3만원 이상',
    ] = Field(
        default='1만원 ~ 2만원',
    )
    allergy : str = Field(
        default='땅콩',
    )
    llm_type: Literal['chatgpt', 'huggingface'] = Field(
        alias='Large Language Model Type',
        description='사용할 LLM 종류',
        default='chatgpt',
    )


class OutputModel(BaseModel):
    output : str = Field(  
        description='이건 어때요?',
    )


