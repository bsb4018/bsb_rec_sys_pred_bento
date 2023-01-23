from typing import List
import os,sys
import random
from connections import MongoDBClient
from exception import PredictionException
import bentoml
from constants import AWS_ACCESS_KEY_ID_ENV_KEY,AWS_ACCESS_KEY_ID_ENV_KEY,S3_MODEL_STORE_BUCKET

def _find_courses_interest(tag: str):
    try:
        mongodbc = MongoDBClient()
        client = mongodbc.client
        connection = mongodbc.dbcollection        
        randomnos = random.randint(0,2)
        courses1 = connection.find({'category': tag}, {'_id': 0, 'course_name':1}).limit(1).skip(randomnos).next().get('course_name')
        randomnos = random.randint(3,5)
        courses2 = connection.find({'category': tag}, {'_id': 0, 'course_name':1}).limit(1).skip(randomnos).next().get('course_name')
        randomnos = random.randint(6,8)
        courses3 = connection.find({'category': tag}, {'_id': 0, 'course_name':1}).limit(1).skip(randomnos).next().get('course_name')
            
        recommended_list = []
        recommended_list.append(courses1)
        recommended_list.append(courses2)
        recommended_list.append(courses3)
        
        #clist = dict(courses2.next())
        #for _,val in clist.items():
        #    recommended_list.append(val)
        #clist = dict(courses3.next())
        #for _,val in clist.items():
        #    recommended_list.append(val)

        return recommended_list
    except Exception as e:
        raise PredictionException(e,sys)


def recommend_by_similar_interest(item_values) -> List[List[str]]:
    try:
        print(item_values)
        
        item_dict = {
        "web_dev":item_values[0],
        "data_sc":item_values[1],
        "data_an":item_values[2],
        "game_dev":item_values[3],
        "mob_dev":item_values[4],
        "program":item_values[5],
        "cloud":item_values[6],
        }

        print(item_dict)
        
        courses = []
        if item_dict.get("web_dev") == 1:
            tag = "web_dev"
            courses.append(_find_courses_interest(tag))
        if item_dict.get("data_sc") == 1:
            tag = "data_sc"
            courses.append(_find_courses_interest(tag))
        if item_dict.get("data_an") == 1:
            tag = "data_an"
            courses.append(_find_courses_interest(tag))
        if item_dict.get("game_dev") == 1:
            tag = "game_dev"
            courses.append(_find_courses_interest(tag))
        if item_dict.get("mob_dev") == 1:
            tag = "mob_dev"
            courses.append(_find_courses_interest(tag))
        if item_dict.get("program") == 1:
            tag = "program"
            courses.append(_find_courses_interest(tag))
        if item_dict.get("cloud") == 1:
            tag = "cloud"
            courses.append(_find_courses_interest(tag))      
        return courses
    except Exception as e:
        raise PredictionException(e,sys)


def save_interest_model_bento():
        try:
            saved_model_courses = bentoml.picklable_model.save_model("recommender_interest", \
                recommend_by_similar_interest, \
                    signatures={"__call__": {"batchable": True}})
            print(f"Interest Model saved: {saved_model_courses}")

            bentoml.models.export_model('recommender_interest:latest', 'bentoStore')
            aws_user = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
            aws_secret = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
            aws_bento_store_bucket = S3_MODEL_STORE_BUCKET
            bentoml.models.export_model('recommender_interest:latest', aws_bento_store_bucket, protocol='s3', \
                subpath='interest-model',user=aws_user, passwd=aws_secret,\
                    params={'acl': 'public-read', 'cache-control': 'max-age=2592000,public'})
        
        except Exception as e:
            raise PredictionException(e,sys)


if __name__ == "__main__":
    save_interest_model_bento()