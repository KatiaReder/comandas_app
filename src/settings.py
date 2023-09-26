from dotenv import load_dotenv, find_dotenv
import os

dotenv_file = find_dotenv()

load_dotenv(dotenv_file)

HOST  = os.getenv("HOST")
PORT  = os.getenv("PORT")
DEBUG = os.getenv("DEBUG")