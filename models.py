from datetime import datetime
from typing import Optional, Literal
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pymongo.errors import DuplicateKeyError

load_dotenv()

class Image:
    def __init__(self):

        # Configurações
        ## Aqui o endereço do seu servidor mongodb
        self.client = MongoClient("mongodb://localhost:27017")
        ## Aqui o nome do seu banco de dados
        self.db = self.client["ic-tcc"]
        ## Aqui o nome da sua coleção
        self.collection = self.db["images"]


        self.collection.create_index("path",unique=True)

    def insert_image(self, image_data: dict):
        """Insert a single image record into MongoDB"""
        image_data["created_at"] = datetime.now()
        try:
            return self.collection.insert_one(image_data)
        except DuplicateKeyError:
            return None

    def insert_multiple_images(self, base_data: dict, count: int, base_path: str):
        """Insert multiple images with the same characteristics but different paths"""
        extension = os.path.splitext(base_path)[1]
        results = []
        
        for i in range(count):
            image_data = base_data.copy()
            image_data["path"] = f"{os.path.splitext(base_path)[0]}_{i}{extension}"
            image_data["created_at"] = datetime.now()
            result = self.collection.insert_one(image_data)
            results.append(result.inserted_id)
            
        return results 