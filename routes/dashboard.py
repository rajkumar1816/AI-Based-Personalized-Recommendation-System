"""Dashboard analytics route."""
from flask import Blueprint, render_template, jsonify
from models.analytics_manager import AnalyticsManager

dash_bp = Blueprint('dashboard', __name__)


@dash_bp.route('/dashboard', methods=['GET'])
def dashboard():
    totals = AnalyticsManager.totals()
    top_genre = AnalyticsManager.most_favorite_genre()
    top_movie = AnalyticsManager.most_viewed_movie()
    return render_template('dashboard.html', totals=totals, top_genre=top_genre, top_movie=top_movie)


@dash_bp.route('/dashboard/data', methods=['GET'])
def dashboard_data():
    totals = AnalyticsManager.totals()
    return jsonify(
        {
            'totals': totals,
            'searches_per_day': AnalyticsManager.searches_per_day(),
            'favorite_genres': AnalyticsManager.favorite_genres(),
            'user_activity': AnalyticsManager.user_activity(),
        }
    )
