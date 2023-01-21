import bentoml
from typing import List
from pydantic import BaseModel
class Interest_Item(BaseModel):
    web_dev:int
    data_sc:int
    data_an:int
    game_dev:int
    mob_dev:int
    program:int
    cloud:int


recommender_runner_interest = bentoml.picklable_model.get("recommender_interest").to_runner()
svc_interest = bentoml.Service("course_recommeder_by_interest", runners=[recommender_runner_interest])

@svc_interest.api(input=bentoml.io.JSON(pydantic_model=Interest_Item), output=bentoml.io.JSON())
async def course_recommend_interest(input_dict:Interest_Item):
    print(input_dict)
    input_dict = input_dict.dict()
    print(input_dict)
    values_list = (list(input_dict.values()))
    print(values_list)

    return await recommender_runner_interest.async_run(values_list)