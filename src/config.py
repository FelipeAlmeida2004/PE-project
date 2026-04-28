from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    PATH_DICT = os.getenv("PATH_DICT")
    SHEET_NAME = os.getenv("SHEET_NAME").split(",")
    DATA = os.getenv("DATA").split(",")


