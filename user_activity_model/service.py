import bentoml
from typing import List
from pydantic import BaseModel
class User_Id(BaseModel):
    user_id: int

recommender_runner_activity = bentoml.picklable_model.get("recommender_activity").to_runner()
svc_activity = bentoml.Service("course_recommeder_by_activity", runners=[recommender_runner_activity])


@svc_activity.api(input=bentoml.io.JSON(pydantic_model=User_Id), output=bentoml.io.JSON())
async def course_recommend_activity(input_arr:User_Id):
    return await recommender_runner_activity.async_run(input_arr.dict())
