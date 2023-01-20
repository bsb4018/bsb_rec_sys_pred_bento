import os
from boto3 import Session
from user_activity_model.exception import PredictionException
from user_activity_model.constants import AWS_ACCESS_KEY_ID_ENV_KEY,AWS_REGION_NAME,AWS_SECRET_ACCESS_KEY_ENV_KEY,S3_TRAINING_BUCKET_NAME,PRODUCTION_MODEL_FILE_PATH
import sys
#import certifi

class AwsStorage:
    def __init__(self):
        try:
            self.ACCESS_KEY_ID = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
            self.SECRET_KEY = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY)
            self.REGION_NAME = os.getenv(AWS_REGION_NAME)
            self.BUCKET_NAME = S3_TRAINING_BUCKET_NAME
        except Exception as e:
            raise PredictionException(e,sys)

    def get_aws_storage_config(self):
        try:
            return self.__dict__
        except Exception as e:
            raise PredictionException(e,sys)


class StorageConnection:
    """
    Created connection with S3 bucket using boto3 api to fetch the model from Repository.
    """
    def __init__(self):
        try:
            self.config = AwsStorage()
            self.session = Session(aws_access_key_id=self.config.ACCESS_KEY_ID,
                                   aws_secret_access_key=self.config.SECRET_KEY,
                                   region_name=self.config.REGION_NAME)
            self.s3 = self.session.resource("s3")
            self.bucket = self.s3.Bucket(self.config.BUCKET_NAME)
        except Exception as e:
            raise PredictionException(e,sys)

    def download_production_model_s3(self):
        """
        Download the contents of a folder directory
        Args:
            bucket_name: the name of the s3 bucket
            s3_folder: the folder path in the s3 bucket
            local_dir: a relative or absolute directory path in the local file system
        """
        try:
            
            s3_folder = "saved_models"
            local_dir = PRODUCTION_MODEL_FILE_PATH
            bucket = self.bucket
            for obj in bucket.objects.filter(Prefix=s3_folder):
                target = obj.key if local_dir is None \
                    else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
                if not os.path.exists(os.path.dirname(target)):
                    os.makedirs(os.path.dirname(target))
                if obj.key[-1] == '/':
                    continue
                bucket.download_file(obj.key, target)
        except Exception as e:
            raise PredictionException(e,sys)


if __name__ == "__main__":
    connection = StorageConnection()
    connection.download_production_model_s3()




