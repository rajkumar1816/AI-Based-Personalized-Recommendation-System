"""Application configuration for the AI-based recommendation system."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'app.db')
DEFAULT_DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'movies.csv')
KAGGLE_DATASET_PATH = os.path.join(ROOT_DIR, 'tmdb_5000_movies.csv')
DATASET_PATH = os.environ.get('DATASET_PATH') or (
    KAGGLE_DATASET_PATH if os.path.exists(KAGGLE_DATASET_PATH) else DEFAULT_DATASET_PATH
)
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
DEBUG = False
APP_NAME = 'AI-Based Personalized Recommendation System'

# TMDB (The Movie Database) settings — set `TMDB_API_KEY` in your environment to enable
# poster lookup by title. If not set, the app will fall back to a default local image.
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
TMDB_IMAGE_BASE_URL = os.environ.get('TMDB_IMAGE_BASE_URL', 'https://image.tmdb.org/t/p/w500')
POSTER_DIR = os.path.join(BASE_DIR, 'static', 'images', 'posters')
POSTER_MAP_PATH = os.path.join(BASE_DIR, 'dataset', 'poster_map.csv')

os.makedirs(DATABASE_DIR, exist_ok=True)
