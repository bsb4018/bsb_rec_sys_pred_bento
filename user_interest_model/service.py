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
    with bentoml.monitor("course_recommeder_by_interest") as mon:
        mon.log(input_dict["web_dev"], name="web_dev", role="interest", data_type="numerical")
        mon.log(input_dict["data_sc"], name="data_sc", role="interest", data_type="numerical")
        mon.log(input_dict["data_an"], name="data_an", role="interest", data_type="numerical")
        mon.log(input_dict["game_dev"], name="game_dev", role="interest", data_type="numerical")
        mon.log(input_dict["mob_dev"], name="mob_dev", role="interest", data_type="numerical")
        mon.log(input_dict["program"], name="program", role="interest", data_type="numerical")
        mon.log(input_dict["cloud"], name="cloud", role="interest", data_type="numerical")

        #print(input_dict)
        input_dict = input_dict.dict()
        #print(input_dict)
        values_list = (list(input_dict.values()))
        #print(values_list)
        recommended_list = recommender_runner_interest.async_run(values_list)
        mon.log(recommended_list, name="recommended_courses", role="prediction", data_type="categorical")

    return await recommended_list