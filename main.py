from fastapi import FastAPI
from models.body import DataBody, DataDict
from pydantic import parse_obj_as
from typing import List
import requests
import json
import pandas as pd

app = FastAPI()

@app.post("/chat/completions")
async def openai_chat(data: DataBody):
    model = data.model
    parsed_data = parse_obj_as(List[DataDict], data.messages)
    parsed_data = parsed_data[0]
    print(type(parsed_data))
    def create_serving_json(data):
        return {'inputs': {name: data[name].tolist() for name in data.keys()} if isinstance(data, dict) else data.tolist()}

    def create_completion(dataset):
        url = 'https://adb-.17.azuredatabricks.net/serving-endpoints/mistral-7b-llm-a100/invocations'
        headers = {'Authorization': f'Bearer ----', 
                'Content-Type': 'application/json'}
        ds_dict = {'dataframe_split': dataset.to_dict(orient='split')} if isinstance(dataset, pd.DataFrame) else create_serving_json(dataset)
        data_json = json.dumps(ds_dict, allow_nan=True)
        response = requests.request(method='POST', headers=headers, url=url, data=data_json)
        if response.status_code != 200:
            raise Exception(f'Request failed with status {response.status_code}, {response.text}')

        return response.json()
    
    def create_df(parsed_data):
        df = pd.DataFrame(index = [
                0
            ],
            columns = [
                "prompt",
                "temperature",
                "max_new_tokens"
            ],
            data =  [
                [
                    parsed_data.prompt,
                    parsed_data.temperature,
                    parsed_data.max_new_tokens
                ]
            ])
        print(df)
        return df
    df = create_df(parsed_data)
    response = create_completion(df)
    return response

# @app.post("/chat/completions")
# async def get_model(data: DataBody):
#     parsed_data = parse_obj_as(List[DataDict], data.messages)
#     return parsed_data[0]

@app.get("/")
async def root():
    return {"message": "Jesus is King!"}