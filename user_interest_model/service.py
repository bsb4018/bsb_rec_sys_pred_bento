import bentoml
from typing import List


recommender_runner_interest = bentoml.picklable_model.get("recommender_interest").to_runner()
svc_interest = bentoml.Service("course_recommeder_by_interest", runners=[recommender_runner_interest])

@svc_interest.api(input=bentoml.io.JSON(), output=bentoml.io.JSON())
async def course_recommend_interest(input_arr):
    return await recommender_runner_interest.async_run(input_arr)