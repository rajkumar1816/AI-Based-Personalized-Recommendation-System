"""Recommendation routes for GET and POST."""
from flask import Blueprint, request, render_template, jsonify
from services.recommendation_service import service
from models.history_manager import HistoryManager
from utils.helper import build_error_message

rec_bp = Blueprint('recommendation', __name__)


@rec_bp.route('/recommend', methods=['GET'])
def recommend_get():
    """Render the dedicated recommendation page and handle optional query parameters."""
    query = request.args.get('q', '').strip()
    category = request.args.get('category', 'All').strip()
    genre = request.args.get('genre', 'All').strip()
    language = request.args.get('language', 'All').strip()
    rating = request.args.get('rating', '')
    year = request.args.get('year', '')

    results = []
    debug = {}

    try:
        rating_value = float(rating) if rating else None
    except ValueError:
        rating_value = None

    try:
        year_value = int(year) if year and year.isdigit() else None
    except ValueError:
        year_value = None

    if query:
        try:
            HistoryManager.add(query, category)
        except Exception:
            pass

        payload = service.get_recommendations(
            query=query,
            top_n=5,
            genre=genre,
            language=language,
            min_rating=rating_value,
            year=year_value,
        )
        results = payload.get('recommendations', [])
        debug = {}

    return render_template('recommendation.html', results=results, debug=debug, query=query)


@rec_bp.route('/recommend', methods=['POST'])
def recommend_post():
    """Accept JSON form with search criteria and return recommendations."""
    data = request.json or request.form
    query = data.get('query', '').strip()
    category = data.get('category', 'All').strip()
    genre = data.get('genre', 'All').strip()
    language = data.get('language', 'All').strip()
    rating = data.get('rating')
    year = data.get('year')

    if not query:
        return jsonify(build_error_message('Please enter a search query to get recommendations.')), 400

    try:
        rating_value = float(rating) if rating else None
    except ValueError:
        rating_value = None

    try:
        year_value = int(year) if year and year.isdigit() else None
    except ValueError:
        year_value = None

    try:
        HistoryManager.add(query, category)
    except Exception:
        pass

    payload = service.get_recommendations(
        query=query,
        top_n=5,
        genre=genre,
        language=language,
        min_rating=rating_value,
        year=year_value,
    )
    return jsonify(payload)


@rec_bp.route('/suggestions', methods=['GET'])
def suggestion_get():
    """Provide search suggestions based on the current query fragment."""
    query = request.args.get('q', '').strip()
    suggestions = service.search_suggestions(query)
    return jsonify({'suggestions': suggestions})
