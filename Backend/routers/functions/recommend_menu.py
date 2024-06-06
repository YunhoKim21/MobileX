import os
import requests

from fastapi import APIRouter

from llm.chat import build
from llm.store import LLMStore
from models.recommend_menu import InputModel, OutputModel

# Configure API router
router = APIRouter(
    tags=['functions'],
)

# Configure metadata
NAME = os.path.basename(__file__)[:-3]

# Configure resources
store = LLMStore()

###############################################
#                   Actions                   #
###############################################


@router.post(f'/func/{NAME}')
async def call_recommend_menu(model: InputModel) -> OutputModel:
    API_KEY = ""
    WEATHER_BASE_URL = "https://api.openweathermap.org/data/3.0/onecall?"

    def get_weather():
        lat, lon = "35.228924103442424", "126.84744032898854"

        weather_url = WEATHER_BASE_URL + f"lat={lat}&lon={lon}&appid={API_KEY}"
        weather_response = requests.get(weather_url)
        weather_response_json = weather_response.json()

        if weather_response.status_code != 200 or len(weather_response_json) == 0:
            print("Failed to get weather data")
            return

        feels_like_in_c = round(weather_response_json['current']['feels_like'] - 273.15, 2)

        return feels_like_in_c

    temperature = str(get_weather())
    
    # Create a LLM chain
    chain = build(
        name=NAME,
        llm=store.get(model.llm_type),
    )

    return OutputModel(
        output=chain.invoke({
            'input_context': f'''
                * Recent Menu: {model.recent_menu}
                * Price: {model.price}
                * Allergy: {model.allergy}
                * Temperature: {temperature}
            ''',
        }),
    )
