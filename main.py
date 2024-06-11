from config import settings
from app.services.dalle3 import Dalle3_Engine

if __name__ == "__main__":
    prompt = "A cute cat sitting on a chair"
    engine = Dalle3_Engine(prompt)
