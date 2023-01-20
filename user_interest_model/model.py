from typing import List
import sys
import random
from user_interest_model.connections import MongoDBClient
from user_interest_model.exception import PredictionException
import bentoml

def _find_courses_interest(tag: str):
    try:
        mongodbc = MongoDBClient()
        client = mongodbc.client
        connection = mongodbc.dbcollection        
        randomnos = random.randint(1,20)
        courses1 = connection.find({'category': tag}, {'_id': 0, 'course_name':1}).limit(1).skip(randomnos)
        randomnos = random.randint(1,20)
        courses2 = connection.find({'category': tag}, {'_id': 0, 'course_name':1}).limit(1).skip(randomnos)
        randomnos = random.randint(1,20)
        courses3 = connection.find({'category': tag}, {'_id': 0, 'course_name':1}).limit(1).skip(randomnos)
            
        recommended_list = []
        clist = dict(courses1.next())
        for _,val in clist.items():
            recommended_list.append(val)
        clist = dict(courses2.next())
        for _,val in clist.items():
            recommended_list.append(val)
        clist = dict(courses3.next())
        for _,val in clist.items():
            recommended_list.append(val)
        
        client.close()
        return recommended_list
    except Exception as e:
        raise PredictionException(e,sys)


def recommend_by_similar_interest(item_dict) -> List[List[str]]:
    try:
        courses = []
        if item_dict["web_dev"] == 1:
            tag = "web_dev"
            courses.append(_find_courses_interest(tag))
        if item_dict["data_sc"] == 1:
            tag = "data_sc"
            courses.append(_find_courses_interest(tag))
        if item_dict['data_an'] == 1:
            tag = "data_an"
            courses.append(_find_courses_interest(tag))
        if item_dict['game_dev'] == 1:
            tag = "game_dev"
            courses.append(_find_courses_interest(tag))
        if item_dict['mob_dev'] == 1:
            tag = "mob_dev"
            courses.append(_find_courses_interest(tag))
        if item_dict['program'] == 1:
            tag = "program"
            courses.append(_find_courses_interest(tag))
        if item_dict['cloud'] == 1:
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
        
        except Exception as e:
            raise PredictionException(e,sys)


if __name__ == "__main__":
    save_interest_model_bento()