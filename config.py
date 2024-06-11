import os
from dotenv import load_dotenv


# Specify the path to your .env file
env_path = '.env' # Change the Path

# If env_path exists, load the .env file
if os.path.exists(env_path):
    load_dotenv(env_path)

class Settings:
    def __init__(self):
        os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
        pass

settings = Settings()