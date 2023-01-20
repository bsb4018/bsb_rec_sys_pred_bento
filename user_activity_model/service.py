import bentoml
from typing import List


recommender_runner_activity = bentoml.picklable_model.get("recommender_activity").to_runner()
svc_activity = bentoml.Service("course_recommeder_by_activity", runners=[recommender_runner_activity])


@svc_activity.api(input=bentoml.io.JSON(), output=bentoml.io.JSON())
async def course_recommend_activity(input_arr):
    return await recommender_runner_activity.async_run(input_arr)
