"""Home route serving the main dashboard and search UI."""
from flask import Blueprint, render_template
from services.recommendation_service import service

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    """Render the main index page with search filters."""
    filters = service.get_filters()
    return render_template(
        'index.html',
        categories=['All', 'Movies'],
        genres=['All'] + filters['genres'],
        languages=['All'] + filters['languages'],
        years=['All'] + [str(year) for year in sorted(filters['years'], reverse=True)],
    )
