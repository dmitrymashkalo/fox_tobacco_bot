import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USER = os.getenv("ADMIN_USER")
CURRENCY = os.getenv("CURRENCY")

API_GET_BRANDS = os.getenv("API_GET_BRANDS")
API_GET_FLAVORS_BY_BRAND = os.getenv("API_GET_FLAVORS_BY_BRAND")
API_GET_FLAVOR_DETAILS = os.getenv("API_GET_FLAVOR_DETAILS")

IMG_URLS = os.getenv("IMG_URLS")