import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SERECT_KEY = 'supersecret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False