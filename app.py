"""Application entry point for the AI-Based Personalized Recommendation System."""
from flask import Flask
from routes.home import home_bp
from routes.recommendation import rec_bp
from routes.history import history_bp
from routes.favorites import fav_bp
from routes.dashboard import dash_bp
from services.recommendation_service import service
from utils.database import initialize_db, insert_movies_from_csv
from config import DATASET_PATH, SECRET_KEY
from utils.logger import get_logger

logger = get_logger()


def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object('config')
    app.secret_key = SECRET_KEY

    @app.context_processor
    def inject_filters():
        filters = service.get_filters()
        return {
            'categories': ['All', 'Movies'],
            'genres': ['All'] + filters['genres'],
            'languages': ['All'] + filters['languages'],
            'years': ['All'] + [str(year) for year in sorted(filters['years'], reverse=True)],
        }

    app.register_blueprint(home_bp)
    app.register_blueprint(rec_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(fav_bp)
    app.register_blueprint(dash_bp)

    try:
        initialize_db()
        insert_movies_from_csv(DATASET_PATH)
        logger.info('Database initialized and movies loaded.')
    except Exception as error:
        logger.exception('Startup initialization failed: %s', error)

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(debug=False, host='0.0.0.0', port=5000)
