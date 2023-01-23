import os
from from_root import from_root

AWS_ACCESS_KEY_ID_ENV_KEY = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV_KEY = "AWS_SECRET_ACCESS_KEY"
AWS_REGION_NAME = "AWS_REGION"
S3_TRAINING_BUCKET_NAME = "bsb4018-rec-sys-app"
S3_FEAST_FEATURE_STORE = "feast-fs-registries-bsb4018"
S3_MODEL_STORE_BUCKET = "bsb4018-rec-sys-app-bentoStore"
PRODUCTION_MODEL_FILE_PATH = os.path.join("production_model")
INTERACTIONS_MODEL_FILE_PATH = "production_interactions_model.pkl"
COURSES_MODEL_FILE_PATH = "production_courses_model.pkl"
INTERACTIONS_MATRIX_FILE_PATH = "production_interaction_matrix.npz"

#FEATURE_STORE_FILE_PATH = os.getenv("FEAST_FEATURE_STORE_REPO_PATH")
FEATURE_STORE_FILE_PATH = os.path.join("feature_repo")
#COURSES_DATA_FILE_PATH = os.getenv("COURSES_DATA_FILE_PATH")