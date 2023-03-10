import os,sys
from typing import List
from utils import load_object
from constants import PRODUCTION_MODEL_FILE_PATH,INTERACTIONS_MATRIX_FILE_PATH,INTERACTIONS_MODEL_FILE_PATH,FEATURE_STORE_FILE_PATH,AWS_ACCESS_KEY_ID_ENV_KEY,AWS_ACCESS_KEY_ID_ENV_KEY,S3_MODEL_STORE_BUCKET
from feast import FeatureStore
import pandas as pd
from exception import PredictionException
import bentoml
from connections import StorageConnection

def recommend_by_similar_user_activity(item_dict) -> List[str]:
    try:
        #load model from artifact
        storage_connection = StorageConnection()
        storage_connection.download_production_model_s3()
        storage_connection.get_feature_store_s3()
        timestamps = list(map(int, os.listdir(PRODUCTION_MODEL_FILE_PATH)))
        latest_timestamp = max(timestamps)
        latest_production_interaction_model = os.path.join(PRODUCTION_MODEL_FILE_PATH, f"{latest_timestamp}", INTERACTIONS_MODEL_FILE_PATH)
        latest_production_interaction_matrix = os.path.join(PRODUCTION_MODEL_FILE_PATH, f"{latest_timestamp}", INTERACTIONS_MATRIX_FILE_PATH)
        interaction_model = load_object(latest_production_interaction_model)
        interaction_matrix = load_object(latest_production_interaction_matrix)

        #get the user from input
        user_id = item_dict["user_id"]

        #get recommendation 
        ids, scores = interaction_model.recommend(user_id, interaction_matrix[user_id], N=5, filter_already_liked_items=False)
        cidx = ids.tolist()

        store = FeatureStore(repo_path=FEATURE_STORE_FILE_PATH)
        course_data = store.get_online_features(features = \
            ["courses_df_feature_view:course_id",\
                "courses_df_feature_view:course_name"],
                    entity_rows=[
                        {"course_feature_id": cidx[0]},
                        {"course_feature_id": cidx[1]},
                        {"course_feature_id": cidx[2]},
                        {"course_feature_id": cidx[3]},
                        {"course_feature_id": cidx[4]}
                    ]).to_dict()

        coursesdf = pd.DataFrame(course_data)

        c=0
        recmd_courses_list = []
        for id in cidx:
            if c == 5:
                break
            c += 1
            recmnd_course = coursesdf[coursesdf["course_id"] == id]["course_name"].values
            recmd_courses_list.append(recmnd_course)


        new_recommend_list = []
        for course in recmd_courses_list:
            for value in course:
                new_recommend_list.append(value)

        #use recommend function of the model to get the recommendation
        if not recmd_courses_list:
            generated_recomendations = ["No Recommendations Available"]
            return generated_recomendations
        else:
            return new_recommend_list
    except Exception as e:
        raise PredictionException(e,sys)


def save_activity_model_bento():
    try:
        saved_model_interactions = bentoml.picklable_model.save_model(\
            "recommender_activity", recommend_by_similar_user_activity, \
                signatures={"__call__": {"batchable": True}}
            )
        print(f"Activity Model saved: {saved_model_interactions}")

        bentoml.models.export_model('recommender_interest:latest', 'bentoStore')
        aws_user = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
        aws_secret = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
        aws_bento_store_bucket = S3_MODEL_STORE_BUCKET
        bentoml.models.export_model('recommender_interest:latest', aws_bento_store_bucket, protocol='s3', \
            subpath='activity-model',user=aws_user, passwd=aws_secret,\
                params={'acl': 'public-read', 'cache-control': 'max-age=2592000,public'})

    except Exception as e:
        raise PredictionException(e,sys)


if __name__ == "__main__":
    save_activity_model_bento()